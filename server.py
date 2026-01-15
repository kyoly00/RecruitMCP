"""
Work24 MCP Server
FastMCP 기반 MCP 서버 - 고용24 OPEN API 도구 제공

Local:
    uvicorn server:http_app --reload --port 8000
    # 또는: python server.py

Public Endpoint 예:
    http://<host>:8000/mcp
"""

import sys
import logging

from fastmcp import FastMCP
from starlette.responses import JSONResponse

# Tool imports
from tools.recruit_tools import find_recruit_notice, get_recruit_detail
from tools.training_tools import find_training_course, get_training_course_detail
from tools.company_tools import find_strong_company
from tools.youth_program_tools import list_youth_programs, match_youth_programs

# ------------------------------------------------------------
# Logging
# ------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
logger = logging.getLogger("work24_mcp_server")

# ------------------------------------------------------------
# FastMCP 서버 인스턴스
# ------------------------------------------------------------
mcp = FastMCP(
    name="work24-mcp-server",
)

# ------------------------------------------------------------
# 상태 페이지 (루트 /)
# ------------------------------------------------------------
@mcp.custom_route("/", methods=["GET"])
async def root(request):
    """상태 확인용 HTTP 엔드포인트."""
    return JSONResponse(
        {
            "name": "Work24 MCP Server",
            "version": "0.1.0",
            "description": "고용24 OPEN API MCP Server",
            "mcp_endpoint": "/mcp",
        }
    )

# ------------------------------------------------------------
# 1. 채용 축 (Recruit / 공채속보)
# ------------------------------------------------------------
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
    logger.info("find_recruit_notice_tool called page=%s, size=%s", page, page_size)
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


@mcp.tool()
async def get_recruit_detail_tool(emp_seqno: str) -> dict:
    return await get_recruit_detail(emp_seqno)

# ------------------------------------------------------------
# 2. 훈련 축 (Training)
# ------------------------------------------------------------
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
    return await get_training_course_detail(
        course_id=course_id,
        course_round=course_round,
        org_id=org_id,
    )

# ------------------------------------------------------------
# 3. 기업 축 (Company)
# ------------------------------------------------------------
@mcp.tool()
async def find_strong_company_tool(
    company_type_codes: list[str] | None = None,
    company_name: str | None = None,
    page: int = 1,
    page_size: int = 10,
) -> dict:
    return await find_strong_company(
        company_type_codes=company_type_codes,
        company_name=company_name,
        page=page,
        page_size=page_size,
    )

# ------------------------------------------------------------
# 4. 청년 프로그램 축 (Youth Programs)
# ------------------------------------------------------------
@mcp.tool()
async def list_youth_programs_tool() -> dict:
    return await list_youth_programs()


@mcp.tool()
async def match_youth_programs_tool(
    age: int,
    employment_status: str,
    education_status: str | None = None,
    preferences: list[str] | None = None,
) -> dict:
    return await match_youth_programs(
        age=age,
        employment_status=employment_status,
        education_status=education_status,
        preferences=preferences,
    )

# ------------------------------------------------------------
# MCP HTTP/SSE 앱 생성 (/mcp)
# ------------------------------------------------------------
http_app = mcp.http_app(
    "/mcp",
    transport="sse",  # SSE MCP endpoint
)

# ------------------------------------------------------------
# Main Entry Point
# ------------------------------------------------------------
def main():
    """Run MCP HTTP/SSE server with uvicorn."""
    import uvicorn

    uvicorn.run(
        "server:http_app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    main()
