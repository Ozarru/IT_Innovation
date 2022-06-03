from fastapi import FastAPI
from .routers import manager, school, edu_stage, classroom, course, user, auth, staff, student
from .admin import superuser
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

app.include_router(school.router)
app.include_router(classroom.router)
app.include_router(course.router)
app.include_router(user.router)
app.include_router(edu_stage.router)
app.include_router(auth.router)
app.include_router(manager.router)
app.include_router(student.router)
app.include_router(staff.router)
app.include_router(superuser.router)


@app.get("/")
async def root():
    return {"message": "Academia"}
