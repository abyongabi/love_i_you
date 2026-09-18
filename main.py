from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.auth_router import router as auth_router
from app.goal_router import router as goal_router
from app.middleware.request_middleware import populate_request_context
from app.mission_router import router as mission_router
from app.user_router import router as user_router

app = FastAPI()


app.middleware("http")(populate_request_context)

app.include_router(auth_router, tags=["Auth"])
app.include_router(user_router, tags=["User"])
app.include_router(goal_router, tags=["Goal"])
app.include_router(mission_router, tags=["Mission"])

app.mount("/", StaticFiles(directory="static", html=True), name="static")
