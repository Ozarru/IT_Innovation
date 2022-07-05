from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from .gen_schemas import *

# ------------------year schemas---------------------


class AcadYearCreate(BaseModel):
    name: str
    start_date: str
    end_date: str


class AcadYearRes(BaseModel):
    id: int
    name: str
    school_id: int
    school: "SchoolRes"

    class Config:
        orm_mode = True


# ------------------term schemas---------------------
class AcadTermCreate(BaseModel):
    name: str
    start_date: str
    end_date: str
    edu_phase_id: int


class AcadTermRes(BaseModel):
    id: int
    name: str
    school_id: int
    school: "SchoolRes"
    edu_phase: "EduPhaseRes"

    class Config:
        orm_mode = True


# ------------------timetable schemas---------------------
class TimetableCreate(BaseModel):
    genre: str
    grade_id: int
    term_id: int
    academic_year_id: int


class TimetableRes(BaseModel):
    id: int
    genre: str
    grade: "GradeRes"
    term: AcadTermRes
    academic_year: AcadYearRes

    class Config:
        orm_mode = True


# ------------------day schemas---------------------
class AcadDayCreate(BaseModel):
    name: str
    start_time: str
    end_time: str
    timetable_id: int


class AcadDayRes(BaseModel):
    id: int
    name: str
    start_time: str
    end_time: str
    timetable: TimetableRes

    class Config:
        orm_mode = True


# ------------------period schemas---------------------
class PeriodCreate(BaseModel):
    name: str
    duration: float
    start_time: str
    end_time: str
    subject_id: int
    academic_day_id: int


class PeriodRes(BaseModel):
    id: int
    name: str
    duration: float
    start_time: str
    end_time: str
    subject: "SubjectRes"
    academic_day: AcadDayRes

    class Config:
        orm_mode = True


# ------------------exam schemas---------------------
class ExamDayCreate(BaseModel):
    name: str
    start_time: str
    end_time: str
    timetable_id: int


class ExamDayRes(BaseModel):
    id: int
    name: str
    start_time: str
    end_time: str
    timetable: TimetableRes

    class Config:
        orm_mode = True


# -----------------------------
class ExamCreate(BaseModel):
    genre: str
    name: str
    duration: float
    start_time: str
    end_time: str
    subject_id: int
    exam_day_id: int


class ExamRes(BaseModel):
    id: int
    genre: str
    name: str
    duration: float
    start_time: str
    end_time: str
    subject: "SubjectRes"
    exam_day: ExamDayRes

    class Config:
        orm_mode = True


# -------------------------
class ExamAttendanceCreate(BaseModel):
    remark: Optional[str]
    exam_id: int
    date: datetime


class ExamAttendanceRes(BaseModel):
    id: int
    is_present: bool
    remark: str
    exam: ExamRes
    date: datetime
    students: "list[StudentRes]"

    class Config:
        orm_mode = True


# -------------------------
class ExamGradeCreate(BaseModel):
    score: float
    remark: Optional[str]
    exam_id: int
    student_matric: int


class ExamGradeRes(BaseModel):
    id: int
    remark: str
    exam: ExamRes
    student: "StudentRes"

    class Config:
        orm_mode = True


# -------------------------
class ExamStatsCreate(BaseModel):
    candidates: int
    highest_score: float
    lowest_score: float
    average_score: float
    success_rate: float
    failure_rate: float
    observations: str
    exam_id: int


class ExamStatsRes(BaseModel):
    id: int
    candidates: int
    highest_score: float
    lowest_score: float
    average_score: float
    success_rate: float
    failure_rate: float
    observations: str
    exam: ExamRes
    students: "list[StudentRes]"

    class Config:
        orm_mode = True


# -------------------------
class FeeCreate(BaseModel):
    name: str
    amount: int
    grade_id: int


class FeeRes(BaseModel):
    id: int
    name: str
    amount: int
    grade: "GradeRes"

    class Config:
        orm_mode = True

# -------------------------


class PaymentCreate(BaseModel):
    fee_id: int
    student_matric: int
    amount_payed: int
    amount_due: int


class PaymentRes(BaseModel):
    id: int
    fee: FeeRes
    amount_payed: int
    amount_due: int
    student: "StudentRes"

    class Config:
        orm_mode = True
