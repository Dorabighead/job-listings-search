from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional, List
from app import crud, schemas
from app.database import get_db
import pandas as pd
import io

router = APIRouter()

@router.get("/", response_model=dict)
def get_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    keyword: Optional[str] = None,
    location: Optional[str] = None,
    salary_min: Optional[int] = None,
    salary_max: Optional[int] = None,
    source: Optional[str] = None,
    experience: Optional[str] = None,
    education: Optional[str] = None,
    db: Session = Depends(get_db)
):
    jobs = crud.get_jobs(
        db=db,
        skip=skip,
        limit=limit,
        keyword=keyword,
        location=location,
        salary_min=salary_min,
        salary_max=salary_max,
        source=source,
        experience=experience,
        education=education
    )

    total = crud.get_jobs_count(
        db=db,
        keyword=keyword,
        location=location,
        salary_min=salary_min,
        salary_max=salary_max,
        source=source,
        experience=experience,
        education=education
    )

    return {
        "total": total,
        "page": skip // limit + 1,
        "limit": limit,
        "jobs": jobs
    }

@router.get("/{job_id}", response_model=schemas.Job)
def get_job(job_id: int, db: Session = Depends(get_db)):
    db_job = crud.get_job(db=db, job_id=job_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="职位不存在")
    return db_job

@router.post("/", response_model=schemas.Job)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    db_job = crud.get_job_by_job_id(db=db, job_id=job.job_id)
    if db_job:
        raise HTTPException(status_code=400, detail="该职位ID已存在")
    return crud.create_job(db=db, job=job)

@router.put("/{job_id}", response_model=schemas.Job)
def update_job(job_id: int, job_update: schemas.JobUpdate, db: Session = Depends(get_db)):
    db_job = crud.update_job(db=db, job_id=job_id, job_update=job_update)
    if db_job is None:
        raise HTTPException(status_code=404, detail="职位不存在")
    return db_job

@router.delete("/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    success = crud.delete_job(db=db, job_id=job_id)
    if not success:
        raise HTTPException(status_code=404, detail="职位不存在")
    return {"message": "删除成功"}

@router.get("/export/excel")
def export_jobs_excel(
    keyword: Optional[str] = None,
    location: Optional[str] = None,
    salary_min: Optional[int] = None,
    salary_max: Optional[int] = None,
    source: Optional[str] = None,
    db: Session = Depends(get_db)
):
    jobs = crud.get_jobs(
        db=db,
        skip=0,
        limit=10000,
        keyword=keyword,
        location=location,
        salary_min=salary_min,
        salary_max=salary_max,
        source=source
    )

    data = []
    for job in jobs:
        data.append({
            "职位ID": job.job_id,
            "职位名称": job.title,
            "公司": job.company,
            "最低薪资": job.salary_min,
            "最高薪资": job.salary_max,
            "地点": job.location,
            "经验要求": job.experience,
            "学历要求": job.education,
            "工作类型": job.job_type,
            "来源": job.source,
            "链接": job.url,
            "创建时间": job.created_at
        })

    df = pd.DataFrame(data)

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='职位信息')

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=jobs.xlsx"}
    )
