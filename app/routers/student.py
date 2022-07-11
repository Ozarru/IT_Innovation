from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ..models import gen_models
from ..config.database import get_db
from .. import gen_schemas, utils, oauth2

router = APIRouter(prefix='/students', tags=['Students'])


@router.get('/', response_model=List[gen_schemas.GenUserRes])
def get_students(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 20, offset: int = 0):

    if current_user.role_id == 1:
        students = db.query(gen_models.User).filter(
            gen_models.User.role_id == 4).limit(limit).offset(offset).all()
        return students

    elif current_user.role_id == 2:
        school = db.query(gen_models.School).filter(
            gen_models.School.manager_id == current_user.id).first()

        if not school:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No school was found with you as the manager, hence no student too!")

        students = db.query(gen_models.User).join(gen_models.School).filter(
            gen_models.User.role_id == 4, gen_models.School.id == school.id).all()
        if not students:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No Student was found!")
        return students

    elif current_user:
        students = db.query(gen_models.User).filter(
            gen_models.User.role_id == 4, gen_models.User.school_id == current_user.school_id).all()
        return students

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.get('/{id}', response_model=gen_schemas.GenUserRes)
def get_student(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    student = db.query(gen_models.User).filter(
        gen_models.User.role_id == 4, gen_models.User.id == id).first()

    if current_user.role_id == 1:
        return student

    elif current_user.role_id == 2:

        school = db.query(gen_models.School).filter(
            gen_models.School.manager_id == current_user.id).first()
        if not school:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No school was found with you as the manager, hence no student too!")

        student = db.query(gen_models.User).join(gen_models.School).filter(
            gen_models.User.role_id == 4, gen_models.School.manager_id == current_user.id, gen_models.User.id == id).first()
        if not student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No student with id: {id} was found in your school!")
        else:
            return student

    elif current_user:
        school = db.query(gen_models.School).filter(
            gen_models.School.id == current_user.school_id).first()
        if not school:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"You do not belong to a school, so you cannot see students!")

        student = db.query(gen_models.User).join(gen_models.School).filter(
            gen_models.User.id == id, gen_models.School.id == school.id).first()
        if not student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No student with id: {id} was found in your school!")
        else:
            return student

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=gen_schemas.GenUserRes)
def create_students(user: gen_schemas.GenUserCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id != 2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
    school = db.query(gen_models.School).filter(
        gen_models.School.manager_id == current_user.id).first()
    if not school:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail=f"Not allowed!!! You must create a school before adding students!")

    hashed_pass = utils.hash(user.password)
    user.password = hashed_pass
    new_user = gen_models.User(role_id=4, school_id=school.id, **user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(school.id, new_user)
    return new_user


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_student(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    school = db.query(gen_models.School).filter(
        gen_models.School.manager_id == current_user.id).first()
    student = db.query(gen_models.User).filter(
        gen_models.User.role_id == 4, gen_models.User.id == id).first()
    if not school:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No school was found with you as the manager, hence no student too!")
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No student with id: {id} was found!")
    if current_user.role_id != 2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")

    student.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}')
def update_student(id: int, updated_student: gen_schemas.GenUserCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    school = db.query(gen_models.School).filter(
        gen_models.School.manager_id == current_user.id).first()
    student = db.query(gen_models.User).filter(
        gen_models.User.role_id == 4, gen_models.User.id == id).first()
    if not school:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No school was found with you as the manager, hence no student too!")
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"student with id: {id} was not found")
    if current_user.role_id != 1 and current_user.role_id != 2 and current_user.id != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")

    student.update(updated_student.dict(), synchronize_session=False)
    db.commit()
    return student


# -----------------------------------------Activation-----------------------------------------------------------------------


@router.post('/activate', status_code=status.HTTP_201_CREATED, response_model=gen_schemas.StudentRes)
def activate_student(student: gen_schemas.StudentActivate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    school = db.query(gen_models.School).filter(
        gen_models.School.manager_id == current_user.id).first()
    if current_user.role_id != 1 and current_user.role_id != 2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")
    elif not school:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail=f"Not allowed!!! You must create a school before activating students!")

    new_student = gen_models.Student(**student.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    print(new_student)
    return new_student


# -----------------------------------------Profile-----------------------------------------------------------------------


@router.get('-profiles', response_model=List[gen_schemas.StudentRes])
def get_profiles(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 20, offset: int = 0):
    if current_user.role_id == 1:
        students = db.query(gen_models.Student).limit(limit).offset(offset).all()
        return students
    elif current_user.role_id == 2:
        school = db.query(gen_models.School).filter(
            gen_models.School.manager_id == current_user.id).first()
        students = db.query(gen_models.Student).join(gen_models.User).filter(
            gen_models.User.school == school).all()

        if not school:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No school was found with you as the manager, hence no Student too!")
        if not students:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No Student was found in your school!")
        return students
    elif current_user:
        school = db.query(gen_models.School).filter(
            gen_models.School.id == current_user.school_id).first()
        students = db.query(gen_models.Student).join(gen_models.User).filter(
            gen_models.User.school == school).all()
        if not school:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Sorry, you do not belong to any school!")
        if not students:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No Student was found in your school!")
        return students
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.get('-profiles/{id}', response_model=gen_schemas.StudentRes)
def get_profile(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id == 1:
        student = db.query(gen_models.Student).filter(
            gen_models.Student.id == id).first()
        if not student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No student with id: {id} was found!")
        return student

    elif current_user.role_id == 2:
        school = db.query(gen_models.School).filter(
            gen_models.School.manager_id == current_user.id).first()
        student = db.query(gen_models.Student).join(gen_models.User).filter(
            gen_models.Student.id == id, gen_models.User.school_id == school.id).first()
        if not school:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No school was found with you as the manager, hence no Student too!")
        if not student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No Student with id:{id} was found in your school!")
        return student

    elif current_user:
        school = db.query(gen_models.School).filter(
            gen_models.School.id == current_user.school_id).first()
        student = db.query(gen_models.Student).join(gen_models.User).filter(
            gen_models.Student.id == id, gen_models.User.school_id == school.id).first()
        if not school:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Sorry, you do not belong to any school!")
        if not student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No Student with id:{id} was found in your school!")
        return student
