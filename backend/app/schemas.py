from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class JobBase(BaseModel):
    job_id: str
    title: str
    company: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    location: Optional[str] = None
    experience: Optional[str] = None
    education: Optional[str] = None
    job_type: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    welfare: Optional[str] = None
    source: str
    url: Optional[str] = None

class JobCreate(JobBase):
    pass

class JobUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    location: Optional[str] = None
    experience: Optional[str] = None
    education: Optional[str] = None
    job_type: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    welfare: Optional[str] = None

class Job(JobBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class FavoriteBase(BaseModel):
    job_id: int
    note: Optional[str] = None

class FavoriteCreate(FavoriteBase):
    pass

class FavoriteUpdate(BaseModel):
    note: Optional[str] = None

class Favorite(FavoriteBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class FavoriteWithJob(Favorite):
    job: Job

class ScraperRequest(BaseModel):
    source: str = Field(..., description="boss | zhaopin | 51job | lagou | all")
    keyword: str = Field(..., description="搜索关键词，如：Python")
    location: Optional[str] = Field(None, description="工作地点，如：北京")
    pages: Optional[int] = Field(1, description="爬取页数", ge=1, le=10)

class ScraperResponse(BaseModel):
    status: str
    message: str
    jobs_count: Optional[int] = None
