
from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..config.database import get_db
from .. import models, schemas, oauth2

router = APIRouter(prefix='/students', tags=['Students'])


@router.get('/', response_model=List[schemas.StudentRes])
def get_students(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 20):
    if current_user.is_super_admin:
        students = db.query(models.Student).all()
        return students
    elif current_user.is_admin:
        student_query = db.query(models.Student).filter(
            models.Student.school_id == current_user.school.id)
        students = student_query.all()
        if not students:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No Student was found")
        return students
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")


@router.get('/{id}', response_model=schemas.StudentRes)
def get_student(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    student_query = db.query(models.Student).filter(
        models.Student.id == id)
    student = student_query.first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Education stage with id: {id} was not found")
    if student.school.admin_id != current_user.id and current_user.is_super_admin != True:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")
    return student


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.StudentRes)
def create_students(student: schemas.StudentCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")
    new_student = models.Student(
        school_id=current_user.school.id, **student.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_student(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    student_query = db.query(models.Student).filter(
        models.Student.id == id)
    student = student_query.first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"school with id: {id} was not found")
    if student.school.admin_id != current_user.id and current_user.is_super_admin != True:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")

    student_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}')
def update_student(id: int, updated_student: schemas.StudentCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    student_query = db.query(models.Student).filter(
        models.Student.id == id)
    student = student_query.first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"school with id: {id} was not found")
    if student.school.admin_id != current_user.id and current_user.is_super_admin != True:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")

    student_query.update(updated_student.dict(), synchronize_session=False)
    db.commit()
    return student
