
from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..config.database import get_db
from .. import models, schemas, oauth2

router = APIRouter(prefix='/edu_stages', tags=['Education Stages'])


@router.get('/', response_model=List[schemas.EduStageRes])
def get_edu_stages(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 20):
    if current_user.is_super_admin:
        edu_stages = db.query(models.EduStage).all()
        return edu_stages
    elif current_user.is_admin:
        edu_stage_query = db.query(models.EduStage).filter(
            models.EduStage.school_id == current_user.school.id)
        edu_stages = edu_stage_query.all()
        if not edu_stages:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No Education stage was found")
        return edu_stages
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")


@router.get('/{id}', response_model=schemas.EduStageRes)
def get_edu_stage(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    edu_stage_query = db.query(models.EduStage).filter(
        models.EduStage.id == id)
    edu_stage = edu_stage_query.first()
    if not edu_stage:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Education stage with id: {id} was not found")
    if edu_stage.school.admin_id != current_user.id and current_user.is_super_admin != True:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")
    return edu_stage


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.EduStageRes)
def create_edu_stages(edu_stage: schemas.EduStageCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")
    new_edu_stage = models.EduStage(
        school_id=current_user.school.id, **edu_stage.dict())
    db.add(new_edu_stage)
    db.commit()
    db.refresh(new_edu_stage)
    return new_edu_stage


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_edu_stage(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    edu_stage_query = db.query(models.EduStage).filter(
        models.EduStage.id == id)
    edu_stage = edu_stage_query.first()
    if not edu_stage:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"school with id: {id} was not found")
    if edu_stage.school.admin_id != current_user.id and current_user.is_super_admin != True:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")

    edu_stage_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}')
def update_edu_stage(id: int, updated_edu_stage: schemas.EduStageCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    edu_stage_query = db.query(models.EduStage).filter(
        models.EduStage.id == id)
    edu_stage = edu_stage_query.first()
    if not edu_stage:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"school with id: {id} was not found")
    if edu_stage.school.admin_id != current_user.id and current_user.is_super_admin != True:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")

    edu_stage_query.update(updated_edu_stage.dict(), synchronize_session=False)
    db.commit()
    return edu_stage
