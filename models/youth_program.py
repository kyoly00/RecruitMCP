"""
Pydantic models for Youth Program (청년 프로그램) matching.
Local JSON-based matching, not from Work24 API.
"""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class ProgramCategory(str, Enum):
    """Youth program categories."""
    EMPLOYMENT = "employment"      # 일경험
    TRAINING = "training"          # 교육/훈련
    ALLOWANCE = "allowance"        # 수당/지원금
    STARTUP = "startup"            # 창업
    HOUSING = "housing"            # 주거
    FINANCE = "finance"            # 금융


class YouthProgram(BaseModel):
    """Single youth support program."""
    program_id: str = Field(description="Program ID")
    name: str = Field(description="Program name")
    category: ProgramCategory = Field(description="Program category")
    description: str = Field(description="Program description")
    target_age_min: int = Field(description="Minimum age for eligibility")
    target_age_max: int = Field(description="Maximum age for eligibility")
    target_employment_status: list[str] = Field(description="Target employment status (구직자, 재직자, 창업자, etc.)")
    target_education_status: list[str] = Field(default=[], description="Target education status")
    benefits: list[str] = Field(description="Key benefits")
    apply_channel: str = Field(description="Application channel/method")
    apply_url: Optional[str] = Field(default=None, description="Application URL")
    related_api_id: Optional[str] = Field(default=None, description="Related Work24 API ID if applicable")


class YouthProgramMatchRequest(BaseModel):
    """Request model for youth program matching."""
    age: int = Field(ge=15, le=50, description="User's age")
    employment_status: str = Field(description="Employment status: 구직자, 재직자, 창업자, 학생")
    education_status: Optional[str] = Field(default=None, description="Education status: 재학, 휴학, 졸업, 중퇴")
    preferences: list[ProgramCategory] = Field(default=[], description="Preferred program categories")
    region: Optional[str] = Field(default=None, description="Preferred region")


class YouthProgramMatchItem(BaseModel):
    """Matched program with score."""
    program: YouthProgram = Field(description="Matched program")
    match_score: float = Field(ge=0, le=1, description="Match score (0-1)")
    match_reasons: list[str] = Field(description="Reasons for matching")


class YouthProgramMatchResponse(BaseModel):
    """Response model for youth program matching."""
    total_programs: int = Field(description="Total available programs")
    matched_count: int = Field(description="Number of matched programs")
    items: list[YouthProgramMatchItem] = Field(description="Matched programs sorted by score")
