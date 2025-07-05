from fastapi import APIRouter, status, HTTPException, Depends
from api.deps import book_service, librarian_service
from core.schemas.librarian import LogInLibrarian, LibrarianTokenResponse, ResponseLibrarian, RegisterLibrarian
from core.schemas.reader import CreateReader, ResponseReader, UpdateReader, ShortReaderResponse
from repository.exception import ConflictException, BaseException, NotFoundException, UnauthorizedException, LimmitException



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
   
):
    pass 

@router.post(
    "/token",
    status_code=status.HTTP_200_OK,
    response_model=LibrarianTokenResponse
)
async def login_user(
    user: LogInLibrarian,
    
):
    pass
    
@router.post(
    "/reader",
    status_code=status.HTTP_201_CREATED
)
async def create_reader(
    reader: CreateReader,
    service = Depends(book_service)
):
    pass