
from .config.database import Base
from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(Integer,  unique=True, nullable=True)
    address = Column(String, nullable=True)
    is_admin = Column(Boolean, server_default='FALSE', nullable=False)
    is_student = Column(Boolean, server_default='FALSE', nullable=False)
    is_parent = Column(Boolean, server_default='FALSE', nullable=False)
    is_staff = Column(Boolean, server_default='FALSE', nullable=False)
    is_owner = Column(Boolean, server_default='FALSE', nullable=False)
    is_super_admin = Column(Boolean, server_default='FALSE', nullable=False)
    admin_level = Column(Integer, nullable=True, server_default=text('0'))
    registered_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'),
                           nullable=False)


class School(Base):
    __tablename__ = 'schools'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True)
    phone = Column(Integer, nullable=True)
    description = Column(String, nullable=True)
    rccm_code = Column(Integer, nullable=True)
    nif_code = Column(Integer, nullable=True)
    bank_name = Column(String, nullable=True)
    bank_acc_name = Column(String, nullable=True)
    bank_acc_num = Column(BigInteger, nullable=True)
    edu_level = Column(String, nullable=False)
    term_alloction = Column(String, nullable=False)
    is_accredited = Column(Boolean, server_default='FALSE', nullable=False)
    admin_id = Column(Integer, ForeignKey(
        'users.id',  ondelete="CASCADE"), nullable=False)
    owner_id = Column(Integer, ForeignKey(
        'users.id',  ondelete="CASCADE"), nullable=True)
    owner = relationship('User')
    registered_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'),
                           nullable=False)


# class Classroom(Base):
#     __tablename__ = 'classrooms'

#     id = Column(Integer, primary_key=True, nullable=False)
#     name = Column(String, nullable=False)
#     description = Column(String, nullable=False)
#     class_size = Column(Integer, nullable=False, default=0)
#     school_id = Column(Integer, ForeignKey(
#         'schools.id', ondelete="CASCADE"), nullable=False)


# class Course(Base):
#     __tablename__ = 'courses'

#     id = Column(Integer, primary_key=True, nullable=False)
#     name = Column(String, nullable=False)
#     description = Column(String, nullable=False)
#     credit = Column(Integer, nullable=False, default=1)
#     class_id = Column(Integer, ForeignKey(
#         'classrooms.id', ondelete="CASCADE"), nullable=False)
#     school_id = Column(Integer, ForeignKey(
#         'schools.id', ondelete="CASCADE"), nullable=False)


# class Subject(Base):
#     __tablename__ = 'subjects'

#     id = Column(Integer, primary_key=True, nullable=False)
#     name = Column(String, nullable=False)
#     description = Column(String, nullable=False)
#     coefficient = Column(Integer, nullable=False, default=1)
#     class_id = Column(Integer, ForeignKey(
#         'classrooms.id', ondelete="CASCADE"), nullable=False)
#     school_id = Column(Integer, ForeignKey(
#         'schools.id', ondelete="CASCADE"), nullable=False)


# ----------------------People---------------------------------------------------


# class Staff(Base):
#     __tablename__ = 'staff'

#     id = Column(Integer, primary_key=True, nullable=False)
#     is_staff = Column(Boolean, ForeignKey(
#         'users.is_staff', ondelete="CASCADE"), unique=True, nullable=False, server_default='TRUE')
#     user_id = Column(Integer, ForeignKey(
#         'users.id', ondelete="CASCADE"), nullable=False)
#     school_id = Column(Integer, ForeignKey(
#         'schools.id', ondelete="CASCADE"), nullable=False)
#     is_academic = Column(Boolean, server_default='TRUE', nullable=False)


# class Parent(Base):
#     __tablename__ = 'parents'

#     id = Column(Integer, primary_key=True, nullable=False)
#     is_parent = Column(Boolean, ForeignKey(
#         'users.is_parent', ondelete="CASCADE"), nullable=False, server_default='TRUE')
#     user_id = Column(Integer, ForeignKey(
#         'users.id', ondelete="CASCADE"), nullable=False)
#     school_id = Column(Integer, ForeignKey(
#         'schools.id', ondelete="CASCADE"), nullable=False)


# class Student(Base):
#     __tablename__ = 'students'

#     id = Column(Integer, primary_key=True, nullable=False)
#     is_student = Column(Boolean, ForeignKey(
#         'users.is_student', ondelete="CASCADE"), nullable=False, server_default='TRUE')
#     user_id = Column(Integer, ForeignKey(
#         'users.id', ondelete="CASCADE"), nullable=False)
#     class_id = Column(Integer, ForeignKey(
#         'classrooms.id', ondelete="CASCADE"), nullable=False)
#     school_id = Column(Integer, ForeignKey(
#         'schools.id', ondelete="CASCADE"), nullable=False)
