from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app.models import gen_models
from ..config.database import get_db
from app import func_schemas, oauth2

router = APIRouter(prefix='/exams', tags=['Exams'])


@router.get('/', response_model=List[func_schemas.ExamRes])
def get_exams(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 0, offset: int = 0):
    if current_user.role_id == 1:
        exams = db.query(gen_models.Exam).all()
        return exams

    elif current_user.role_id == 2:
        school = db.query(gen_models.School).filter(
            gen_models.School.manager_id == current_user.id).first()
        if not school:
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                                detail=f"No school was found with you as the manager, hence no exams too!")
        exams = db.query(gen_models.Exam).filter(
            gen_models.Exam.school_id == school.id).all()
        if not exams:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No exam was found!")
        return exams

    elif current_user:
        exams = db.query(gen_models.Exam).filter(
            gen_models.Exam.school_id == current_user.school_id).all()
        return exams

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.get('/{id}', response_model=func_schemas.ExamRes)
def get_exam(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    exam = db.query(gen_models.Exam).filter(
        gen_models.Exam.id == id).first()

    if current_user.role_id == 1:
        return exam

    elif current_user.role_id == 2:

        school = db.query(gen_models.School).filter(
            gen_models.School.manager_id == current_user.id).first()
        if not school:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No school was found with you as the manager, hence no exam too!")

        exam = db.query(gen_models.Exam).join(gen_models.School).filter(
            gen_models.Exam.school_id == school.id, gen_models.Exam.id == id).first()
        if not exam:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No exam with id: {id} was found in your school!")
        else:
            return exam

    elif current_user:
        school = db.query(gen_models.School).filter(
            gen_models.School.id == current_user.school_id).first()
        if not school:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"You do not belong to a school, so you cannot see exams!")

        exam = db.query(gen_models.Exam).join(gen_models.School).filter(
            gen_models.Clase.school.id == school.id, gen_models.Exam.id == id).first()
        if not exam:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No exam with id: {id} was found in your school!")
        else:
            return exam

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=func_schemas.ExamRes)
def create_exams(exam: func_schemas.ExamCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id != 2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
    school = db.query(gen_models.School).filter(
        gen_models.School.manager_id == current_user.id).first()
    if not school:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail=f"Not allowed!!! You must create a school before adding exams!")

    new_exam = gen_models.Exam(
        school_id=school.id, **exam.dict())
    db.add(new_exam)
    db.commit()
    db.refresh(new_exam)
    print(new_exam)
    return new_exam


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_exam(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id == 2:
        exam = db.query(gen_models.Exam).filter(gen_models.Exam.id == id).first()
        if exam == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"exam with id: {id} was not found")

        exam.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.put('/{id}')
def update_exam(id: int, updated_exam: func_schemas.ExamCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id == 2:
        exam = db.query(gen_models.Exam).filter(gen_models.Exam.id == id).first()
        if exam == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"exam with id: {id} was not found")

        exam.update(updated_exam.dict(), synchronize_session=False)
        db.commit()
        return exam

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
