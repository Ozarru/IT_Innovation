from .config.database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    birth_date = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=True)
    address = Column(String, nullable=True)
    is_active = Column(Boolean, server_default='FALSE', nullable=False)
    registered_at = Column(TIMESTAMP(timezone=True),
                           server_default=text('now()'))
    last_login = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    role_id = Column(Integer, ForeignKey(
        'roles.id', ondelete="CASCADE"), nullable=True)
    role = relationship('Role', backref="users")
    school_id = Column(Integer, ForeignKey(
        'schools.id', ondelete="CASCADE"), nullable=True)
    school = relationship('School', backref="users")


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    sec_level = Column(Integer, server_default='0', nullable=False)


class SubRole(Base):
    __tablename__ = 'subroles'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    sec_level = Column(Integer, server_default='0', nullable=False)


class Manager(Base):
    __tablename__ = 'managers'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    is_manager = Column(Boolean, server_default='true', nullable=False)
    user_id = Column(Integer, ForeignKey(
        'users.id', ondelete="CASCADE"), primary_key=True, unique=True, nullable=False)
    user = relationship('User', backref=backref("manager", uselist=False))


class Staff(Base):
    __tablename__ = 'staff'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    matric_id = Column(Integer, unique=True, nullable=False)
    is_staff = Column(Boolean, server_default='true', nullable=False)
    email = Column(String, ForeignKey(
        'users.email', ondelete="CASCADE"), primary_key=True, unique=True, nullable=False)
    user = relationship('User', backref=backref("staff", uselist=False))


fam_assoc_table = Table(
    "family_association",
    Base.metadata,
    Column("parent_email", ForeignKey('parents.email'), unique=True),
    Column("student_email", ForeignKey('students.email'), unique=True),
)


class Parent(Base):
    __tablename__ = 'parents'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    is_parent = Column(Boolean, server_default='true', nullable=False)
    email = Column(String, ForeignKey(
        'users.email', ondelete="CASCADE"), primary_key=True, unique=True, nullable=False)
    user = relationship('User', backref=backref("parent", uselist=False))
    students = relationship(
        "Student", secondary=fam_assoc_table, back_populates="parents"
    )


class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    matric_id = Column(Integer, unique=True, nullable=False)
    is_student = Column(Boolean, server_default='true', nullable=False)
    email = Column(String, ForeignKey(
        'users.email', ondelete="CASCADE"), primary_key=True, unique=True, nullable=False)
    user = relationship('User', backref=backref("student", uselist=False))
    parents = relationship(
        "Parent", secondary=fam_assoc_table, back_populates="students"
    )


class School(Base):
    __tablename__ = 'schools'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True)
    phone = Column(String, unique=True, nullable=True)
    description = Column(String, nullable=True)
    rccm_code = Column(Integer, nullable=True)
    nif_code = Column(Integer, nullable=True)
    bank_name = Column(String, nullable=True)
    bank_acc_name = Column(String, nullable=True)
    bank_acc_num = Column(String, unique=True, nullable=True)
    is_active = Column(Boolean, server_default='FALSE', nullable=False)
    registered_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'),
                           nullable=False)
    manager_id = Column(Integer, ForeignKey("managers.user_id"),
                        primary_key=True, unique=True, nullable=False)
    manager = relationship('Manager', backref=backref("school", uselist=False))


class EduStage(Base):
    __tablename__ = 'edu_stages'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    school_id = Column(Integer, ForeignKey(
        'schools.id', ondelete="CASCADE"), nullable=False)
    school = relationship('School', backref="edu_stages")


class EduPhase(Base):
    __tablename__ = 'edu_phases'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    edu_calendar = Column(String, nullable=False)
    edu_stage_id = Column(Integer, ForeignKey(
        'edu_stages.id', ondelete="CASCADE"), nullable=False)
    edu_stage = relationship('EduStage', backref="edu_phases")


class Grade(Base):
    __tablename__ = 'grades'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    alias = Column(String, nullable=True)
    class_size = Column(Integer, nullable=False, default=0)
    edu_phase_id = Column(Integer, ForeignKey(
        'edu_phases.id', ondelete="CASCADE"), nullable=False)
    edu_phase = relationship('EduPhase', backref="grades")


# class Course(Base):
#     __tablename__ = 'courses'

#     id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
#     name = Column(String, nullable=False)
#     description = Column(String, nullable=False)
#     credit = Column(Integer, nullable=False, default=1)
#     class_id = Column(Integer, ForeignKey(
#         'classrooms.id', ondelete="CASCADE"), nullable=False)
#     school_id = Column(Integer, ForeignKey(
#         'schools.id', ondelete="CASCADE"), nullable=False)


# class Subject(Base):
#     __tablename__ = 'subjects'

#     id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
#     name = Column(String, nullable=False)
#     description = Column(String, nullable=False)
#     coefficient = Column(Integer, nullable=False, default=1)
#     class_id = Column(Integer, ForeignKey(
#         'classrooms.id', ondelete="CASCADE"), nullable=False)
#     school_id = Column(Integer, ForeignKey(
#         'schools.id', ondelete="CASCADE"), nullable=False)
