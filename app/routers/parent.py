from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ..models import gen_models
from ..config.database import get_db
from .. import gen_schemas, utils, oauth2

router = APIRouter(prefix='/parents', tags=['Parents'])


@router.get('/', response_model=List[gen_schemas.GenUserRes])
def get_parents(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 20, offset: int = 0):

    if current_user.role_id == 1:
        parents = db.query(gen_models.User).filter(
            gen_models.User.role_id == 5).limit(limit).offset(offset).all()
        return parents

    elif current_user.role_id == 2:
        school = db.query(gen_models.School).filter(
            gen_models.School.manager_id == current_user.id).first()

        if not school:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No school was found with you as the manager, hence no parent too!")

        parents = db.query(gen_models.User).join(gen_models.School).filter(
            gen_models.User.role_id == 5, gen_models.School.id == school.id).all()
        if not parents:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No parent was found!")
        return parents

    elif current_user:
        parents = db.query(gen_models.User).filter(
            gen_models.User.role_id == 5, gen_models.User.school_id == current_user.school_id).all()
        return parents

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.get('/{id}', response_model=gen_schemas.GenUserRes)
def get_parent(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    parent = db.query(gen_models.User).filter(
        gen_models.User.role_id == 5, gen_models.User.id == id).first()

    if current_user.role_id == 1:
        return parent

    elif current_user.role_id == 2:

        school = db.query(gen_models.School).filter(
            gen_models.School.manager_id == current_user.id).first()
        if not school:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No school was found with you as the manager, hence no parent too!")

        parent = db.query(gen_models.User).join(gen_models.School).filter(
            gen_models.User.role_id == 5, gen_models.School.manager_id == current_user.id, gen_models.User.id == id).first()
        if not parent:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No parent with id: {id} was found in your school!")
        else:
            return parent

    elif current_user:
        school = db.query(gen_models.School).filter(
            gen_models.School.id == current_user.school_id).first()
        if not school:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"You do not belong to a school, so you cannot see parents!")

        parent = db.query(gen_models.User).join(gen_models.School).filter(
            gen_models.User.id == id, gen_models.School.id == school.id).first()
        if not parent:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No parent with id: {id} was found in your school!")
        else:
            return parent

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=gen_schemas.GenUserRes)
def create_parents(user: gen_schemas.GenUserCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id != 2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
    school = db.query(gen_models.School).filter(
        gen_models.School.manager_id == current_user.id).first()
    if not school:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail=f"Not allowed!!! You must create a school before adding parents!")

    hashed_pass = utils.hash(user.password)
    user.password = hashed_pass
    new_user = gen_models.User(role_id=5, school_id=school.id, **user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(school.id, new_user)
    return new_user


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_parent(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    school = db.query(gen_models.School).filter(
        gen_models.School.manager_id == current_user.id).first()
    parent = db.query(gen_models.User).filter(
        gen_models.User.role_id == 5, gen_models.User.id == id).first()
    if not school:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No school was found with you as the manager, hence no parent too!")
    if not parent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No parent with id: {id} was found!")
    if current_user.role_id != 2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")

    parent.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}')
def update_parent(id: int, updated_parent: gen_schemas.GenUserCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id == 2:
        school = db.query(gen_models.School).filter(
            gen_models.School.manager_id == current_user.id).first()
        if not school:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No school was found with you as the manager, hence no parent too!")
        parent = db.query(gen_models.User).filter(
            gen_models.User.role_id == 5, gen_models.User.id == id).first()
        if not parent:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"parent with id: {id} was not found")

        parent.update(updated_parent.dict(), synchronize_session=False)
        db.commit()
        return parent

    elif current_user.id == id:
        parent = db.query(gen_models.User).filter(
            gen_models.User.role_id == 5, gen_models.User.id == id).first()
        if not parent:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"parent with id: {id} was not found")

        parent.update(updated_parent.dict(), synchronize_session=False)
        db.commit()
        return parent

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")

# -----------------------------------------Activation-----------------------------------------------------------------------


@router.post('/activate', status_code=status.HTTP_201_CREATED, response_model=gen_schemas.ParentRes)
def activate_parent(parent: gen_schemas.ParentActivate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    school = db.query(gen_models.School).filter(
        gen_models.School.manager_id == current_user.id).first()
    if current_user.role_id != 1 and current_user.role_id != 2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")
    elif not school:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail=f"Not allowed!!! You must create a school before activating parents!")

    new_parent = gen_models.Parent(**parent.dict())
    db.add(new_parent)
    db.commit()
    db.refresh(new_parent)
    print(new_parent)
    return new_parent


# -----------------------------------------Profile-----------------------------------------------------------------------


@router.get('-profiles', response_model=List[gen_schemas.ParentRes])
def get_profiles(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 20, offset: int = 0):
    if current_user.role_id == 1:
        parents = db.query(gen_models.Parent).limit(limit).offset(offset).all()
        return parents
    elif current_user.role_id == 2:
        school = db.query(gen_models.School).filter(
            gen_models.School.manager_id == current_user.id).first()
        parents = db.query(gen_models.Parent).join(gen_models.User).filter(
            gen_models.User.school == school).all()

        if not school:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No school was found with you as the manager, hence no parent too!")
        if not parents:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No parent was found in your school!")
        return parents
    elif current_user:
        school = db.query(gen_models.School).filter(
            gen_models.School.id == current_user.school_id).first()
        parents = db.query(gen_models.Parent).join(gen_models.User).filter(
            gen_models.User.school == school).all()
        if not school:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Sorry, you do not belong to any school!")
        if not parents:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No parent was found in your school!")
        return parents
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.get('-profiles/{id}', response_model=gen_schemas.ParentRes)
def get_profile(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id == 1:
        parent = db.query(gen_models.Parent).filter(
            gen_models.Parent.id == id).first()
        if not parent:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No parent with id: {id} was found!")
        return parent

    elif current_user.role_id == 2:
        school = db.query(gen_models.School).filter(
            gen_models.School.manager_id == current_user.id).first()
        parent = db.query(gen_models.Parent).join(gen_models.User).filter(
            gen_models.Parent.id == id, gen_models.User.school_id == school.id).first()
        if not school:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No school was found with you as the manager, hence no parent too!")
        if not parent:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No parent with id:{id} was found in your school!")
        return parent

    elif current_user:
        school = db.query(gen_models.School).filter(
            gen_models.School.id == current_user.school_id).first()
        parent = db.query(gen_models.Parent).join(gen_models.User).filter(
            gen_models.Parent.id == id, gen_models.User.school_id == school.id).first()
        if not school:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Sorry, you do not belong to any school!")
        if not parent:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No parent with id:{id} was found in your school!")
        return parent
