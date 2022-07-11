
from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ..models import gen_models
from ..config.database import get_db
from .. import gen_schemas, oauth2

router = APIRouter(prefix='/schools', tags=['Schools'])


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[gen_schemas.SchoolRes])
def get_schools(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 50, offset: int = 0):
    if current_user.role_id == 1:
        schools = db.query(gen_models.School).limit(limit).offset(offset).all()
        return schools
    elif current_user.role_id == 2:
        schools = db.query(gen_models.School).filter(
            gen_models.School.manager_id == current_user.id).all()
        if not schools:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No school was found with you as the manager!")
        return schools
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=gen_schemas.SchoolRes)
def get_school(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    school = db.query(gen_models.School).filter(gen_models.School.id == id).first()
    if not school:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No school with id: {id} was found")
    if current_user.role_id != 1 and school.manager_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")
    return school


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=gen_schemas.SchoolRes)
def create_schools(school: gen_schemas.SchoolCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id != 2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")
    school_exist = db.query(gen_models.School).filter(
        gen_models.School.manager_id == current_user.id).first()
    if school_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Conflict!!! Admin already has a school, therefore cannot create another school.")

    new_school = gen_models.School(
        manager_id=current_user.id, **school.dict())
    db.add(new_school)
    db.commit()
    db.refresh(new_school)
    return new_school


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_school(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    school = db.query(gen_models.School).filter(gen_models.School.id == id).first()
    if not school:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No school with id: {id} was found")
    if current_user.role_id != 1 and school.manager_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")

    school.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}')
def update_school(id: int, updated_school: gen_schemas.SchoolCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    school = db.query(gen_models.School).filter(gen_models.School.id == id).first()
    if not school:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No school with id: {id} was found")
    if current_user.role_id != 1 and school.manager_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")

    school.update(updated_school.dict(), synchronize_session=False)
    db.commit()
    return school
