from settings import config
from jose import jwt
from jose.exceptions import JWTError
from datetime import timedelta, timezone, datetime
import bcrypt

def encode_jwt(
    payload: dict,
    privet_key: str = config.jwt.secret_key.read_text(),
    alghorithm: str = config.jwt.alghorithm,
    access_token_expire_minutes: int = config.jwt.access_token_expire_minute,
    expire_time_delta: timedelta | None = None
) -> str:
    expire = datetime.now(timezone.utc) + (
        expire_time_delta if expire_time_delta 
        else timedelta(minutes=access_token_expire_minutes)
    )
    try:
        if "sub" in payload:
            payload['sub'] = str(payload['sub'])
        to_encode = payload.copy()
        to_encode.update({"exp": int(expire.timestamp())})
        return jwt.encode(
            to_encode,
            key=privet_key,
            algorithm=alghorithm
        )
    except JWTError as e:
        raise ValueError("Invalid token") from e

def decode_jwt(
    token: str,
    public_key: str = config.jwt.public_key.read_text(),
    alghorithm: str = config.jwt.alghorithm,
) -> dict:
    try:
        return jwt.decode(
            token=token,
            key=public_key,
            algorithms=[alghorithm]
        )
    except JWTError as e:
        raise ValueError("Invalid token") from e

        
def hash_password(
    payload_password: str
) -> str:
    salt  = bcrypt.gensalt()
    return bcrypt.hashpw(
        password=payload_password.encode(),
        salt=salt
    )

def verefy_passowrd(
    payload_password: str,
    hashed_password: str 
) -> bool:

    if not payload_password or not hashed_password:
        return False
    
    try:
        # Преобразуем в bytes если нужно
        pw_bytes = payload_password.encode('utf-8') if isinstance(payload_password, str) else payload_password
        hash_bytes = hashed_password.encode('utf-8') if isinstance(hashed_password, str) else hashed_password
        
        return bcrypt.checkpw(pw_bytes, hash_bytes)
    except (ValueError, TypeError, AttributeError):
        return False

