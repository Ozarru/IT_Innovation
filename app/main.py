from fastapi import FastAPI
from .admin import superuser
from .functions import attendance, exam, grades, payment, timetable
from .routers import manager, school, edu_stage, edu_phase, grade, auth, staff, student, parent, subject
from .config import config
from fastapi.middleware.cors import CORSMiddleware


# # creates tables based on models on first run if the table doesn't exist yet
# models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

print(config.settings.database_name)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

# -----------Routes-------------------------------------------------------------------

# -------------authentication---------
app.include_router(auth.router)
# -------------users----------------
app.include_router(manager.router)
app.include_router(student.router)
app.include_router(parent.router)
app.include_router(staff.router)
app.include_router(superuser.router)
# -------------schools----------------
app.include_router(school.router)
app.include_router(edu_stage.router)
app.include_router(edu_phase.router)
app.include_router(grade.router)
app.include_router(subject.router)
# ----------functions--------------


@app.get("/")
async def root():
    return {"message": "Academia"}
