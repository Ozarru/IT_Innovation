from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..config.database import get_db
from app import gen_schemas, models, oauth2

router = APIRouter(prefix='/grades', tags=['Grades'])


@router.get('/', response_model=List[gen_schemas.GradeRes])
def get_grades(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    grades = db.query(models.grade).filter(
        models.grade.id == current_user.school_id).all()
    return grades


@router.get('/{id}', response_model=List[gen_schemas.GradeRes])
def get_grade(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    grade = db.query(models.grade).filter(
        models.grade.id == id).first()
    if not grade:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"grade with id: {id} was not found")

    if grade.school_id != current_user.school_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Not authorized to perform this action")

    return grade


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=gen_schemas.GradeRes)
def create_grades(grade: gen_schemas.GradeCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    new_grade = models.grade(
        school_id=current_user.school.id**grade.dict())
    db.add(new_grade)
    db.commit()
    db.refresh(new_grade)
    print(new_grade)
    return new_grade


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_grade(id: int, db: Session = Depends(get_db)):
    grade_query = db.query(models.grade).filter(
        models.grade.id == id)
    grade = grade_query.first()
    if grade == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"grade with id: {id} was not found")
    grade_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}')
def update_grade(id: int, updated_grade: gen_schemas.GradeCreate, db: Session = Depends(get_db)):
    grade_query = db.query(models.grade).filter(
        models.grade.id == id)
    grade = grade_query.first()
    if grade == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"grade with id: {id} was not found")
    grade_query.update(updated_grade.dict(), synchronize_session=False)
    db.commit()
    return grade
