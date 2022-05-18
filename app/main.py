from fastapi import FastAPI
from .routers import school, classroom, course, user, auth
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
    allow_creddentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

# -----------Routes-------------------------------------------------------------------

app.include_router(school.router)
app.include_router(classroom.router)
app.include_router(course.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Academia"}
