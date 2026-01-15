"""
Recruit (채용/공채속보) MCP Tools
Work24 공채속보 검색 및 상세 조회 도구
API: callOpenApiSvcInfo210L21
"""

from utils.http_client import call_work24_api, safe_get, ensure_list, ApiType


async def find_recruit_notice(
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
    Search job postings from Work24 공채속보 (Open Recruitment News).
    
    Args:
        page: Page number (1-indexed)
        page_size: Number of results per page (max 100)
        region: Region code (e.g., '11' for Seoul, '26' for Busan)
        occupation_codes: List of occupation codes (e.g., ['023100', '021300'])
        salary_type: Salary type - 'Y'=annual, 'M'=monthly, 'D'=daily, 'H'=hourly
        min_salary: Minimum salary in 10,000 KRW units
        max_salary: Maximum salary in 10,000 KRW units
        education_code: Education level code
        career_type: 'N'=entry level, 'E'=experienced, 'Z'=no preference
    
    Returns:
        Dictionary with total count and list of job postings
    """
    params = {
        "callTp": "L",
        "startPage": page,
        "display": page_size,
    }
    
    if region:
        params["region"] = region
    if occupation_codes:
        params["occupation"] = "|".join(occupation_codes)
    if salary_type:
        params["salTp"] = salary_type
    if min_salary:
        params["minPay"] = min_salary
    if max_salary:
        params["maxPay"] = max_salary
    if education_code:
        params["education"] = education_code
    if career_type:
        params["career"] = career_type
    
    # 공채속보 API (210L21) 사용
    data = await call_work24_api(
        "callOpenApiSvcInfo210L21",
        params,
        api_type=ApiType.RECRUIT,
    )
    
    # 공채속보 API의 XML 구조: dhsOpenEmpInfoList > dhsOpenEmpInfo
    root = safe_get(data, "dhsOpenEmpInfoList", default={})
    total = int(safe_get(root, "total", default="0"))
    emp_list = ensure_list(safe_get(root, "dhsOpenEmpInfo", default=[]))
    
    items = []
    for emp in emp_list:
        item = {
            "emp_seqno": safe_get(emp, "empSeqno", default=""),
            "company": safe_get(emp, "empBusiNm", default=""),
            "title": safe_get(emp, "empWantedTitle", default=""),
            "company_type": safe_get(emp, "coClcdNm", default=None),
            "employment_type": safe_get(emp, "empWantedTypeNm", default=None),
            "start_date": _format_date(safe_get(emp, "empWantedStdt")),
            "end_date": _format_date(safe_get(emp, "empWantedEndt")),
            "logo_url": safe_get(emp, "regLogImgNm", default=None),
            "detail_url": safe_get(emp, "empWantedHomepgDetail", default=None),
            "mobile_url": safe_get(emp, "empWantedMobileUrl", default=None),
        }
        items.append(item)
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": items,
    }


async def get_recruit_detail(emp_seqno: str) -> dict:
    """
    Get detailed information for a specific job posting from 공채속보.
    
    Args:
        emp_seqno: Unique job posting ID from find_recruit_notice results
    
    Returns:
        Detailed job posting information
    """
    params = {
        "callTp": "D",
        "empSeqno": emp_seqno,
    }
    
    # 공채속보 API (210L21) 사용
    data = await call_work24_api(
        "callOpenApiSvcInfo210L21",
        params,
        api_type=ApiType.RECRUIT,
    )
    
    # 상세 조회 응답 구조 (확인 필요)
    root = safe_get(data, "dhsOpenEmpInfoList", default={})
    emp = safe_get(root, "dhsOpenEmpInfo", default={})
    
    # 리스트인 경우 첫 번째 항목 사용
    if isinstance(emp, list) and len(emp) > 0:
        emp = emp[0]
    
    return {
        "emp_seqno": emp_seqno,
        "company": safe_get(emp, "empBusiNm", default=""),
        "title": safe_get(emp, "empWantedTitle", default=""),
        "company_type": safe_get(emp, "coClcdNm", default=None),
        "employment_type": safe_get(emp, "empWantedTypeNm", default=None),
        "start_date": _format_date(safe_get(emp, "empWantedStdt")),
        "end_date": _format_date(safe_get(emp, "empWantedEndt")),
        "detail_url": safe_get(emp, "empWantedHomepgDetail", default=None),
        "mobile_url": safe_get(emp, "empWantedMobileUrl", default=None),
        # 상세 필드들 (API 문서 확인 후 추가 가능)
        "raw_data": emp,  # 디버깅용
    }


def _format_date(date_str: str | None) -> str | None:
    """Format date string from YYYYMMDD to YYYY-MM-DD."""
    if not date_str or len(date_str) != 8:
        return date_str
    return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"


def _parse_int(value) -> int | None:
    """Parse integer from string, return None if not possible."""
    if value is None:
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None
