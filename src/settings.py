from pydantic_settings import BaseSettings
from pydantic import BaseModel


class JWTConfig(BaseModel):
    pass

class ServerConfig(BaseModel):
    pass

class DataBaseConfig(BaseModel):
    pass

class Settings(BaseSettings):
    pass