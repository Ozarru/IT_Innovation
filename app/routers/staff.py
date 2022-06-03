
from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..config.database import get_db
from .. import models, schemas, utils, oauth2

router = APIRouter(prefix='/staff', tags=['Staff'])


@router.get('/', response_model=List[schemas.StaffRes])
def get_all_staff(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 20, offset: int = 0):
    if current_user.role_id == 1:
        staff = db.query(models.User).filter(models.User.role_id == 4).all()
        # staff = db.query(models.User).filter(models.User.role_id == 4).limit(limit).offset(offset).all()
        return staff
    elif current_user.role_id == 2:
        school = db.query(models.School).filter(
            models.School.manager_id == current_user.id).first()
        staff = db.query(models.User).filter(
            models.User.role_id == 3,  models.User.school_id == school.id).all()
        # models.User.role_id == 3, models.User.school_id == current_school).limit(limit).offset(offset).all()
        if not school:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No school was found with you as the manager!")
        if not staff:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No staff was found!")
        return staff
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.get('/{id}', response_model=schemas.StaffRes)
def get_one_staff(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    school = db.query(models.School).filter(
        models.School.manager_id == current_user.id).first()
    staff = db.query(models.User).filter(
        models.User.role_id == 3, models.User.id == id).first()
    if not school:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No school was found with you as the manager!")
    if not staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No staff with id: {id} was found!")
    if current_user.role_id != 1 and current_user.role_id != 2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
    return staff


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.StaffRes)
def create_staff(user: schemas.StaffCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    school = db.query(models.School).filter(
        models.School.manager_id == current_user.id).first()
    if current_user.role_id != 2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
    if not school:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail=f"Not allowed!!! You must create a school before adding staff!")

    hashed_pass = utils.hash(user.password)
    user.password = hashed_pass
    new_user = models.User(school_id=school.id, **user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(school.id, new_user)
    return new_user


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_staff(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    school = db.query(models.School).filter(
        models.School.manager_id == current_user.id).first()
    staff = db.query(models.User).filter(
        models.User.role_id == 3, models.User.id == id).first()
    if not school:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No school was found with you as the manager!")
    if not staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No staff with id: {id} was found!")
    if current_user.role_id != 1 and 2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")

    staff.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}')
def update_staff(id: int, updated_staff: schemas.StaffCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    school = db.query(models.School).filter(
        models.School.manager_id == current_user.id).first()
    staff = db.query(models.User).filter(
        models.User.role_id == 3, models.User.id == id).first()
    if not school:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No school was found with you as the manager!")
    if not staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"staff with id: {id} was not found")
    if current_user.role_id != 1 and current_user.role_id != 2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")

    staff.update(updated_staff.dict(), synchronize_session=False)
    db.commit()
    return staff
