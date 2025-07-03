from pydantic_settings import BaseSettings
from pydantic import BaseModel
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent

class JWTConfig(BaseModel):
    public_key: Path = BASE_DIR / "secret" / "jwt-public.pem" 
    secret_key: Path = BASE_DIR / "secret" / "jwt-privet.pem"
    alghorithm: str = "RS256"
    access_token_expire_minute: int = 1

class DataBaseConfig(BaseModel):
    url: str = "sqlite+aiosqlite:///database.db"
    echo: bool = False
    max_overflow: int = 10
    pool_pre_ping: bool = True
    pool_recycle: int = 3600 

class ServerConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000

class Settings(BaseSettings):
    jwt: JWTConfig = JWTConfig()
    db: DataBaseConfig = DataBaseConfig()
    server: ServerConfig = ServerConfig()

config = Settings()