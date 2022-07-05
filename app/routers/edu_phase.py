
from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..config.database import get_db
from .. import gen_schemas, models, oauth2

router = APIRouter(prefix='/edu_phases', tags=['Education Phases'])


@router.get('/', response_model=List[gen_schemas.EduPhaseRes])
def get_edu_phases(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 20):
    if current_user.role_id == 1:
        edu_phases = db.query(models.EduPhase).all()
        return edu_phases
    elif current_user.role_id == 2:
        edu_phases = db.query(models.EduPhase).filter(
            models.EduPhase.edu_stage.school.manager_id == current_user.id).all()
        if not edu_phases:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No Education phase was found")
        return edu_phases
    else:
        edu_phases = db.query(models.EduStage).filter(
            models.EduPhase.edu_stage.school_id == current_user.school_id).all()
        if not edu_phases:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No Education stage was found")
        return edu_phases
    # else:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail=f"Forbidden!!! Insufficient authentication credentials.")


@router.get('/{id}', response_model=gen_schemas.EduPhaseRes)
def get_edu_phase(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    edu_phase = db.query(models.EduPhase).filter(
        models.EduPhase.id == id).first()
    if not edu_phase:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Education phase with id: {id} was not found")
    if current_user.role_id == 1 != True and edu_phase.edu_stage.school.manager_id != current_user.id and edu_phase.edu_stage.school_id != current_user.school_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")
    return edu_phase


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=gen_schemas.EduPhaseRes)
def create_edu_phases(edu_phase: gen_schemas.EduPhaseCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    if not current_user.role_id == 2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")
    new_edu_phase = models.EduPhase(**edu_phase.dict())
    db.add(new_edu_phase)
    db.commit()
    db.refresh(new_edu_phase)
    return new_edu_phase


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_edu_phase(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    edu_phase_query = db.query(models.EduPhase).filter(
        models.EduPhase.id == id)
    edu_phase = edu_phase_query.first()
    if not edu_phase:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"school with id: {id} was not found")
    if current_user.role_id == 1 != True and edu_phase.edu_stage.school.manager_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")

    edu_phase_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}')
def update_edu_phase(id: int, updated_edu_phase: gen_schemas.EduPhaseCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    edu_phase_query = db.query(models.EduPhase).filter(
        models.EduPhase.id == id)
    edu_phase = edu_phase_query.first()
    if not edu_phase:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"school with id: {id} was not found")
    if current_user.role_id == 1 != True and edu_phase.edu_stage.school.manager_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")

    edu_phase_query.update(updated_edu_phase.dict(), synchronize_session=False)
    db.commit()
    return edu_phase
