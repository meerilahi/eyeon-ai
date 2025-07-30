import contextlib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.chat import router as chat_router
from app.firebase.firebase_init import init_firebase
# from app.core.scheduler import start_loops

@contextlib.asynccontextmanager
async def startup_event(app: FastAPI):
    init_firebase()
    # await start_loops()
    yield

app = FastAPI(
    title="EyeOn AI Backend",
    description="AI-powered surveillance backend with LangGraph chatbot, VLM analysis, and alert system.",
    version="1.0.0",
    lifespan=startup_event,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/chat", tags=["Chat"])

@app.get("/")
def read_root():
    return {"status": "EyeOn AI backend running"}
