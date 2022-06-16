from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..config.database import get_db
from .. import models, schemas, utils, oauth2

router = APIRouter(prefix='/parents', tags=['Parents'])


@router.get('/', response_model=List[schemas.GenUserRes])
# @router.get('/', response_model=List[schemas.ParentRes])
def get_parents(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 20, offset: int = 0):
    if current_user.role_id == 1:
        parents = db.query(models.User).filter(models.User.role_id == 5).all()
        # parents = db.query(models.Parent).all()
        # parents = db.query(models.User).filter(models.User.role_id == 5).limit(limit).offset(offset).all()
        return parents
    elif current_user.role_id == 2:
        school = db.query(models.School).filter(
            models.School.manager_id == current_user.id).first()
        parents = db.query(models.User).filter(
            models.User.role_id == 5, models.User.school_id == school.id).all()
        # parents = db.query(models.Parent).filter(
        #     models.Parent.user.school.manager_id == current_user.id).all()

        # models.User.role_id == 5,, models.User.school_id == current_school).limit(limit).offset(offset).all()
        if not school:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No school was found with you as the manager, hence no parent too!")
        if not parents:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No Parent was found!")
        return parents
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.get('/{id}', response_model=schemas.GenUserRes)
def get_parent(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    school = db.query(models.School).filter(
        models.School.manager_id == current_user.id).first()
    parent = db.query(models.User).filter(
        models.User.role_id == 5, models.User.id == id).first()
    if not school:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No school was found with you as the manager, hence no parent too!")
    if not parent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No parent with id: {id} was found!")
    if current_user.role_id != 1 and current_user.role_id != 2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
    return parent


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.GenUserRes)
def create_parents(user: schemas.GenUserCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    school = db.query(models.School).filter(
        models.School.manager_id == current_user.id).first()
    if current_user.role_id != 2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
    if not school:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail=f"Not allowed!!! You must create a school before adding parents!")

    hashed_pass = utils.hash(user.password)
    user.password = hashed_pass
    new_user = models.User(role_id=5, school_id=school.id, **user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(school.id, new_user)
    return new_user


@router.post('/activate', status_code=status.HTTP_201_CREATED, response_model=schemas.ParentRes)
def activate_parent(parent: schemas.ParentActivate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    # parent_exist = db.query(models.Parent).filter(
    #     models.Parent.user_email == current_user.id).first()
    school = db.query(models.School).filter(
        models.School.manager_id == current_user.id).first()
    if current_user.role_id != 1 and current_user.role_id != 2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")
    # if parent_exist:
    #     raise HTTPException(status_code=status.HTTP_409_CONFLICT,
    #                         detail=f"Conflict!!! Parent already exists.")
    elif not school:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail=f"Not allowed!!! You must create a school before activating parents!")

    new_parent = models.Parent(**parent.dict())
    db.add(new_parent)
    db.commit()
    db.refresh(new_parent)
    print(new_parent)
    return new_parent


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_parent(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    school = db.query(models.School).filter(
        models.School.manager_id == current_user.id).first()
    parent = db.query(models.User).filter(
        models.User.role_id == 5, models.User.id == id).first()
    if current_user.role_id != 1 and 2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
    if not school:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No school was found with you as the manager, hence no parent too!")
    if not parent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No parent with id: {id} was found!")

    parent.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}')
def update_parent(id: int, updated_parent: schemas.GenUserCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    school = db.query(models.School).filter(
        models.School.manager_id == current_user.id).first()
    parent = db.query(models.User).filter(
        models.User.role_id == 5, models.User.id == id).first()
    if not school:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No school was found with you as the manager, hence no parent too!")
    if not parent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No parent with id: {id} was found")
    if current_user.role_id != 1 and current_user.role_id != 2 and current_user.id != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")

    parent.update(updated_parent.dict(), synchronize_session=False)
    db.commit()
    return parent

# -----------------------------------------------Profiles----------------------------------------------


@router.get('-profiles', response_model=List[schemas.ParentRes])
def get_parents(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 20, offset: int = 0):
    if current_user.role_id == 1:
        parents = db.query(models.Parent).limit(limit).offset(offset).all()
        return parents
    elif current_user.role_id == 2:
        school = db.query(models.School).filter(
            models.School.manager_id == current_user.id).first()
        parents = db.query(models.Parent).filter(
            models.Parent.user.school.manager_id == current_user.id).all()

        if not school:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No school was found with you as the manager, hence no parent too!")
        if not parents:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No Parent was found!")
        return parents
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.get('-profiles/{id}', response_model=List[schemas.ParentRes])
def get_parents(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    parent = db.query(models.Parent).filter(models.Parent.id == id).first()

    if not parent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No parent with id: {id} was found!")

    if current_user.email == parent.email:
        return parent

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
    # return parent
