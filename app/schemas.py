from datetime import datetime
from typing import Optional
from xmlrpc.client import boolean
from pydantic import BaseModel, EmailStr


# ---------------User--------------------------------
class UserBase(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None
    admin_level:  Optional[int] = 0
    is_super_admin: Optional[boolean] = False
    is_admin: Optional[boolean] = False
    registered_at: Optional[datetime] = None


class UserCreate(UserBase):
    pass


class UserRes(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: int

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


# -------------School--------------------------------
class SchoolBase (BaseModel):
    name: str
    address: str
    email: Optional[str] = None
    phone: Optional[str] = None
    description: Optional[str] = None
    rccm_code: Optional[int] = None
    nif_code: Optional[int] = None
    bank_name: Optional[str] = None
    bank_acc_name: Optional[str] = None
    bank_acc_num: Optional[int] = None
    edu_level: str
    term_alloction: str
    is_accredited: Optional[boolean] = False
    registered_at: Optional[datetime] = None


class SchoolCreate(SchoolBase):
    pass


class SchoolRes(BaseModel):
    id: int
    name: str
    description: str
    admin_id: int
    admin: UserRes

    class Config:
        orm_mode = True


# -------------Classroom--------------------------------
class ClassroomBase (BaseModel):
    name: str
    description: Optional[str] = None
    class_size: Optional[int] = None


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
    description: Optional[str] = None
    credit: Optional[int] = None


class CourseCreate(CourseBase):
    pass


class CourseRes(CourseBase):
    pass

    class Config:
        orm_mode = True
