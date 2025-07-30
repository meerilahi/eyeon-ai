from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    firebase_creds_path: str
    firebase_project_id: str
    OPENAI_API_KEY : str

    class Config:
        env_file = ".env"

settings = Settings()
