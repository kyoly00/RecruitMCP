"""
Work24 API 호출 테스트 스크립트
MCP 서버 없이 직접 API 호출 테스트
"""

import asyncio
import sys
import os

# 프로젝트 루트를 PYTHONPATH에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tools.recruit_tools import find_recruit_notice
from tools.training_tools import find_training_course
from tools.company_tools import find_strong_company
from tools.youth_program_tools import list_youth_programs, match_youth_programs


async def test_recruit():
    """공채속보 API 테스트"""
    print("\n" + "=" * 50)
    print("테스트: 공채속보 검색 (find_recruit_notice)")
    print("=" * 50)
    
    try:
        result = await find_recruit_notice(
            page=1,
            page_size=5,
        )
        print(f"총 결과: {result.get('total', 0)}건")
        print(f"반환된 항목: {len(result.get('items', []))}건")
        
        for i, item in enumerate(result.get("items", [])[:3], 1):
            print(f"\n  [{i}] {item.get('company', 'N/A')} - {item.get('title', 'N/A')}")
            print(f"      고용형태: {item.get('employment_type', 'N/A')}")
            
    except Exception as e:
        print(f"에러: {e}")
        import traceback
        traceback.print_exc()


async def test_training():
    """훈련과정 API 테스트"""
    print("\n" + "=" * 50)
    print("테스트: 훈련과정 검색 (find_training_course)")
    print("=" * 50)
    
    try:
        result = await find_training_course(
            start_date="20260101",
            end_date="20260331",
            page=1,
            page_size=5,
        )
        print(f"총 결과: {result.get('total', 0)}건")
        print(f"반환된 항목: {len(result.get('items', []))}건")
        
        for i, item in enumerate(result.get("items", [])[:3], 1):
            print(f"\n  [{i}] {item.get('title', 'N/A')}")
            print(f"      기관: {item.get('provider_name', 'N/A')}")
            
    except Exception as e:
        print(f"에러: {e}")
        import traceback
        traceback.print_exc()


async def test_company():
    """기업정보 API 테스트"""
    print("\n" + "=" * 50)
    print("테스트: 강소기업 검색 (find_strong_company)")
    print("=" * 50)
    
    try:
        result = await find_strong_company(
            page=1,
            page_size=5,
        )
        print(f"총 결과: {result.get('total', 0)}건")
        print(f"반환된 항목: {len(result.get('items', []))}건")
        
        for i, item in enumerate(result.get("items", [])[:3], 1):
            print(f"\n  [{i}] {item.get('company_name', 'N/A')}")
            print(f"      유형: {item.get('company_type', 'N/A')}")
            print(f"      소개: {item.get('summary', 'N/A')[:50]}..." if item.get('summary') else "")
            
    except Exception as e:
        print(f"에러: {e}")
        import traceback
        traceback.print_exc()


async def test_youth_programs():
    """청년 프로그램 테스트 (로컬 JSON)"""
    print("\n" + "=" * 50)
    print("테스트: 청년 프로그램 목록 (list_youth_programs)")
    print("=" * 50)
    
    try:
        result = await list_youth_programs()
        print(f"총 프로그램: {result.get('total', 0)}개")
        
        for i, item in enumerate(result.get("items", [])[:3], 1):
            print(f"\n  [{i}] {item.get('name', 'N/A')}")
            print(f"      카테고리: {item.get('category', 'N/A')}")
            
    except Exception as e:
        print(f"에러: {e}")
        import traceback
        traceback.print_exc()


async def main():
    print("=" * 60)
    print("Work24 API 직접 호출 테스트")
    print("=" * 60)
    
    # 청년 프로그램 (로컬) - 항상 동작해야 함
    await test_youth_programs()
    
    # 공채속보 API
    await test_recruit()
    
    # 훈련과정 API
    await test_training()
    
    # 기업정보 API
    await test_company()
    
    print("\n" + "=" * 60)
    print("테스트 완료")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
