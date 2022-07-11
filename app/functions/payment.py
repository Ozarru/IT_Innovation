from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app.models import gen_models
from ..config.database import get_db
from app import func_schemas, oauth2

router = APIRouter(prefix='/payments', tags=['Payments'])


@router.get('/', response_model=List[func_schemas.PaymentRes])
def get_payments(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 0, offset: int = 0):
    if current_user.role_id == 1:
        payments = db.query(gen_models.Payment).all()
        return payments

    elif current_user.role_id == 2:
        school = db.query(gen_models.School).filter(
            gen_models.School.manager_id == current_user.id).first()
        if not school:
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                                detail=f"No school was found with you as the manager, hence no payments too!")
        payments = db.query(gen_models.Payment).filter(
            gen_models.Payment.school_id == school.id).all()
        if not payments:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No payment was found!")
        return payments

    elif current_user:
        payments = db.query(gen_models.Payment).filter(
            gen_models.Payment.school_id == current_user.school_id).all()
        return payments

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.get('/{id}', response_model=func_schemas.PaymentRes)
def get_payment(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    payment = db.query(gen_models.Payment).filter(
        gen_models.Payment.id == id).first()

    if current_user.role_id == 1:
        return payment

    elif current_user.role_id == 2:

        school = db.query(gen_models.School).filter(
            gen_models.School.manager_id == current_user.id).first()
        if not school:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No school was found with you as the manager, hence no payment too!")

        payment = db.query(gen_models.Payment).join(gen_models.School).filter(
            gen_models.Payment.school_id == school.id, gen_models.Payment.id == id).first()
        if not payment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No payment with id: {id} was found in your school!")
        else:
            return payment

    elif current_user:
        school = db.query(gen_models.School).filter(
            gen_models.School.id == current_user.school_id).first()
        if not school:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"You do not belong to a school, so you cannot see payments!")

        payment = db.query(gen_models.Payment).join(gen_models.School).filter(
            gen_models.Clase.school.id == school.id, gen_models.Payment.id == id).first()
        if not payment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No payment with id: {id} was found in your school!")
        else:
            return payment

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=func_schemas.PaymentRes)
def create_payments(payment: func_schemas.PaymentCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id != 2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
    school = db.query(gen_models.School).filter(
        gen_models.School.manager_id == current_user.id).first()
    if not school:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail=f"Not allowed!!! You must create a school before adding payments!")

    new_payment = gen_models.Payment(
        school_id=school.id, **payment.dict())
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    print(new_payment)
    return new_payment


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_payment(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id == 2:
        payment = db.query(gen_models.Payment).filter(
            gen_models.Payment.id == id).first()
        if payment == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"payment with id: {id} was not found")

        payment.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.put('/{id}')
def update_payment(id: int, updated_payment: func_schemas.PaymentCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id == 2:
        payment = db.query(gen_models.Payment).filter(
            gen_models.Payment.id == id).first()
        if payment == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"payment with id: {id} was not found")

        payment.update(updated_payment.dict(), synchronize_session=False)
        db.commit()
        return payment

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
