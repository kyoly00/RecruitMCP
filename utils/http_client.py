"""
Work24 OPEN API HTTP Client
Shared utility for calling Work24 APIs and parsing XML responses.
"""

import os
import sys
import logging
import traceback
from typing import Any
from enum import Enum
import httpx
import xmltodict
from dotenv import load_dotenv

# stderr로 로깅 설정 (MCP는 stdout을 JSON-RPC로 사용하므로 stderr 필수)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
logger = logging.getLogger("work24_http_client")

# 환경변수 로드
load_dotenv()
logger.info("dotenv loaded")

# Base URLs for Work24 APIs
WORK24_BASE_URL = "https://www.work24.go.kr/cm/openApi/call"
logger.info("WORK24_BASE_URL: %s", WORK24_BASE_URL)
WORK24_WK_BASE = f"{WORK24_BASE_URL}/wk"  # 채용, 정부지원일자리, 기업
WORK24_HR_BASE = f"{WORK24_BASE_URL}/hr"  # 훈련

logger.info("Base URLs - WK: %s, HR: %s", WORK24_WK_BASE, WORK24_HR_BASE)


class ApiType(str, Enum):
    """API types with corresponding environment variable names."""
    RECRUIT = "WORK24_RECRUIT_AUTH_KEY"      # 채용정보/공채속보 (210L21), 기업정보 (210L31)
    TRAINING = "WORK24_TRAINING_AUTH_KEY"    # 훈련과정 (310L01, 310L02)


def get_auth_key(api_type: ApiType) -> str:
    """
    Get Work24 API authentication key for specific API type.
    """
    logger.debug("get_auth_key called for api_type=%s", api_type)
    key = os.getenv(api_type.value)
    if not key:
        error_msg = f"{api_type.value} environment variable is not set"
        logger.error(error_msg)
        raise ValueError(error_msg)
    logger.debug("Auth key found (length=%d)", len(key))
    return key


async def call_work24_api(
    endpoint: str,
    params: dict[str, Any],
    api_type: ApiType,
    base_url: str = WORK24_WK_BASE,
    return_type: str = "XML",
) -> dict[str, Any]:
    """
    Call Work24 OPEN API and parse response.
    """
    logger.info("=" * 50)
    logger.info("call_work24_api START")
    logger.info("  endpoint: %s", endpoint)
    logger.info("  api_type: %s", api_type)
    logger.info("  params: %s", params)
    logger.info("  base_url: %s", base_url)
    logger.info("  return_type: %s", return_type)

    try:
        url = f"{base_url}/{endpoint}.do"
        logger.info("  Full URL (without params): %s", url)

        # Add common parameters with API-specific auth key
        auth_key = get_auth_key(api_type)
        request_params: dict[str, Any] = {
            "authKey": auth_key,
            "returnType": return_type,
            **params,
        }

        # Remove None values
        request_params = {k: v for k, v in request_params.items() if v is not None}
        
        # authKey 마스킹하여 로깅
        log_params = {k: (v[:8] + "..." if k == "authKey" else v) for k, v in request_params.items()}
        logger.info("  Request params (masked): %s", log_params)

        async with httpx.AsyncClient(timeout=30.0) as client:
            logger.info("  Sending HTTP GET request...")
            response = await client.get(url, params=request_params)
            
            # 최종 호출 URL 로깅 (authKey 포함된 실제 URL)
            final_url = str(response.request.url)
            # authKey 마스킹
            if "authKey=" in final_url:
                import re
                masked_url = re.sub(r'authKey=[^&]+', 'authKey=***MASKED***', final_url)
                logger.info("  Final URL (masked): %s", masked_url)
            
            logger.info("  Response status: %d", response.status_code)
            logger.debug("  Response headers: %s", dict(response.headers))
            
            response.raise_for_status()
            
            response_text = response.text
            # 디버깅: XML 응답 전체 출력
            logger.info("  Response XML (first 1000 chars):\n%s", response_text[:1000])
            
            if return_type == "XML":
                result = xmltodict.parse(response_text)
                logger.info("  XML parsed successfully")
                # 디버깅: 파싱된 결과의 키 출력
                logger.info("  Parsed result: %s", result)
            else:
                result = response.json()
                logger.info("  JSON parsed successfully")
            
            logger.info("call_work24_api END - SUCCESS")
            logger.info("=" * 50)
            return result
            
    except httpx.HTTPStatusError as e:
        logger.error("HTTP Error: %s", e)
        logger.error("Response body: %s", e.response.text[:500] if e.response else "N/A")
        raise
    except Exception as e:
        logger.error("Unexpected error in call_work24_api: %s", e)
        logger.error("Traceback: %s", traceback.format_exc())
        raise


def safe_get(data: dict, *keys, default: Any = None) -> Any:
    """Safely get nested dictionary value."""
    result = data
    for key in keys:
        if isinstance(result, dict):
            result = result.get(key)
        else:
            return default
        if result is None:
            return default
    return result


def ensure_list(value: Any) -> list:
    """Ensure value is a list (wrap single items)."""
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]
