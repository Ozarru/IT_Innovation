from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..config.database import get_db
from app import models, schemas, utils, oauth2

router = APIRouter(prefix='/superusers', tags=['Superusers'])


@router.get('/', response_model=List[schemas.GenUserRes])
def get_superusers(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    if current_user.role_id != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials")
    superusers = db.query(models.User).filter(models.User.role_id == 1).all()
    # superusers = db.query(models.User).filter(
    #     models.User.name.contains(search)).limit(limit).offset(offset).all()
    return superusers


@router.get('/{id}', response_model=schemas.GenUserRes)
def get_superuser(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    superuser = db.query(models.User).filter(
        models.User.role_id == 1, models.User.id == id).first()
    if not superuser:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No superuser with id: {id} was found")
    if current_user.role_id != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials")
    return superuser


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.GenUserRes)
# def create_superusers(user: schemas.GenUserCreate, db: Session = Depends(get_db)):
def create_superusers(user: schemas.GenUserCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials")

    hashed_pass = utils.hash(user.password)
    user.password = hashed_pass
    new_user = models.User(role_id=1, **user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(new_user)
    return new_user


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_superuser(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    superuser = db.query(models.User).filter(
        models.User.role_id == 1, models.User.id == id).first()
    if not superuser:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No superuser with id: {id} was found")
    if current_user.role_id != 1 and superuser.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials")
    superuser.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}')
def update_superuser(id: int, updated_user: schemas.GenUserCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    superuser = db.query(models.User).filter(
        models.User.role_id == 1, models.User.id == id).first()
    if not superuser:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No superuser with id: {id} was found")
    if current_user.role_id != 1 and superuser.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials")
    superuser.update(updated_user.dict(), synchronize_session=False)
    db.commit()
    return superuser
