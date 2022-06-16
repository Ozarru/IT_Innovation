from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..config.database import get_db
from .. import models, schemas, utils, oauth2

router = APIRouter(prefix='/students', tags=['Students'])


@router.get('/', response_model=List[schemas.GenUserRes])
def get_students(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 20, offset: int = 0):
    if current_user.role_id == 1:
        students = db.query(models.User).filter(models.User.role_id == 4).all()
        # students = db.query(models.User).filter(models.User.role_id == 4).limit(limit).offset(offset).all()
        return students
    elif current_user.role_id == 2:
        school = db.query(models.School).filter(
            models.School.manager_id == current_user.id).first()
        if not school:
            print(school)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No school was found with you as the manager, hence no student too!")
        students = db.query(models.User).filter(
            models.User.role_id == 4, models.User.school == school).all()
        # models.User.role_id == 4,, models.User.school_id == current_school).limit(limit).offset(offset).all()
        if not students:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No Student was found!")
        return students
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.get('/{id}', response_model=schemas.GenUserRes)
def get_student(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    school = db.query(models.School).filter(
        models.School.manager_id == current_user.id).first()
    student = db.query(models.User).filter(
        models.User.role_id == 4, models.User.id == id).first()
    if not school:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No school was found with you as the manager, hence no student too!")
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No student with id: {id} was found!")
    if current_user.role_id != 1 and current_user.role_id != 2 and student.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
    return student


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.GenUserRes)
def create_students(user: schemas.GenUserCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    school = db.query(models.School).filter(
        models.School.manager_id == current_user.id).first()
    if current_user.role_id != 2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
    if not school:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail=f"Not allowed!!! You must create a school before adding students!")

    hashed_pass = utils.hash(user.password)
    user.password = hashed_pass
    new_user = models.User(role_id=4, school_id=school.id, **user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(school.id, new_user)
    return new_user


@router.post('/activate', status_code=status.HTTP_201_CREATED, response_model=schemas.StudentRes)
def activate_student(student: schemas.StudentActivate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    school = db.query(models.School).filter(
        models.School.manager_id == current_user.id).first()
    if current_user.role_id != 1 and current_user.role_id != 2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")
    elif not school:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail=f"Not allowed!!! You must create a school before activating students!")

    new_student = models.Student(**student.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    print(new_student)
    return new_student


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_student(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    school = db.query(models.School).filter(
        models.School.manager_id == current_user.id).first()
    student = db.query(models.User).filter(
        models.User.role_id == 4, models.User.id == id).first()
    if not school:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No school was found with you as the manager, hence no student too!")
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No student with id: {id} was found!")
    if current_user.role_id != 1 and 2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")

    student.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}')
def update_student(id: int, updated_student: schemas.GenUserCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    school = db.query(models.School).filter(
        models.School.manager_id == current_user.id).first()
    student = db.query(models.User).filter(
        models.User.role_id == 4, models.User.id == id).first()
    if not school:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No school was found with you as the manager, hence no student too!")
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"student with id: {id} was not found")
    if current_user.role_id != 1 and current_user.role_id != 2 and current_user.id != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")

    student.update(updated_student.dict(), synchronize_session=False)
    db.commit()
    return student
