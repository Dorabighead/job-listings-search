from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.FavoriteWithJob])
def get_favorites(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    favorites = crud.get_favorites(db=db, skip=skip, limit=limit)
    return favorites

@router.get("/{favorite_id}", response_model=schemas.FavoriteWithJob)
def get_favorite(favorite_id: int, db: Session = Depends(get_db)):
    db_favorite = crud.get_favorite(db=db, favorite_id=favorite_id)
    if db_favorite is None:
        raise HTTPException(status_code=404, detail="收藏不存在")
    return db_favorite

@router.post("/", response_model=schemas.Favorite)
def create_favorite(favorite: schemas.FavoriteCreate, db: Session = Depends(get_db)):
    db_job = crud.get_job(db=db, job_id=favorite.job_id)
    if not db_job:
        raise HTTPException(status_code=404, detail="职位不存在")

    existing_favorite = crud.get_favorite_by_job_id(db=db, job_id=favorite.job_id)
    if existing_favorite:
        raise HTTPException(status_code=400, detail="该职位已收藏")

    return crud.create_favorite(db=db, favorite=favorite)

@router.put("/{favorite_id}", response_model=schemas.Favorite)
def update_favorite(favorite_id: int, favorite_update: schemas.FavoriteUpdate, db: Session = Depends(get_db)):
    db_favorite = crud.update_favorite(db=db, favorite_id=favorite_id, favorite_update=favorite_update)
    if db_favorite is None:
        raise HTTPException(status_code=404, detail="收藏不存在")
    return db_favorite

@router.delete("/{favorite_id}")
def delete_favorite(favorite_id: int, db: Session = Depends(get_db)):
    success = crud.delete_favorite(db=db, favorite_id=favorite_id)
    if not success:
        raise HTTPException(status_code=404, detail="收藏不存在")
    return {"message": "取消收藏成功"}
