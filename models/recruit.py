"""
Pydantic models for Recruit (채용) API responses.
"""

from pydantic import BaseModel, Field
from typing import Optional


class RecruitSearchRequest(BaseModel):
    """Request model for recruit notice search."""
    page: int = Field(default=1, ge=1, description="Page number (1-indexed)")
    page_size: int = Field(default=10, ge=1, le=100, description="Number of items per page")
    region: Optional[str] = Field(default=None, description="Region code (e.g., '11' for Seoul)")
    occupation_codes: Optional[list[str]] = Field(default=None, description="Occupation codes (e.g., ['023100', '021300'])")
    salary_type: Optional[str] = Field(default=None, description="Salary type: 'Y'=annual, 'M'=monthly, 'D'=daily, 'H'=hourly")
    min_salary: Optional[int] = Field(default=None, description="Minimum salary (in 10,000 KRW)")
    max_salary: Optional[int] = Field(default=None, description="Maximum salary (in 10,000 KRW)")
    education_code: Optional[str] = Field(default=None, description="Education level code")
    career_type: Optional[str] = Field(default=None, description="Career type: 'N'=entry level, 'E'=experienced, 'Z'=no preference")


class RecruitItem(BaseModel):
    """Single recruit notice item."""
    wanted_auth_no: str = Field(description="Unique job posting ID")
    company: str = Field(description="Company name")
    title: str = Field(description="Job title")
    region: str = Field(description="Work location")
    industry: Optional[str] = Field(default=None, description="Industry type")
    salary_type: Optional[str] = Field(default=None, description="Salary type code")
    salary_text: Optional[str] = Field(default=None, description="Human-readable salary range")
    min_salary: Optional[int] = Field(default=None, description="Minimum salary")
    max_salary: Optional[int] = Field(default=None, description="Maximum salary")
    employment_type: Optional[str] = Field(default=None, description="Employment type (정규직, 계약직, etc.)")
    education: Optional[str] = Field(default=None, description="Required education")
    career: Optional[str] = Field(default=None, description="Required career level")
    close_date: Optional[str] = Field(default=None, description="Application deadline")
    wanted_info_url: Optional[str] = Field(default=None, description="Job posting URL")
    mobile_url: Optional[str] = Field(default=None, description="Mobile URL")


class RecruitSearchResponse(BaseModel):
    """Response model for recruit notice search."""
    total: int = Field(description="Total number of matching jobs")
    page: int = Field(description="Current page number")
    page_size: int = Field(description="Items per page")
    items: list[RecruitItem] = Field(description="List of job postings")


class RecruitDetailResponse(BaseModel):
    """Response model for recruit notice detail."""
    wanted_auth_no: str = Field(description="Unique job posting ID")
    company: str = Field(description="Company name")
    title: str = Field(description="Job title")
    main_duties: Optional[str] = Field(default=None, description="Main job duties")
    requirements: Optional[str] = Field(default=None, description="Job requirements")
    preferred: Optional[str] = Field(default=None, description="Preferred qualifications")
    hiring_process: Optional[str] = Field(default=None, description="Hiring process description")
    region: Optional[str] = Field(default=None, description="Work location")
    work_type: Optional[str] = Field(default=None, description="Work schedule type")
    employment_type: Optional[str] = Field(default=None, description="Employment type")
    salary_text: Optional[str] = Field(default=None, description="Salary information")
    company_info: Optional[str] = Field(default=None, description="Company description")
    benefits: Optional[str] = Field(default=None, description="Benefits and perks")
