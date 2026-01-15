"""
Work24 MCP Server
fastmcp 기반 MCP 서버 - 고용24 OPEN API 도구 제공

Usage:
    uv run python server.py
    
Or with MCP Inspector:
    npx @anthropic/mcp-inspector uv run python server.py
"""

import sys
import logging

# stderr로 로깅 (MCP는 stdout을 JSON-RPC로 사용)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
logger = logging.getLogger("work24_mcp_server")
logging.getLogger("docket").setLevel(logging.WARNING)
logging.getLogger("fakeredis").setLevel(logging.WARNING)
logging.getLogger("fastmcp").setLevel(logging.WARNING)

from fastmcp import FastMCP

# Import tool functions
from tools.recruit_tools import find_recruit_notice, get_recruit_detail
from tools.training_tools import find_training_course, get_training_course_detail
from tools.company_tools import find_strong_company
from tools.youth_program_tools import list_youth_programs, match_youth_programs

# Create MCP server
mcp = FastMCP(
    name="work24-mcp-server",
    version="0.1.0",
)


# ============================================================
# 1. 채용 축 (Recruit)
# ============================================================

@mcp.tool()
async def find_recruit_notice_tool(
    page: int = 1,
    page_size: int = 10,
    region: str | None = None,
    occupation_codes: list[str] | None = None,
    salary_type: str | None = None,
    min_salary: int | None = None,
    max_salary: int | None = None,
    education_code: str | None = None,
    career_type: str | None = None,
) -> dict:
    """
    Search job postings from Work24 (워크넷).
    
    Args:
        page: Page number (1-indexed)
        page_size: Number of results per page (max 100)
        region: Region code (e.g., '11' for Seoul, '26' for Busan, '41' for Gyeonggi)
        occupation_codes: List of occupation codes (e.g., ['023', '024'] for IT jobs)
        salary_type: Salary type - 'Y'=annual, 'M'=monthly, 'D'=daily, 'H'=hourly
        min_salary: Minimum salary in 10,000 KRW units (e.g., 3000 = 30M KRW/year)
        max_salary: Maximum salary in 10,000 KRW units
        education_code: Education level code ('00'=무관, '01'=초졸, '02'=중졸, '03'=고졸, '04'=대졸2~3년, '05'=대졸4년, '06'=석사, '07'=박사)
        career_type: 'N'=entry level, 'E'=experienced, 'Z'=no preference
    
    Returns:
        Dictionary with total count and list of job postings including company, title, salary, region
    """
    logger.info("find_recruit_notice_tool called with page=%s, page_size=%s, region=%s, occupation_codes=%s",
                page, page_size, region, occupation_codes)
    try:
        result = await find_recruit_notice(
            page=page,
            page_size=page_size,
            region=region,
            occupation_codes=occupation_codes,
            salary_type=salary_type,
            min_salary=min_salary,
            max_salary=max_salary,
            education_code=education_code,
            career_type=career_type,
        )
        logger.info("find_recruit_notice_tool returned %d items", len(result.get("items", [])))
        return result
    except Exception as e:
        logger.error("find_recruit_notice_tool error: %s", e, exc_info=True)
        raise


@mcp.tool()
async def get_recruit_detail_tool(emp_seqno: str) -> dict:
    """
    Get detailed information for a specific job posting from 공채속보.
    
    Args:
        emp_seqno: Unique job posting ID (empSeqno) from find_recruit_notice_tool results
    
    Returns:
        Detailed job posting including company, title, dates, and URLs
    """
    return await get_recruit_detail(emp_seqno)


# ============================================================
# 3. 훈련 축 (Training)
# ============================================================

