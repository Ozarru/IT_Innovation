from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..config.database import get_db
from app import gen_schemas, models, utils, oauth2

router = APIRouter(prefix='/managers', tags=['Managers'])


@router.get('/', response_model=List[gen_schemas.GenUserRes])
def get_managers(db: Session = Depends(get_db), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    # def get_managers(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    # if current_user.role_id != 1:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail=f"Forbidden!!! Insufficient authentication credentials")
    # managers = db.query(models.User).filter(models.User.role_id == 2).all()
    managers = db.query(models.User).filter(models.User.role_id == 2).all()
    # managers = db.query(models.User).filter(
    #     models.User.name.contains(search)).limit(limit).offset(offset).all()
    return managers


@router.get('/{id}', response_model=gen_schemas.GenUserRes)
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


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=gen_schemas.GenUserRes)
def create_managers(user: gen_schemas.GenUserCreate, db: Session = Depends(get_db)):

    hashed_pass = utils.hash(user.password)
    user.password = hashed_pass
    new_user = models.User(role_id=2, **user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(new_user)
    return new_user


@router.post('/activate', status_code=status.HTTP_201_CREATED, response_model=gen_schemas.ManagerRes)
def activate_manager(manager: gen_schemas.ManagerActivate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    manager_exists = db.query(models.Manager).filter(
        models.Manager.user_id == current_user.id).first()
    # if current_user.role_id != 1 and current_user.role_id != 2:
    if current_user.role_id != 2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")
    if manager_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Conflict!!! Manager already exists.")
    else:
        new_manager = models.Manager(
            user_id=current_user.id, **manager.dict())
        db.add(new_manager)
        db.commit()
        db.refresh(new_manager)
        print(new_manager.user.email)
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
def update_manager(id: int, updated_user: gen_schemas.GenUserRes, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
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


# -----------------------------------------------Profiles----------------------------------------------


@router.get('-profiles', response_model=List[gen_schemas.ManagerRes])
def get_managers(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 20, offset: int = 0):
    managers = db.query(models.Manager).limit(limit).offset(offset).all()
    if current_user.role_id != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
    return managers


@router.get('-profiles/{id}', response_model=List[gen_schemas.ManagerRes])
def get_managers(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    manager = db.query(models.Manager).filter(models.Manager.id == id).first()
    if not manager:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No Manager with id: {id} was found!")

    if current_user.id == manager.user_id:
        return manager

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
    # return Manager
