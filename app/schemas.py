from datetime import datetime
from typing import Optional
from xmlrpc.client import boolean
from pydantic import BaseModel, EmailStr


class Role(BaseModel):
    name = str
    sec_level = int


class RoleRes(Role):
    pass


# ---------------User--------------------------------
class UserBase(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    password: str
    birth_date: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    birth_date: Optional[str]
    is_active: Optional[boolean]
    registered_at: Optional[datetime]
    role_id: Optional[int]
    school_id: Optional[int]


class UserCreate(UserBase):
    pass


class UserRes(BaseModel):
    id: int
    firstname: str
    lastname: str
    email: EmailStr
    phone: str
    role_id: int
    school_id: int
    # role: RoleRes
    # school: "SchoolRes"

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]


# -------------User creation schemas--------------------------------
class GenUserCreate(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    password: str
    phone: Optional[str]

    class Config:
        orm_mode = True


class SuperUserCreate(GenUserCreate):
    pass
    role_id: int = 1


class TopUserCreate(GenUserCreate):
    pass
    role_id: int = 2


class StaffCreate(GenUserCreate):
    pass
    role_id: int = 3


class StudentCreate(GenUserCreate):
    pass
    role_id: int = 4


class ParentCreate(GenUserCreate):
    pass
    role_id: int = 5

# -------------User response schemas--------------------------------


class GenUserRes(BaseModel):
    id: int
    firstname: str
    lastname: str
    role_id: int

    class Config:
        orm_mode = True


class SuperUserRes(GenUserRes):
    pass


class TopUserRes(GenUserRes):
    pass


class StaffRes(GenUserRes):
    pass
    school_id: int
    # school: "SchoolRes"


class StudentRes(GenUserRes):
    pass
    school_id: int
    # school: "SchoolRes"


class ParentRes(GenUserRes):
    pass
    school_id: int
    # school: "SchoolRes"


# -------------Manager schemas--------------------------------


class Manager(BaseModel):
    user_id: int
    user: UserRes
    school: "SchoolRes"


class ManagerCreate(BaseModel):
    is_manager: boolean


class ManagerRes(BaseModel):
    user_id: int
    user: TopUserRes

# -------------School schemas--------------------------------


class SchoolBase (BaseModel):
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
    is_active: Optional[boolean]
    registered_at: Optional[datetime]


class SchoolCreate(SchoolBase):
    pass


class SchoolRes(BaseModel):
    id: int
    name: str
    description: str
    manager_id: int
    # manager:  ManagerRes

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
