from datetime import datetime
from typing import Optional
from xmlrpc.client import boolean
from pydantic import BaseModel, EmailStr


# ---------------User--------------------------------
class UserBase(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    password: str
    phone: Optional[str] = None
    registered_at: Optional[datetime] = None


class UserCreate(UserBase):
    pass


class UserRes(BaseModel):
    id: int
    firstname: str
    lastname: str
    email: EmailStr
    phone: str

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


# -------------Admin--------------------------------
class Admin(UserBase):
    admin_id: int
    admin_level: int = 128
    is_admin: boolean = True
    is_staff: boolean = True
    is_owner: boolean = False
    is_super_admin: boolean = False


class AdminRes(UserRes):
    pass

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
    is_active: Optional[boolean] = False
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
