
from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..config.database import get_db
from .. import models, schemas, oauth2

router = APIRouter(prefix='/schools', tags=['Schools'])


@router.get('/', response_model=List[schemas.SchoolRes])
def get_schools(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 20):
    if current_user.is_super_admin != True:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Not Authorized to perform requested action")
    # schools = db.query(models.School).filter(models.School.admin_id == current_user.id).all()
    # schools = db.query(models.School).all()
    schools = db.query(models.School).limit(limit).all()
    return schools


@router.get('/{id}', response_model=schemas.SchoolRes)
def get_school(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    school_query = db.query(models.School).filter(models.School.id == id)
    school = school_query.first()
    if not school:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"school with id: {id} was not found")
    if school.admin_id != current_user.id and current_user.is_super_admin != True:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Not Authorized to perform requested action")
    return school


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.SchoolRes)
def create_schools(school: schemas.SchoolCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    new_school = models.School(admin_id=current_user.id, **school.dict())
    db.add(new_school)
    db.commit()
    db.refresh(new_school)
    return new_school


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_school(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    school_query = db.query(models.School).filter(models.School.id == id)
    school = school_query.first()
    if not school:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"school with id: {id} was not found")
    if school.admin_id != current_user.id and current_user.is_super_admin != True:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Not Authorized to perform requested action")

    school_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}')
def update_school(id: int, updated_school: schemas.SchoolCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    school_query = db.query(models.School).filter(models.School.id == id)
    school = school_query.first()
    if not school:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"school with id: {id} was not found")
    if school.admin_id != current_user.id and current_user.is_super_admin != True:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Not Authorized to perform requested action")

    school_query.update(updated_school.dict(), synchronize_session=False)
    db.commit()
    return school
