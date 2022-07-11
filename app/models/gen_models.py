from datetime import datetime, timezone
from ..config.database import Base
from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP


# --------------------------------association tables---------------------------


# class_attendance_assoc = Table(
#     "assoc_class_attendance",
#     Base.metadata,
#     Column("attendance_id", ForeignKey('class_attendances.id'), unique=True),
#     Column("attendance", ForeignKey('students.matric_id'), unique=True),
# )

# exam_attendance_assoc = Table(
#     "assoc_exam_attendance",
#     Base.metadata,
#     Column("attendance_id", ForeignKey('exam_attendances.id'), unique=True),
#     Column("student_matric", ForeignKey('students.matric_id'), unique=True),
# )

# payment_assoc = Table(
#     "assoc_payment",
#     Base.metadata,
#     Column("payment_id", ForeignKey('payments.id'), unique=True),
#     Column("student_matric", ForeignKey('students.matric_id'), unique=True),
# )

exam_stats_assoc = Table(
    "assoc_exam_stats",
    Base.metadata,
    Column("exam_id", ForeignKey('exams.id'), unique=True),
    Column("student_matric", ForeignKey('students.matric_id'), unique=True),
)

parent_assoc = Table(
    "assoc_parent",
    Base.metadata,
    Column("parent_email", ForeignKey('parents.email'), unique=True),
    Column("student_email", ForeignKey('students.email'), unique=True),
)

# ----------------super models---------------


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


class EduStage(Base):
    __tablename__ = 'edu_stages'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)


class EduPhase(Base):
    __tablename__ = 'edu_phases'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    edu_stage_id = Column(Integer, ForeignKey(
        'edu_stages.id', ondelete="CASCADE"), nullable=False)
    edu_stage = relationship('EduStage', backref="edu_phases")


class Grade(Base):
    __tablename__ = 'grades'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    edu_phase_id = Column(Integer, ForeignKey(
        'edu_phases.id', ondelete="CASCADE"), nullable=False)
    edu_phase = relationship('EduPhase', backref="grades")


class AcademicYear(Base):
    __tablename__ = 'academic_years'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    start_date = Column(String, nullable=False)
    end_date = Column(String, nullable=False)
    # start_date = Column(datetime.daete, nullable=False)
    # end_date = Column(datetime.daete, nullable=False)


class TermGenre(Base):
    __tablename__ = 'term_genres'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, unique=True, nullable=False)


class Day(Base):
    __tablename__ = 'days'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, unique=True, nullable=False)


class TimetableGenre(Base):
    __tablename__ = 'timetable_genres'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)


# ----------------users models---------------


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
    matric = Column(Integer, unique=True, nullable=True)
    is_staff = Column(Boolean, server_default='true', nullable=False)
    email = Column(String, ForeignKey(
        'users.email', ondelete="CASCADE"), primary_key=True, unique=True, nullable=False)
    user = relationship('User', backref=backref("staff", uselist=False))


# ----------------school models---------------
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


class Classe(Base):
    __tablename__ = 'classes'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    alias = Column(String, nullable=True)
    class_size = Column(Integer, nullable=False, default=0)
    grade_id = Column(Integer, ForeignKey(
        'grades.id', ondelete="CASCADE"), nullable=False)
    supervisor_mail = Column(String, ForeignKey(
        'staff.email', ondelete="CASCADE"), nullable=True)
    school_id = Column(Integer, ForeignKey(
        'schools.id', ondelete="CASCADE"), nullable=False)
    grade = relationship('Grade', backref="classes")
    supervisor = relationship(
        'Staff', backref=backref("grades", uselist=False))
    school = relationship('School', backref="classes")


class Term(Base):
    __tablename__ = 'terms'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    start_date = Column(String, nullable=False)
    end_date = Column(String, nullable=False)
    # start_date = Column(datetime.daete, nullable=False)
    # end_date = Column(datetime.daete, nullable=False)
    term_genre_id = Column(Integer, ForeignKey(
        'term_genres.id', ondelete="CASCADE"), nullable=False)
    term_genre = relationship('TermGenre', backref="terms")


class Timetable(Base):
    __tablename__ = 'timetables'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    timetable_genre_id = Column(Integer, ForeignKey(
        'timetable_genres.id', ondelete="CASCADE"), nullable=False)
    timetable_genre = relationship('TimetableGenre', backref="timetables")
    classe_id = Column(Integer, ForeignKey(
        'classes.id', ondelete="CASCADE"), nullable=False)
    classe = relationship('Classe', backref="timetables")
    term_id = Column(Integer, ForeignKey(
        'terms.id', ondelete="CASCADE"), nullable=False)
    term = relationship('Term', backref="timetables")
    academic_year_id = Column(Integer, ForeignKey(
        'academic_years.id', ondelete="CASCADE"), nullable=False)
    academic_year = relationship('AcademicYear', backref="timetables")


