
from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..config.database import get_db
from .. import gen_schemas, models, oauth2

router = APIRouter(prefix='/subjects', tags=['Subjects'])


@router.get('/', response_model=List[gen_schemas.SubjectRes])
def get_subjects(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 20):
    if current_user.role_id == 1:
        subjects = db.query(models.Subject).all()
        return subjects
    elif current_user.role_id == 2:
        subjects = db.query(models.Subject).filter(
            models.Subject.edu_phase.edu_stage.school.manager_id == current_user.id).all()
        if not subjects:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No Education phase was found")
        return subjects
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")


@router.get('/{id}', response_model=gen_schemas.SubjectRes)
def get_subject(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    subject = db.query(models.Subject).filter(
        models.Subject.id == id).first()
    if not subject:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Education phase with id: {id} was not found")
    if current_user.role_id == 1 != True and subject.edu_phase.edu_stage.school.manager_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")
    return subject


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=gen_schemas.SubjectRes)
def create_subjects(subject: gen_schemas.SubjectCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    if not current_user.role_id == 2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")
    new_subject = models.Subject(**subject.dict())
    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)
    return new_subject


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_subject(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    subject_query = db.query(models.Subject).filter(
        models.Subject.id == id)
    subject = subject_query.first()
    if not subject:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"school with id: {id} was not found")
    if current_user.role_id == 1 != True and subject.edu_phase.edu_stage.school.manager_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")

    subject_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}')
def update_subject(id: int, updated_subject: gen_schemas.SubjectCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    subject_query = db.query(models.Subject).filter(
        models.Subject.id == id)
    subject = subject_query.first()
    if not subject:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"school with id: {id} was not found")
    if current_user.role_id == 1 != True and subject.edu_phase.edu_stage.school.manager_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")

    subject_query.update(updated_subject.dict(), synchronize_session=False)
    db.commit()
    return subject
