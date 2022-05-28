
from .config.database import Base
from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=True)
    address = Column(String, nullable=True)
    is_student = Column(Boolean, server_default='FALSE', nullable=False)
    is_parent = Column(Boolean, server_default='FALSE', nullable=False)
    is_staff = Column(Boolean, server_default='FALSE', nullable=False)
    is_admin = Column(Boolean, server_default='FALSE', nullable=False)
    is_owner = Column(Boolean, server_default='FALSE', nullable=False)
    is_super_admin = Column(Boolean, server_default='FALSE', nullable=False)
    admin_level = Column(Integer, nullable=True, server_default=text('0'))
    registered_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'),
                           nullable=False)
    school = relationship('School', back_populates='admin',
                          uselist=False, cascade='all, delete')


class School(Base):
    __tablename__ = 'schools'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True)
    phone = Column(String, unique=True, nullable=True)
    description = Column(String, nullable=True)
    rccm_code = Column(Integer, nullable=True)
    nif_code = Column(Integer, nullable=True)
    bank_name = Column(String, nullable=True)
    bank_acc_name = Column(String, nullable=True)
    bank_acc_num = Column(BigInteger, nullable=True)
    edu_stages = relationship('EduStage', backref='school')
    is_active = Column(Boolean, server_default='FALSE', nullable=False)
    registered_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'),
                           nullable=False)
    admin_id = Column(Integer, ForeignKey(
        'users.id', ondelete="CASCADE"), primary_key=True, nullable=False)
    admin = relationship('User', back_populates='school')


class EduStage(Base):
    __tablename__ = 'edu_stages'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    school_id = Column(Integer, ForeignKey(
        'schools.id', ondelete="CASCADE"), nullable=False)
    edu_phases = relationship('EduPhase', backref='edu_stage')


class EduPhase(Base):
    __tablename__ = 'edu_phases'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    edu_calendar = Column(String, nullable=False)
    edu_stage_id = Column(Integer, ForeignKey(
        'edu_stages.id', ondelete="CASCADE"), nullable=False)
    grades = relationship('Grade', backref='edu_phase')


class Grade(Base):
    __tablename__ = 'grades'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    alias = Column(String, nullable=True)
    class_size = Column(Integer, nullable=False, default=0)
    edu_phase_id = Column(Integer, ForeignKey(
        'edu_phases.id', ondelete="CASCADE"), nullable=False)


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

# class SuperAdmin(User):
#     __tablename__ = 'superadmins'

#     admin_id = Column(Integer, ForeignKey(
#         'users.id', ondelete="CASCADE"), primary_key=True, nullable=False)
#     is_super_admin = Column(Boolean, server_default='TRUE',
#                             primary_key=True, nullable=False)
#     admin_level = Column(Integer, nullable=False, server_default=text('256'))


# class Owner(User):
#     __tablename__ = 'owners'

#     admin_id = Column(Integer, ForeignKey(
#         'users.id', ondelete="CASCADE"), primary_key=True, nullable=False)
#     is_staff = Column(Boolean, server_default='FALSE', nullable=False)
#     is_admin = Column(Boolean, server_default='TRUE', nullable=False)
#     is_owner = Column(Boolean, server_default='TRUE', nullable=False)
#     admin_level = Column(Integer, nullable=True, server_default=text('256'))


# class Admin(User):
#     __tablename__ = 'admins'

#     admin_id = Column(Integer, ForeignKey(
#         'users.id', ondelete="CASCADE"), primary_key=True, nullable=False)
#     is_staff = Column(Boolean, server_default='TRUE', nullable=False)
#     is_admin = Column(Boolean, server_default='TRUE', nullable=False)
#     is_owner = Column(Boolean, server_default='FALSE', nullable=False)
#     is_super_admin = Column(Boolean, server_default='FALSE', nullable=False)
#     admin_level = Column(Integer, nullable=True, server_default=text('128'))


# class Staff(User):
#     staff_id = Column(Integer, ForeignKey(
#         'users.id', ondelete="CASCADE"), primary_key=True, nullable=False)
#     name = Column(String, nullable=False)
#     address = Column(String, nullable=False)
#     email = Column(String, unique=True, nullable=True)
#     phone = Column(String, unique=True, nullable=True)
#     is_staff = Column(Boolean, server_default='TRUE', nullable=False)
#     employer_id = Column(Integer, ForeignKey(
#         'admins.admin_id', ondelete="CASCADE"), nullable=False)
#     employer = relationship('Admin')
#     school_id = Column(Integer, ForeignKey(
#         'schools.id', ondelete="CASCADE"), nullable=False)
#     school = relationship('School')
#     admin_level = Column(Integer, nullable=True, server_default=text('64'))

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
