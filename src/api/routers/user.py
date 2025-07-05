from fastapi import APIRouter, status, HTTPException, Depends
from api.deps import get_book_db, get_librarian_db
from core.schemas.librarian import LogInLibrarian, LibrarianTokenResponse, ResponseLibrarian, RegisterLibrarian
from core.schemas.reader import CreateReader, ResponseReader
from core.models.librarian import Librarian
from core.models.reader import Reader
from repository.database.librarian import LibrarianRepository
from repository.exception import NotFoundException, ConflictException, DataBaseErrorExceprion, LibraryException, UnauthorizedException
from utils.auth_jwt import encode_jwt

router = APIRouter(
    prefix='auth',
    tags=['Auth']
)

@router.post(
    "/regiser",
    status_code=status.HTTP_201_CREATED
)
async def create_librarian(
    user: RegisterLibrarian,
    db: LibrarianRepository = Depends(get_librarian_db)
):
    try:
        new_user = await db.create_librarian(Librarian(**user.dict()))
        return ResponseLibrarian.from_orm(new_user)
    except ConflictException as e:
        HTTPException(
            status_code=e.status_code,
            detail="Email is busy"
        )

@router.post(
    "/token",
    status_code=status.HTTP_200_OK,
    response_model=LibrarianTokenResponse
)
async def login_user(
    user: LogInLibrarian,
    db: LibrarianRepository = Depends(get_librarian_db)
):
    try:
        user = await db.login_librarian(user.email, user.password)
        return LibrarianTokenResponse(access_token=encode_jwt(
            {"sub": str(user.id)}
        ))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="login or password incorect"
        )
    
@router.post(
    "/reader",
    status_code=status.HTTP_201_CREATED
)
async def create_reader(
    reader: CreateReader,
    db: LibrarianRepository = Depends()
):
    pass