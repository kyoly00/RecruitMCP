"""
Youth Program (청년 프로그램) MCP Tools
로컬 JSON 기반 청년 프로그램 목록/매칭 도구
"""

import json
from pathlib import Path
from models.youth_program import ProgramCategory


# Load youth programs data
_DATA_PATH = Path(__file__).parent.parent / "data" / "youth_programs.json"


def _load_programs() -> list[dict]:
    """Load youth programs from JSON file."""
    if not _DATA_PATH.exists():
        return []
    with open(_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


async def list_youth_programs() -> dict:
    """
    List all available youth support programs.
    
    Returns:
        Dictionary with list of all youth programs with their details
    """
    programs = _load_programs()
    return {
        "total": len(programs),
        "items": programs,
    }


async def match_youth_programs(
    age: int,
    employment_status: str,
    education_status: str | None = None,
    preferences: list[str] | None = None,
    region: str | None = None,
) -> dict:
    """
    Match youth programs based on user profile.
    
    Args:
        age: User's age (15-50)
        employment_status: Current status - '구직자', '재직자', '창업자', '학생'
        education_status: Education status - '재학', '휴학', '졸업', '중퇴'
        preferences: Preferred categories - 'employment', 'training', 'allowance', 'startup', 'housing', 'finance'
        region: Preferred region code
    
    Returns:
        Dictionary with matched programs sorted by relevance score
    """
    programs = _load_programs()
    matched = []
    
    for prog in programs:
        score = 0.0
        reasons = []
        
        # Age matching
        age_min = prog.get("target_age_min", 0)
        age_max = prog.get("target_age_max", 100)
        if age_min <= age <= age_max:
            score += 0.3
            reasons.append(f"Age {age} within range {age_min}-{age_max}")
        else:
            continue  # Skip if age doesn't match
        
        # Employment status matching
        target_status = prog.get("target_employment_status", [])
        if employment_status in target_status or not target_status:
            score += 0.25
            reasons.append(f"Matches employment status: {employment_status}")
        else:
            continue  # Skip if status doesn't match
        
        # Education status matching (optional)
        if education_status:
            target_edu = prog.get("target_education_status", [])
            if education_status in target_edu or not target_edu:
                score += 0.15
                reasons.append(f"Matches education status: {education_status}")
        
        # Preference matching
        if preferences:
            prog_category = prog.get("category", "")
            if prog_category in preferences:
                score += 0.3
                reasons.append(f"Matches preferred category: {prog_category}")
        
        matched.append({
            "program": prog,
            "match_score": round(score, 2),
            "match_reasons": reasons,
        })
    
    # Sort by score descending
    matched.sort(key=lambda x: x["match_score"], reverse=True)
    
    return {
        "total_programs": len(programs),
        "matched_count": len(matched),
        "items": matched[:10],  # Top 10 matches
    }
