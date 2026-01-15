"""
Training Course (훈련과정) MCP Tools
내일배움카드 훈련과정 검색 및 상세 조회 도구
"""

from utils.http_client import call_work24_api, safe_get, ensure_list, WORK24_HR_BASE, ApiType


async def find_training_course(
    start_date: str,
    end_date: str,
    page: int = 1,
    page_size: int = 20,
    area1: str | None = None,
    area2: str | None = None,
    ncs1: str | None = None,
    ncs2: str | None = None,
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
        area1: Region code level 1 (e.g., '11' for Seoul, '41' for Gyeonggi)
        area2: Region code level 2 (detailed area)
        ncs1: NCS major category code (e.g., '20' for IT)
        ncs2: NCS middle category code
        course_type: Training type code (e.g., 'C0061S' for K-Digital Training)
        keyword: Course name keyword search
        provider_name: Training provider name search
    
    Returns:
        Dictionary with total count and list of training courses with employment rates
    """
    params = {
        "outType": "1",  # List type
        "pageNum": page,
        "pageSize": page_size,
        "srchTraStDt": start_date,
        "srchTraEndDt": end_date,
    }
    
    if area1:
        params["srchTraArea1"] = area1
    if area2:
        params["srchTraArea2"] = area2
    if ncs1:
        params["srchNcs1"] = ncs1
    if ncs2:
        params["srchNcs2"] = ncs2
    if course_type:
        params["crseTracseSe"] = course_type
    if keyword:
        params["srchTraProcessNm"] = keyword
    if provider_name:
        params["srchTraOrganNm"] = provider_name
    
    data = await call_work24_api(
        "callOpenApiSvcInfo310L01", 
        params, 
        api_type=ApiType.TRAINING,
        base_url=WORK24_HR_BASE,
    )
    
    # Parse XML response
    # 실제 구조: HRDNet > srchList > scn_list
    root = safe_get(data, "HRDNet", default={})
    total = int(safe_get(root, "scn_cnt", default="0"))
    srch_list = safe_get(root, "srchList", default={})
    course_list = ensure_list(safe_get(srch_list, "scn_list", default=[]))
    
    items = []
    for c in course_list:
        item = {
            "course_id": safe_get(c, "trprId", default=""),
            "course_round": safe_get(c, "trprDegr", default="1"),
            "title": safe_get(c, "title", default=""),  # 실제 필드명 수정
            "provider_name": safe_get(c, "subTitle", default=""),  # 실제 필드명
            "address": safe_get(c, "address", default=None),
            "phone": safe_get(c, "telNo", default=None),
            "start_date": safe_get(c, "traStartDate", default=None),  # 이미 포맷됨
            "end_date": safe_get(c, "traEndDate", default=None),
            "ncs_code": safe_get(c, "ncsCd", default=None),
            "tuition": _parse_int(safe_get(c, "courseMan")),
            "support_amount": _parse_int(safe_get(c, "realMan")),
            "employment_rate_3m": safe_get(c, "eiEmplRate3", default=None),
            "satisfaction_score": safe_get(c, "stdgScor", default=None),
            "org_id": safe_get(c, "trainstCstId", default=None),
            "train_target": safe_get(c, "trainTarget", default=None),
            "title_link": safe_get(c, "titleLink", default=None),
        }
        items.append(item)
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": items,
    }


async def get_training_course_detail(
    course_id: str,
    course_round: str = "1",
    org_id: str = "",
) -> dict:
    """
    Get detailed information for a specific training course.
    
    Args:
        course_id: Course ID (TRPR_ID) from find_training_course results
        course_round: Course round number
        org_id: Training organization ID
    
    Returns:
        Detailed course information including curriculum and organization details
    """
    params = {
        "outType": "2",  # Detail type
        "srchTrprId": course_id,
        "srchTrprDegr": course_round,
        "srchTorgId": org_id,
    }
    
    data = await call_work24_api(
        "callOpenApiSvcInfo310L02",
        params,
        api_type=ApiType.TRAINING,
        base_url=WORK24_HR_BASE,
    )
    
    root = safe_get(data, "HRDNet", default={})
    inst_base = safe_get(root, "inst_base_info", default={})
    inst_detail = safe_get(root, "inst_detail_info", default={})
    
    # Determine if K-Digital
    course_type = safe_get(inst_base, "crseTracseSe", default="")
    is_k_digital = "C0061" in str(course_type) if course_type else False
    
    return {
        "course_id": course_id,
        "course_round": course_round,
        "course_name": safe_get(inst_base, "trprNm", default=""),
        "org_name": safe_get(inst_base, "inoNm", default=""),
        "org_homepage": safe_get(inst_base, "hpAddr", default=None),
        "org_address": safe_get(inst_base, "addr", default=None),
        "org_tel": safe_get(inst_base, "telNo", default=None),
        "ncs_code": safe_get(inst_base, "ncsCd", default=None),
        "ncs_name": safe_get(inst_base, "ncsNm", default=None),
        "total_days": _parse_int(safe_get(inst_detail, "trDcnt")),
        "total_hours": _parse_int(safe_get(inst_detail, "trtm")),
        "tuition": _parse_int(safe_get(inst_detail, "courseMan")),
        "support_amount": _parse_int(safe_get(inst_detail, "realMan")),
        "target": safe_get(inst_detail, "trgtCat", default=None),
        "is_k_digital": is_k_digital,
        "curriculum": safe_get(inst_detail, "trainGoal", default=None),
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
