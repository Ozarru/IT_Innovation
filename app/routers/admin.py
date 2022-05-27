from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..config.database import get_db
from app import models, schemas, utils, oauth2

router = APIRouter(prefix='/admins', tags=['Admins'])


@router.get('/', response_model=List[schemas.AdminRes])
def get_admins(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 0, skip: int = 0, search: Optional[str] = ""):
    if current_user.is_super_admin != True:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Not Authorized to perform requested action")
    admins = db.query(models.AdminRes).all()
    # admins = db.query(models.User).filter(
    #     models.User.name.contains(search)).limit(limit).offset(skip).all()
    return admins


@router.get('/{id}', response_model=schemas.AdminRes)
def get_user(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    admin = db.query(models.User).filter(models.User.id == id).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Admin with id: {id} was not found")
    if admin.admin_id != current_user.id and current_user.is_super_admin != True:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Not Authorized to perform requested action")
    return admin


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.AdminRes)
def create_admins(user: schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_pass = utils.hash(user.password)
    user.password = hashed_pass
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(new_user)
    return new_user


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} was not found")
    user_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/drugs/{id}')
def update_user(id: int, updated_user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} was not found")
    user_query.update(updated_user.dict(), synchronize_session=False)
    db.commit()
    return user
