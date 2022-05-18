from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..config.database import get_db
from app import models, schemas, oauth2

router = APIRouter(prefix='/classrooms', tags=['Classrooms'])


@router.get('/', response_model=List[schemas.ClassroomRes])
def get_classrooms(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    classrooms = db.query(models.Classroom).filter(
        models.Classroom.id == current_user.school_id).all()
    return classrooms


@router.get('/{id}')
def get_classroom(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    classroom = db.query(models.Classroom).filter(
        models.Classroom.id == id).first()
    if not classroom:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"classroom with id: {id} was not found")

    if classroom.school_id != current_user.school_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Not authorized to perform this action")

    return classroom


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ClassroomRes)
def create_classrooms(classroom: schemas.ClassroomCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    new_classroom = models.Classroom(
        school_id=current_user.school.id**classroom.dict())
    db.add(new_classroom)
    db.commit()
    db.refresh(new_classroom)
    print(new_classroom)
    return new_classroom


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_classroom(id: int, db: Session = Depends(get_db)):
    classroom_query = db.query(models.Classroom).filter(
        models.Classroom.id == id)
    classroom = classroom_query.first()
    if classroom == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"classroom with id: {id} was not found")
    classroom_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}')
def update_classroom(id: int, updated_classroom: schemas.ClassroomCreate, db: Session = Depends(get_db)):
    classroom_query = db.query(models.Classroom).filter(
        models.Classroom.id == id)
    classroom = classroom_query.first()
    if classroom == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"classroom with id: {id} was not found")
    classroom_query.update(updated_classroom.dict(), synchronize_session=False)
    db.commit()
    return classroom
