
from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ..models import gen_models
from ..config.database import get_db
from .. import gen_schemas, oauth2

router = APIRouter(prefix='/edu_stages', tags=['Education Stages'])


@router.get('/', response_model=List[gen_schemas.EduStageRes])
def get_edu_stages(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 20):
    if current_user.role_id == 1:
        edu_stages = db.query(gen_models.EduStage).all()
        return edu_stages
    elif current_user.role_id == 2:
        edu_stages = db.query(gen_models.EduStage).filter(
            gen_models.EduStage.school.manager_id == current_user.id).all()
        if not edu_stages:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No Education stage was found")
        return edu_stages
    else:
        edu_stages = db.query(gen_models.EduStage).filter(
            gen_models.EduStage.school_id == current_user.school_id).all()
        if not edu_stages:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No Education stage was found")
        return edu_stages
    # else:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail=f"Forbidden!!! Insufficient authentication credentials.")


@router.get('/{id}', response_model=gen_schemas.EduStageRes)
def get_edu_stage(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    edu_stage_query = db.query(gen_models.EduStage).filter(
        gen_models.EduStage.id == id)
    edu_stage = edu_stage_query.first()
    if not edu_stage:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Education stage with id: {id} was not found")
    if current_user.role_id == 1 != True and edu_stage.school.manager_id != current_user.id and edu_stage.school_id != current_user.school_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")
    return edu_stage


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=gen_schemas.EduStageRes)
def create_edu_stages(edu_stage: gen_schemas.EduStageCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if not current_user.role_id == 2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")
    new_edu_stage = gen_models.EduStage(
        school_id=current_user.school.id, **edu_stage.dict())
    db.add(new_edu_stage)
    db.commit()
    db.refresh(new_edu_stage)
    return new_edu_stage


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_edu_stage(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    edu_stage_query = db.query(gen_models.EduStage).filter(
        gen_models.EduStage.id == id)
    edu_stage = edu_stage_query.first()
    if not edu_stage:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"school with id: {id} was not found")
    if current_user.role_id == 1 != True and edu_stage.school.manager_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")

    edu_stage_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}')
def update_edu_stage(id: int, updated_edu_stage: gen_schemas.EduStageCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    edu_stage_query = db.query(gen_models.EduStage).filter(
        gen_models.EduStage.id == id)
    edu_stage = edu_stage_query.first()
    if not edu_stage:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"school with id: {id} was not found")
    if current_user.role_id == 1 != True and edu_stage.school.manager_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")

    edu_stage_query.update(updated_edu_stage.dict(), synchronize_session=False)
    db.commit()
    return edu_stage
