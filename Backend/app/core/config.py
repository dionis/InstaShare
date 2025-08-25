from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "InstaShare-backend"
    PROJECT_VERSION: str = "0.1.0"

    DATABASE_URL: str
    SUPABASE_URL: str
    SUPABASE_KEY: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
