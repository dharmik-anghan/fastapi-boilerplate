from fastapi import FastAPI
from route.user.api import user_router

app = FastAPI()

app.include_router(user_router, prefix="/api/user")