from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

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


class StudentActivate(BaseModel):
    matric_id: int
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
    # classes: ClassRes
    user: GenUserRes

    class Config:
        orm_mode = True

# -------------EduStage--------------------------------


class EduStageBase (BaseModel):
    name: str
    description: Optional[str]


class EduStageCreate(EduStageBase):
    pass


class EduStageRes(EduStageBase):
    id: int
    school_id: int
    school: SchoolRes

    class Config:
        orm_mode = True

# -------------Classroom--------------------------------


class ClassroomBase (BaseModel):
    name: str
    description: Optional[str]
    class_size: Optional[int]


class ClassroomCreate(ClassroomBase):
    pass


class ClassroomRes(ClassroomBase):
    pass
    school_id: int

    class Config:
        orm_mode = True


# ----------------Course--------------------------------
class CourseBase (BaseModel):
    name: str
    description: Optional[str]
    credit: Optional[int]


class CourseCreate(CourseBase):
    pass


class CourseRes(CourseBase):
    pass

    class Config:
        orm_mode = True
