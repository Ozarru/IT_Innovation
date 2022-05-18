from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..config.database import get_db
from app import models, schemas

router = APIRouter(prefix='/courses', tags=['Courses'])


@router.get('/')
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(models.Course).all()
    return courses


@router.get('/{id}')
def get_course(id: int, db: Session = Depends(get_db)):
    courses = db.query(models.Course).filter(
        models.Course.id == id).first()
    if not courses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"course with id: {id} was not found")
    return courses


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.CourseRes)
def create_courses(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    new_course = models.Course(**course.dict())
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    print(new_course)
    return new_course


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_course(id: int, db: Session = Depends(get_db)):
    courses_query = db.query(models.Course).filter(
        models.Course.id == id)
    course = courses_query.first()
    if course == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"course with id: {id} was not found")
    courses_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}')
def update_course(id: int, updated_course: schemas.CourseCreate, db: Session = Depends(get_db)):
    courses_query = db.query(models.Course).filter(
        models.Course.id == id)
    course = courses_query.first()
    if course == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"course with id: {id} was not found")
    courses_query.update(updated_course.dict(), synchronize_session=False)
    db.commit()
    return course
