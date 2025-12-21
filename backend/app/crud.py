from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import Optional, List
from app import models, schemas

def create_job(db: Session, job: schemas.JobCreate):
    db_job = models.Job(**job.model_dump())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def get_job(db: Session, job_id: int):
    return db.query(models.Job).filter(models.Job.id == job_id).first()

def get_job_by_job_id(db: Session, job_id: str):
    return db.query(models.Job).filter(models.Job.job_id == job_id).first()

def get_jobs(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    keyword: Optional[str] = None,
    location: Optional[str] = None,
    salary_min: Optional[int] = None,
    salary_max: Optional[int] = None,
    source: Optional[str] = None,
    experience: Optional[str] = None,
    education: Optional[str] = None
):
    query = db.query(models.Job)

    if keyword:
        query = query.filter(
            or_(
                models.Job.title.contains(keyword),
                models.Job.company.contains(keyword),
                models.Job.description.contains(keyword)
            )
        )

    if location:
        query = query.filter(models.Job.location.contains(location))

    if salary_min is not None:
        query = query.filter(models.Job.salary_min >= salary_min)

    if salary_max is not None:
        query = query.filter(models.Job.salary_max <= salary_max)

    if source:
        query = query.filter(models.Job.source == source)

    if experience:
        query = query.filter(models.Job.experience.contains(experience))

    if education:
        query = query.filter(models.Job.education.contains(education))

    query = query.order_by(models.Job.created_at.desc())

    return query.offset(skip).limit(limit).all()

def get_jobs_count(
    db: Session,
    keyword: Optional[str] = None,
    location: Optional[str] = None,
    salary_min: Optional[int] = None,
    salary_max: Optional[int] = None,
    source: Optional[str] = None,
    experience: Optional[str] = None,
    education: Optional[str] = None
):
    query = db.query(models.Job)

    if keyword:
        query = query.filter(
            or_(
                models.Job.title.contains(keyword),
                models.Job.company.contains(keyword),
                models.Job.description.contains(keyword)
            )
        )

    if location:
        query = query.filter(models.Job.location.contains(location))

    if salary_min is not None:
        query = query.filter(models.Job.salary_min >= salary_min)

    if salary_max is not None:
        query = query.filter(models.Job.salary_max <= salary_max)

    if source:
        query = query.filter(models.Job.source == source)

    if experience:
        query = query.filter(models.Job.experience.contains(experience))

    if education:
        query = query.filter(models.Job.education.contains(education))

    return query.count()

def update_job(db: Session, job_id: int, job_update: schemas.JobUpdate):
    db_job = get_job(db, job_id)
    if db_job:
        update_data = job_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_job, key, value)
        db.commit()
        db.refresh(db_job)
    return db_job

def delete_job(db: Session, job_id: int):
    db_job = get_job(db, job_id)
    if db_job:
        db.delete(db_job)
        db.commit()
        return True
    return False

def create_favorite(db: Session, favorite: schemas.FavoriteCreate):
    db_favorite = models.Favorite(**favorite.model_dump())
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    return db_favorite

def get_favorite(db: Session, favorite_id: int):
    return db.query(models.Favorite).filter(models.Favorite.id == favorite_id).first()

def get_favorites(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Favorite).order_by(models.Favorite.created_at.desc()).offset(skip).limit(limit).all()

def get_favorite_by_job_id(db: Session, job_id: int):
    return db.query(models.Favorite).filter(models.Favorite.job_id == job_id).first()

def update_favorite(db: Session, favorite_id: int, favorite_update: schemas.FavoriteUpdate):
    db_favorite = get_favorite(db, favorite_id)
    if db_favorite:
        update_data = favorite_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_favorite, key, value)
        db.commit()
        db.refresh(db_favorite)
    return db_favorite

def delete_favorite(db: Session, favorite_id: int):
    db_favorite = get_favorite(db, favorite_id)
    if db_favorite:
        db.delete(db_favorite)
        db.commit()
        return True
    return False
