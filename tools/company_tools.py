"""
Company (기업정보) MCP Tools
강소기업/공채기업 검색 도구
API: callOpenApiSvcInfo210L31
"""

from utils.http_client import call_work24_api, safe_get, ensure_list, ApiType


async def find_strong_company(
    company_type_codes: list[str] | None = None,
    company_name: str | None = None,
    page: int = 1,
    page_size: int = 10,
    sort_field: str | None = None,
    sort_order: str = "DESC",
) -> dict:
    """
    Search strong/hiring companies from Work24.
    
    Args:
        company_type_codes: List of company type codes (['10', '20', '40'] etc.)
            - '10': 강소기업
            - '20': 일생활균형우수기업  
            - '40': 청년친화강소기업
        company_name: Company name keyword search
        page: Page number (1-indexed)
        page_size: Number of results per page
        sort_field: Sort field name
        sort_order: Sort order ('ASC' or 'DESC')
    
    Returns:
        Dictionary with total count and list of companies
    """
    params = {
        "startPage": page,
        "display": page_size,
        "callTp": "L",
        "sortOrderBy": sort_order,
    }
    
    if company_type_codes:
        params["coClcd"] = "|".join(company_type_codes)
    if company_name:
        params["coNm"] = company_name
    if sort_field:
        params["sortField"] = sort_field
    
    data = await call_work24_api(
        "callOpenApiSvcInfo210L31",
        params,
        api_type=ApiType.RECRUIT,  # COMPANY와 RECRUIT는 같은 키 사용
    )
    
    # 실제 XML 구조: dhsOpenEmpHireInfoList > dhsOpenEmpHireInfo
    root = safe_get(data, "dhsOpenEmpHireInfoList", default={})
    total = int(safe_get(root, "total", default="0"))
    company_list = ensure_list(safe_get(root, "dhsOpenEmpHireInfo", default=[]))
    
    items = []
    for co in company_list:
        item = {
            "company_id": safe_get(co, "empCoNo", default=""),
            "company_name": safe_get(co, "coNm", default=""),
            "company_type": safe_get(co, "coClcdNm", default=None),
            "business_no": safe_get(co, "busino", default=None),
            "summary": safe_get(co, "coIntroSummaryCont", default=None),
            "description": safe_get(co, "coIntroCont", default=None),
            "homepage": safe_get(co, "homepg", default=None),
            "main_business": safe_get(co, "mainBusiCont", default=None),
            "logo_url": safe_get(co, "regLogImgNm", default=None),
            "latitude": _parse_float(safe_get(co, "mapCoorY")),
            "longitude": _parse_float(safe_get(co, "mapCoorX")),
        }
        items.append(item)
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": items,
    }


def _parse_int(value) -> int | None:
    """Parse integer from string, return None if not possible."""
    if value is None:
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def _parse_float(value) -> float | None:
    """Parse float from string, return None if not possible."""
    if value is None:
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None
