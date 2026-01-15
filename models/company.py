"""
Pydantic models for Company (기업) API responses.
"""

from pydantic import BaseModel, Field
from typing import Optional


class CompanySearchRequest(BaseModel):
    """Request model for company search."""
    company_type_codes: Optional[list[str]] = Field(default=None, description="Company type codes (e.g., ['10', '20', '40'])")
    company_name: Optional[str] = Field(default=None, description="Company name keyword")
    page: int = Field(default=1, ge=1, description="Page number")
    page_size: int = Field(default=10, ge=1, le=100, description="Items per page")
    sort_field: Optional[str] = Field(default=None, description="Sort field")
    sort_order: Optional[str] = Field(default="DESC", description="Sort order (ASC/DESC)")


class CompanyItem(BaseModel):
    """Single company item."""
    company_id: str = Field(description="Company ID")
    company_name: str = Field(description="Company name")
    company_type: Optional[str] = Field(default=None, description="Company type")
    business_no: Optional[str] = Field(default=None, description="Business registration number")
    industry: Optional[str] = Field(default=None, description="Industry type")
    address: Optional[str] = Field(default=None, description="Company address")
    homepage: Optional[str] = Field(default=None, description="Company website")
    main_business: Optional[str] = Field(default=None, description="Main business description")
    employee_count: Optional[int] = Field(default=None, description="Number of employees")
    revenue: Optional[str] = Field(default=None, description="Annual revenue")
    latitude: Optional[float] = Field(default=None, description="Latitude")
    longitude: Optional[float] = Field(default=None, description="Longitude")


class CompanySearchResponse(BaseModel):
    """Response model for company search."""
    total: int = Field(description="Total number of matching companies")
    page: int = Field(description="Current page number")
    page_size: int = Field(description="Items per page")
    items: list[CompanyItem] = Field(description="List of companies")
