from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..config.database import get_db
from app import models, schemas, utils

router = APIRouter(prefix='/students', tags=['Users'])


@router.get('/', response_model=List[schemas.UserRes])
def get_users(db: Session = Depends(get_db), limit: int = 0, skip: int = 0, search: Optional[str] = ""):
    users = db.query(models.User).all()  # gets all available results
    # users = db.query(models.User).limit(limit).all()       #limits to x number of results
    # users = db.query(models.User).offset(skip).all()       #skips x number of results
    # users = db.query(models.User).filter(
    #     models.User.name.contains(search)).limit(limit).offset(skip).all()
    return users


@router.get('/{id}', response_model=schemas.UserRes)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} was not found")
    return user


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserRes)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_pass = utils.hash(user.password)
    user.password = hashed_pass
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(new_user)
    return new_user


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} was not found")
    user_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
