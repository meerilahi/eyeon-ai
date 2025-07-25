from fastapi import FastAPI
from backend.api import health
from backend.firebase.firebase_init import init_firebase
import contextlib


@contextlib.asynccontextmanager
async def startup_event(app):
    init_firebase()
    print("✅ Firebase initialized")
    yield

app = FastAPI(title="EyeOn AI", lifespan=startup_event)

app.include_router(health.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "EyeOn AI backend running"}