@mcp.tool()
async def find_training_course_tool(
    start_date: str,
    end_date: str,
    page: int = 1,
    page_size: int = 20,
    area1: str | None = None,
    ncs1: str | None = None,
    course_type: str | None = None,
    keyword: str | None = None,
    provider_name: str | None = None,
) -> dict:
    """
    Search training courses (내일배움카드, K-Digital Training, etc.).
    
    Args:
        start_date: Training start date from (YYYYMMDD, e.g., '20260101')
        end_date: Training start date to (YYYYMMDD, e.g., '20260331')
        page: Page number (1-indexed)
        page_size: Number of results per page (max 100)
        area1: Region code ('11'=Seoul, '26'=Busan, '27'=Daegu, '28'=Incheon, '29'=Gwangju, '30'=Daejeon, '31'=Ulsan, '36'=Sejong, '41'=Gyeonggi, '42'=Gangwon, '43'=Chungbuk, '44'=Chungnam, '45'=Jeonbuk, '46'=Jeonnam, '47'=Gyeongbuk, '48'=Gyeongnam, '50'=Jeju)
        ncs1: NCS major category ('01'=사업관리, '02'=경영회계사무, '15'=기계, '19'=전기전자, '20'=정보통신)
        course_type: Training type code ('C0061S'=K-Digital Training, 'C0061T'=K-Digital Credit)
        keyword: Course name keyword search
        provider_name: Training provider name search
    
    Returns:
        Dictionary with training courses including tuition, support amount, employment rate
    """
    return await find_training_course(
        start_date=start_date,
        end_date=end_date,
        page=page,
        page_size=page_size,
        area1=area1,
        ncs1=ncs1,
        course_type=course_type,
        keyword=keyword,
        provider_name=provider_name,
    )


@mcp.tool()
async def get_training_course_detail_tool(
    course_id: str,
    course_round: str = "1",
    org_id: str = "",
) -> dict:
    """
    Get detailed information for a specific training course.
    
    Args:
        course_id: Course ID (TRPR_ID) from find_training_course_tool results
        course_round: Course round number (default: "1")
        org_id: Training organization ID
    
    Returns:
        Detailed course info including curriculum, organization details, and costs
    """
    return await get_training_course_detail(
        course_id=course_id,
        course_round=course_round,
        org_id=org_id,
    )


# ============================================================
# 4. 기업 축 (Company)
# ============================================================

@mcp.tool()
async def find_strong_company_tool(
    company_type_codes: list[str] | None = None,
    company_name: str | None = None,
    page: int = 1,
    page_size: int = 10,
) -> dict:
    """
    Search strong/hiring companies from Work24.
    
    Args:
        company_type_codes: List of company type codes
            - '10': 강소기업 (Strong SME)
            - '20': 일생활균형우수기업 (Work-Life Balance)
            - '40': 청년친화강소기업 (Youth-Friendly SME)
        company_name: Company name keyword search
        page: Page number (1-indexed)
        page_size: Number of results per page
    
    Returns:
        Dictionary with companies including industry, employee count, and location
    """
    return await find_strong_company(
        company_type_codes=company_type_codes,
        company_name=company_name,
        page=page,
        page_size=page_size,
    )


# ============================================================
# 5. 청년 프로그램 축 (Youth Programs)
# ============================================================

@mcp.tool()
async def list_youth_programs_tool() -> dict:
    """
    List all available youth support programs in Korea.
    
    Returns:
        Dictionary with all youth programs including eligibility, benefits, and application info
    """
    return await list_youth_programs()


@mcp.tool()
async def match_youth_programs_tool(
    age: int,
    employment_status: str,
    education_status: str | None = None,
    preferences: list[str] | None = None,
) -> dict:
    """
    Match youth programs based on user profile.
    
    Args:
        age: User's age (15-50)
        employment_status: Current status - '구직자' (job seeker), '재직자' (employed), '창업자' (entrepreneur), '학생' (student)
        education_status: Education status - '재학' (enrolled), '휴학' (on leave), '졸업' (graduated), '중퇴' (dropped out)
        preferences: Preferred program categories:
            - 'employment': 일경험 (Work experience)
            - 'training': 교육/훈련 (Education/Training)
            - 'allowance': 수당/지원금 (Allowance/Subsidy)
            - 'startup': 창업 (Startup)
            - 'housing': 주거 (Housing)
            - 'finance': 금융 (Finance)
    
    Returns:
        Dictionary with matched programs sorted by relevance score with match reasons
    """
    return await match_youth_programs(
        age=age,
        employment_status=employment_status,
        education_status=education_status,
        preferences=preferences,
    )


# ============================================================
# Main Entry Point
# ============================================================

def main():
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
