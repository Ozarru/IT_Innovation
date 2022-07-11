from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app.models import gen_models
from ..config.database import get_db
from app import gen_schemas, oauth2

router = APIRouter(prefix='/classes', tags=['Classes'])


@router.get('/', response_model=List[gen_schemas.ClasseRes])
def get_classes(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 0, offset: int = 0):
    if current_user.role_id == 1:
        classes = db.query(gen_models.Classe).all()
        return classes

    elif current_user.role_id == 2:
        school = db.query(gen_models.School).filter(
            gen_models.School.manager_id == current_user.id).first()
        if not school:
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                                detail=f"No school was found with you as the manager, hence no classes too!")
        classes = db.query(gen_models.Classe).filter(
            gen_models.Classe.school_id == school.id).all()
        if not classes:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No Classe was found!")
        return classes

    elif current_user:
        classes = db.query(gen_models.Classe).filter(
            gen_models.Classe.school_id == current_user.school_id).all()
        return classes

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.get('/{id}', response_model=gen_schemas.ClasseRes)
def get_classe(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    classe = db.query(gen_models.Classe).filter(
        gen_models.Classe.id == id).first()

    if current_user.role_id == 1:
        return classe

    elif current_user.role_id == 2:

        school = db.query(gen_models.School).filter(
            gen_models.School.manager_id == current_user.id).first()
        if not school:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No school was found with you as the manager, hence no classe too!")

        classe = db.query(gen_models.Classe).join(gen_models.School).filter(
            gen_models.Classe.school_id == school.id, gen_models.Classe.id == id).first()
        if not classe:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No classe with id: {id} was found in your school!")
        else:
            return classe

    elif current_user:
        school = db.query(gen_models.School).filter(
            gen_models.School.id == current_user.school_id).first()
        if not school:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"You do not belong to a school, so you cannot see classes!")

        classe = db.query(gen_models.Classe).join(gen_models.School).filter(
            gen_models.Clase.school.id == school.id, gen_models.Classe.id == id).first()
        if not classe:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No parent with id: {id} was found in your school!")
        else:
            return classe

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=gen_schemas.ClasseRes)
def create_classes(classe: gen_schemas.ClasseCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id != 2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
    school = db.query(gen_models.School).filter(
        gen_models.School.manager_id == current_user.id).first()
    if not school:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail=f"Not allowed!!! You must create a school before adding classes!")

    new_classe = gen_models.Classe(
        school_id=school.id, **classe.dict())
    db.add(new_classe)
    db.commit()
    db.refresh(new_classe)
    print(new_classe)
    return new_classe


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_classe(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id == 2:
        classe = db.query(gen_models.Classe).filter(
            gen_models.Classe.id == id).first()
        if classe == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"classe with id: {id} was not found")

        classe.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.put('/{id}')
def update_classe(id: int, updated_classe: gen_schemas.ClasseCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id == 2:
        classe = db.query(gen_models.Classe).filter(
            gen_models.Classe.id == id).first()
        if classe == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"classe with id: {id} was not found")

        classe.update(updated_classe.dict(), synchronize_session=False)
        db.commit()
        return classe

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