# ------------------------------------Classes-----------------------------

class SchoolWeek(Base):
    __tablename__ = 'school_weeks'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    start_day = Column(String, nullable=False)
    end_day = Column(String, nullable=False)
    timetable_id = Column(Integer, ForeignKey(
        'timetables.id', ondelete="CASCADE"), nullable=False)
    timetable = relationship('Timetable', backref="school_weeks")


class SchoolDay(Base):
    __tablename__ = 'school_days'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    day_id = Column(Integer, ForeignKey(
        'days.id', ondelete="CASCADE"), nullable=False)
    day = relationship('Day', backref="school_days")
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
    # start_time = Column(datetime.houer, nullable=False)
    # end_time = Column(datetime.houer, nullable=False)
    timetable_id = Column(Integer, ForeignKey(
        'timetables.id', ondelete="CASCADE"), nullable=False)
    timetable = relationship('Timetable', backref="school_days")


class Subject(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    syllabus = Column(String, nullable=True)
    coefficient = Column(Integer, nullable=False, default=1)
    classe_id = Column(Integer, ForeignKey(
        'classes.id', ondelete="CASCADE"), nullable=False)
    classe = relationship('Classe', backref="subjects")
    term_id = Column(Integer, ForeignKey(
        'terms.id', ondelete="CASCADE"), nullable=False)
    term = relationship('Term', backref="subjects")
    teacher_mail = Column(String, ForeignKey(
        'staff.email', ondelete="CASCADE"), nullable=False)
    teacher = relationship('Staff', backref="subjects")


class Period(Base):
    __tablename__ = 'periods'

    id = Column(Integer, primary_key=True, autoincrement=True,
                unique=True,  nullable=False)
    name = Column(String, nullable=False)
    duration = Column(Float, nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
    # start_time = Column(datetime.houer, nullable=False)
    # end_time = Column(datetime.houer, nullable=False)
    school_day_id = Column(Integer, ForeignKey(
        'school_days.id', ondelete="CASCADE"), nullable=False)
    school_day = relationship('SchoolDay', backref="periods")
    subject_id = Column(Integer, ForeignKey(
        'subjects.id', ondelete="CASCADE"), primary_key=True, unique=True, nullable=False)
    subject = relationship(
        'Subject', backref=backref("periods", uselist=False))


class ClassAttendance(Base):
    __tablename__ = 'class_attendances'

    id = Column(Integer, primary_key=True, autoincrement=True,
                unique=True,  nullable=False)
    period_id = Column(Integer, ForeignKey(
        'periods.id',  ondelete="CASCADE"), nullable=True)
    student_matric = Column(Integer, ForeignKey(
        'students.matric_id', ondelete="CASCADE"), nullable=False)
    observation = Column(String, nullable=True)
    is_present = Column(Boolean, server_default='false', nullable=False)
    period = relationship(
        'Period', backref=backref("class_attendances", uselist=False))
    student = relationship(
        'Student', backref=backref("class_attendances", uselist=False))
    date = Column(String, server_default=text('now()'), nullable=False)
    # date = Column(datetime.today, server_default=text('now()'), nullable=False)


# class AttendanceRecap(Base):
#     __tablename__ = 'attendance_recaps'

#     student_matric = Column(Integer, ForeignKey(
#         'students.matric_id', primary_key=True, ondelete="CASCADE"), nullable=False)
#     times_seen = Column(Integer, server_default='0', nullable=False)
#     times_missed = Column(Integer, server_default='0', nullable=False)
#     percentage = Column(Float, server_default='0', nullable=False)
#     student = relationship(
#         'Student', backref=backref("attendance_recaps", uselist=False))
#     class_attendances = relationship(
#         "ClassAttendance", secondary=class_attendance_assoc, back_populates="attendance_recaps"
#     )

# ------------------------------------Exams-----------------------------


class ExamDay(Base):
    __tablename__ = 'exam_days'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    day_id = Column(Integer, ForeignKey(
        'days.id', ondelete="CASCADE"), nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
    timetable_id = Column(Integer, ForeignKey(
        'timetables.id', ondelete="CASCADE"), nullable=False)
    # start_time = Column(datetime.houer, nullable=False)
    # end_time = Column(datetime.houer, nullable=False)
    day = relationship('Day', backref="exam_days")
    timetable = relationship('Timetable', backref="exam_days")


class Exam(Base):
    __tablename__ = 'exams'

    id = Column(Integer, primary_key=True, autoincrement=True,
                unique=True,  nullable=False)
    name = Column(String, nullable=False)
    duration = Column(Float, nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
    subject_id = Column(Integer, ForeignKey(
        'subjects.id', ondelete="CASCADE"), primary_key=True, unique=True, nullable=False)
    exam_day_id = Column(Integer, ForeignKey(
        'exam_days.id', ondelete="CASCADE"), nullable=False)
    # start_time = Column(datetime.houer, nullable=False)
    # end_time = Column(datetime.houer, nullable=False)
    exam_day = relationship('ExamDay', backref="exams")
    subject = relationship(
        'Subject', backref=backref("exams", uselist=False))


class ExamAttendance(Base):
    __tablename__ = 'exam_attendances'

    id = Column(Integer, primary_key=True, autoincrement=True,
                unique=True,  nullable=False)
    exam_id = Column(Integer, ForeignKey(
        'exams.id', primary_key=True,  ondelete="CASCADE"), nullable=False)
    student_matric = Column(Integer, ForeignKey(
        'students.matric_id', primary_key=True, ondelete="CASCADE"), nullable=False)
    observation = Column(String, nullable=True)
    is_present = Column(Boolean, server_default='false', nullable=False)
    exam = relationship('Exam', backref="exam_attendances")
    student = relationship('Student', backref="exam_attendances")


class ExamGrade(Base):
    __tablename__ = 'exam_grades'

    id = Column(Integer, primary_key=True, autoincrement=True,
                unique=True, nullable=False)
    exam_id = Column(Integer, ForeignKey(
        'exams.id', primary_key=True,   ondelete="CASCADE"), nullable=False)
    student_matric = Column(Integer, ForeignKey(
        'students.matric_id', primary_key=True, ondelete="CASCADE"), nullable=False)
    score = Column(Float, nullable=True, server_default='0')
    observation = Column(String, nullable=True)
    student = relationship('Student', backref="exam_grades")
    exam = relationship('Exam', backref="exam_grades")


class ExamStats(Base):
    __tablename__ = 'exam_stats'

    id = Column(Integer, primary_key=True, unique=True,
                autoincrement=True, nullable=False)
    exam_id = Column(Integer, ForeignKey(
        'exams.id', ondelete="CASCADE"), nullable=False)
    candidates = Column(Integer, nullable=True, server_default='0')
    highest_score = Column(Float, nullable=True, server_default='0')
    lowest_score = Column(Float, nullable=True, server_default='0')
    average_score = Column(Float, nullable=True, server_default='0')
    success_rate = Column(Float, nullable=True, server_default='0')
    failure_rate = Column(Float, nullable=True, server_default='0')
    observations = Column(String, nullable=True,
                          server_default='Nothing to report')
    exam = relationship('Exam', backref=backref(
        "exam_stats", uselist=False))


# ------------------------------------Payment-----------------------------

class Fee(Base):
    __tablename__ = 'fees'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    grade_id = Column(Integer, ForeignKey(
        'grades.id', ondelete="CASCADE"), nullable=True)
    grade = relationship('Grade', backref="fees")
    name = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)


class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, unique=True,
                autoincrement=True, nullable=False)
    fee_id = Column(Integer, ForeignKey(
        'fees.id', ondelete="CASCADE"), nullable=False)
    student_matric = Column(Integer, ForeignKey(
        'students.matric_id', ondelete="CASCADE"), unique=True, nullable=False)
    amount_payed = Column(Integer, nullable=False)
    amount_due = Column(Integer, nullable=True, server_default='0')
    fee = relationship('Fee', backref="payments")
    student = relationship('Student', backref=backref(
        "payments", uselist=False))


class Parent(Base):
    __tablename__ = 'parents'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    is_parent = Column(Boolean, server_default='true', nullable=False)
    email = Column(String, ForeignKey(
        'users.email', ondelete="CASCADE"), primary_key=True, unique=True, nullable=False)
    user = relationship('User', backref=backref("parent", uselist=False))
    students = relationship(
        "Student", secondary=parent_assoc, back_populates="parents"
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
        "Parent", secondary=parent_assoc, back_populates="students"
    )
    # payments = relationship(
    #     "Payment", secondary=payment_assoc, back_populates="students"
    # )
    # exam_attendances = relationship(
    #     "ExamAttendance", secondary=exam_attendance_assoc, back_populates="students"
    # )
    # classe_attendances = relationship(
    #     "ClassAttendance", secondary=class_attendance_assoc, back_populates="students"
    # )
    classe_id = Column(Integer, ForeignKey(
        'classes.id', ondelete="CASCADE"), nullable=True)
    classe = relationship('Classe', backref=backref("student", uselist=False))
