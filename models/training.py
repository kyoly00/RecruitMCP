"""
Pydantic models for Training Course (훈련과정) API responses.
"""

from pydantic import BaseModel, Field
from typing import Optional


class TrainingSearchRequest(BaseModel):
    """Request model for training course search."""
    page: int = Field(default=1, ge=1, description="Page number (1-indexed)")
    page_size: int = Field(default=20, ge=1, le=100, description="Items per page")
    start_date: str = Field(description="Training start date from (YYYYMMDD)")
    end_date: str = Field(description="Training start date to (YYYYMMDD)")
    area1: Optional[str] = Field(default=None, description="Region code level 1 (e.g., '11' for Seoul)")
    area2: Optional[str] = Field(default=None, description="Region code level 2")
    ncs1: Optional[str] = Field(default=None, description="NCS major category code")
    ncs2: Optional[str] = Field(default=None, description="NCS middle category code")
    course_type: Optional[str] = Field(default=None, description="Training type code (e.g., 'C0061S' for K-Digital)")
    keyword: Optional[str] = Field(default=None, description="Course name keyword")
    provider_name: Optional[str] = Field(default=None, description="Training provider name")


class TrainingItem(BaseModel):
    """Single training course item."""
    course_id: str = Field(description="Course ID (TRPR_ID)")
    course_round: str = Field(description="Course round number")
    title: str = Field(description="Course title")
    provider_name: str = Field(description="Training provider name")
    address: Optional[str] = Field(default=None, description="Provider address")
    phone: Optional[str] = Field(default=None, description="Contact phone")
    start_date: str = Field(description="Training start date")
    end_date: str = Field(description="Training end date")
    ncs_code: Optional[str] = Field(default=None, description="NCS classification code")
    ncs_name: Optional[str] = Field(default=None, description="NCS classification name")
    tuition: Optional[int] = Field(default=None, description="Total tuition (KRW)")
    support_amount: Optional[int] = Field(default=None, description="Government support amount (KRW)")
    real_cost: Optional[int] = Field(default=None, description="Actual training cost (KRW)")
    employment_rate_3m: Optional[str] = Field(default=None, description="3-month employment rate (%)")
    satisfaction_score: Optional[str] = Field(default=None, description="Trainee satisfaction score")
    org_id: Optional[str] = Field(default=None, description="Training organization ID")


class TrainingSearchResponse(BaseModel):
    """Response model for training course search."""
    total: int = Field(description="Total number of matching courses")
    page: int = Field(description="Current page number")
    page_size: int = Field(description="Items per page")
    items: list[TrainingItem] = Field(description="List of training courses")


class TrainingDetailRequest(BaseModel):
    """Request model for training course detail."""
    course_id: str = Field(description="Course ID (TRPR_ID)")
    course_round: str = Field(description="Course round number")
    org_id: str = Field(description="Training organization ID")


class TrainingDetailResponse(BaseModel):
    """Response model for training course detail."""
    course_id: str = Field(description="Course ID")
    course_round: str = Field(description="Course round")
    course_name: str = Field(description="Course name")
    org_name: str = Field(description="Training organization name")
    org_homepage: Optional[str] = Field(default=None, description="Organization website")
    org_address: Optional[str] = Field(default=None, description="Organization address")
    org_tel: Optional[str] = Field(default=None, description="Organization phone")
    ncs_code: Optional[str] = Field(default=None, description="NCS code")
    ncs_name: Optional[str] = Field(default=None, description="NCS name")
    total_days: Optional[int] = Field(default=None, description="Total training days")
    total_hours: Optional[int] = Field(default=None, description="Total training hours")
    tuition: Optional[int] = Field(default=None, description="Tuition (KRW)")
    support_amount: Optional[int] = Field(default=None, description="Support amount (KRW)")
    target: Optional[str] = Field(default=None, description="Target trainees")
    is_k_digital: bool = Field(default=False, description="Is K-Digital Training")
    curriculum: Optional[str] = Field(default=None, description="Curriculum summary")
