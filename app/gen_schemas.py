from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from .func_schemas import AcadTermRes, AcadYearRes

# --------------------------------------------------Role schemas------------------------------------------


class Role(BaseModel):
    name: str
    sec_level: int

    class Config:
        orm_mode = True


# -------------------------------------------Authentication schemas--------------------------------------


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]


# ------------------------------------------------Request schemas----------------------------------------


# User creation schemas
class GenUserCreate(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    password: str
    phone: Optional[str]
    # school_id: Optional[int]

    class Config:
        orm_mode = True


# School creation schemas
class SchoolCreate (BaseModel):
    name: str
    address: str
    email: Optional[str]
    phone: Optional[str]
    description: Optional[str]
    rccm_code: Optional[int]
    nif_code: Optional[int]
    bank_name: Optional[str]
    bank_acc_name: Optional[str]
    bank_acc_num: Optional[int]
    is_active: Optional[bool]
    registered_at: Optional[datetime]

    class Config:
        orm_mode = True


# Activation schemas
class ManagerActivate(BaseModel):
    is_manager: bool = True

    class Config:
        orm_mode = True


class ParentActivate(BaseModel):
    is_parent: bool = True
    email: EmailStr

    class Config:
        orm_mode = True


class PrtAssocStd(BaseModel):
    parent_mail: EmailStr
    student_mail: EmailStr

    class Config:
        orm_mode = True


class StudentActivate(BaseModel):
    matric_id: int
    grade_id: int
    is_student: bool = True
    email: EmailStr

    class Config:
        orm_mode = True


class StaffActivate(BaseModel):
    matric_id: int
    is_staff: bool = True
    email: EmailStr

    class Config:
        orm_mode = True


# ------------------------------------------------Response schemas---------------------------------------


class SchoolRes(BaseModel):
    id: int
    name: str
    description: str
    manager_id: int
    # manager:  "GenUserRes"

    class Config:
        orm_mode = True


class GenUserRes(BaseModel):
    id: int
    firstname: Optional[str]
    lastname: Optional[str]
    email: EmailStr
    role_id: Optional[int]
    role: Optional[Role]
    school_id: Optional[int]
    school: Optional[SchoolRes]

    class Config:
        orm_mode = True


class ManagerRes(BaseModel):
    id: int
    user_id: int
    user: GenUserRes

    class Config:
        orm_mode = True


class StudentRes(BaseModel):
    id: int
    is_student: bool
    matric_id: int
    email: EmailStr
    parents: list[GenUserRes]
    user: GenUserRes
    # classe: "ClasseRes"

    class Config:
        orm_mode = True


class ParentRes(BaseModel):
    id: int
    is_parent: bool
    email: EmailStr
    students: list[GenUserRes]
    user: GenUserRes

    class Config:
        orm_mode = True


class StaffRes(BaseModel):
    id: int
    is_staff: bool
    email: EmailStr
    user: GenUserRes

    class Config:
        orm_mode = True

# -------------EduStage--------------------------------


class EduStageCreate (BaseModel):
    name: str
    description: Optional[str]


class EduStageRes(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

# -------------EduPhase--------------------------------


class EduPhaseCreate (BaseModel):
    name: str
    edu_stage_id: int
    description: Optional[str]


class EduPhaseRes(BaseModel):
    id: int
    name: str
    edu_stage: EduStageRes
    description: Optional[str]

    class Config:
        orm_mode = True

# -------------Classroom--------------------------------


class GradeCreate (BaseModel):
    name: str
    edu_phase_id: int
    description: Optional[str]


class GradeRes(BaseModel):
    id: int
    name: str
    description: Optional[str]
    edu_phase: EduPhaseRes

    class Config:
        orm_mode = True


class ClasseCreate (BaseModel):
    grade_id: int
    alias: Optional[str]
    class_size: Optional[int]
    supervisor_mail: Optional[EmailStr]


class ClasseRes(BaseModel):
    id: int
    alias: str
    class_size: int
    grade: GradeRes
    school: SchoolRes
    supervisor: Optional[StaffRes]

    class Config:
        orm_mode = True


# ----------------Course--------------------------------
class SubjectCreate (BaseModel):
    name: str
    description: Optional[str]
    syllabus: Optional[str]
    coefficient: Optional[int]
    grade_id: int
    teacher_mail: EmailStr
    term_id: int
    academic_year_id: int


class SubjectRes(BaseModel):
    id: int
    name: str
    description: str
    syllabus: str
    coefficient: int
    grade: GradeRes
    teacher: StaffRes
    term: "AcadTermRes"
    academic_year: "AcadYearRes"

    class Config:
        orm_mode = True
