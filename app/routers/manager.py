from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..config.database import get_db
from app import models, schemas, utils, oauth2

router = APIRouter(prefix='/managers', tags=['Managers'])


@router.get('/', response_model=List[schemas.UserRes])
def get_managers(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    if current_user.role_id != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials")
    managers = db.query(models.User).filter(models.User.role_id == 2).all()
    # managers = db.query(models.User).filter(
    #     models.User.name.contains(search)).limit(limit).offset(offset).all()
    return managers


@router.get('/{id}', response_model=schemas.UserRes)
def get_manager(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    manager = db.query(models.User).filter(
        models.User.role_id == 2, models.User.id == id).first()
    if not manager:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No manager with id: {id} was found")
    if current_user.role_id != 1 and manager.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials")
    return manager


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserRes)
def create_managers(user: schemas.TopUserCreate, db: Session = Depends(get_db)):

    hashed_pass = utils.hash(user.password)
    user.password = hashed_pass
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(new_user)
    return new_user


@router.post('/link_manager', status_code=status.HTTP_201_CREATED, response_model=schemas.ManagerRes)
def link_manager(manager: schemas.ManagerCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    manager_exist = db.query(models.Manager).filter(
        models.Manager.user_id == current_user.id).first()
    if current_user.role_id != 1 and current_user.role_id != 2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")
    if manager_exist:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Manager already exists.")

    new_manager = models.Manager(
        user_id=current_user.id, **manager.dict())
    db.add(new_manager)
    db.commit()
    db.refresh(new_manager)
    print(new_manager)
    return new_manager


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_manager(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    manager = db.query(models.User).filter(
        models.User.role_id == 2, models.User.id == id).first()
    if not manager:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No manager with id: {id} was found")
    if current_user.role_id != 1 and manager.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials")
    manager.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}')
def update_manager(id: int, updated_user: schemas.UserCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    manager = db.query(models.User).filter(
        models.User.role_id == 2, models.User.id == id).first()
    if not manager:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No manager with id: {id} was found")
    if current_user.role_id != 1 and manager.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials")
    manager.update(updated_user.dict(), synchronize_session=False)
    db.commit()
    return manager
