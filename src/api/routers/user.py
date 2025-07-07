from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from api.deps import book_service, librarian_service, reader_service, currnet_user
from core.schemas.token import Token, TokenData
from core.schemas.librarian import LibrarianWithReadersResponse, LogInLibrarian,  LibrarianResponse, RegisterLibrarian
from core.schemas.reader import CreateReader, ResponseReader, UpdateReader, ShortReaderResponse, ReaderWithRecordsResponse, ResponseReaderWithBooks
from repository.exception import ConflictException, BaseException, NotFoundException, UnauthorizedException, LimmitException, ClientException

from core.service.librarian import LibrarianService
from core.service.reader import ReaderService

from utils.auth_jwt import encode_jwt

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

@router.post(
    "/regiser",
    status_code=status.HTTP_201_CREATED
)
async def create_librarian(
    user: RegisterLibrarian,
    service: LibrarianService = Depends(librarian_service)
) -> LibrarianResponse:
    try:
        result = await service.create_librarian(user)
        return result
    
    except ConflictException as err:
        HTTPException(
            status_code=err.status_code,
            detail="Пользователь с таким Email уже зарегистрирован"
        )

@router.get(
    "/librarian",
    status_code=status.HTTP_200_OK
)
async def get_librarian(
    token: TokenData = Depends(currnet_user),
    service: LibrarianService = Depends(librarian_service)
) -> LibrarianWithReadersResponse:
    try:
        return await service.get_with_reader(token.sub)
    except NotFoundException as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    except BaseException as err:
        raise HTTPException(
            status_code=err.status_code,
            detail="Server Error"
        )

@router.post(
    "/token",
    status_code=status.HTTP_200_OK
)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: LibrarianService = Depends(librarian_service)  
) -> Token:
    try:
        result = await service.authenticate(form_data.username, form_data.password)
        token = encode_jwt(payload={
            "sub":result.id,
            "role":"librarian"
        })
        return Token(
            access_token=token
        )
    except (ClientException, NotFoundException) as err:
        raise HTTPException(
            status_code=err.status_code,
            detail="Не верный логин или пароль"
        )
    
@router.post(
    "/reader",
    status_code=status.HTTP_201_CREATED
)
async def create_reader(
    reader: CreateReader,
    service: ReaderService = Depends(reader_service),
    token_data: TokenData = Depends(currnet_user)
) -> ShortReaderResponse:
    try:
        result = await service.create_reader(reader, token_data.sub)
        return result
    except ConflictException as err:
        raise HTTPException(
            status_code=err.status_code,
            detail="Читатель с таким Email уже есть"
        )
    except BaseException as err:
        raise HTTPException(
            status_code=err.status_code,
            detail="Ошибка сервера повторите запрос"
        )

@router.get(
    "/reader/{reader_id}",
    status_code=status.HTTP_200_OK
)
async def get_reader(
    reader_id: int,
    service: ReaderService = Depends(reader_service),
    token_data: TokenData = Depends(currnet_user)
) -> ReaderWithRecordsResponse:
    try:
        result = await service.get_with_borrow_books(reader_id=reader_id)
        return result
    except NotFoundException as err:
        raise HTTPException(
            status_code=err.status_code
        )
    
@router.get(
    "/reader/{reader_id}/books",
    status_code=status.HTTP_200_OK
)
async def get_reader_with_books(
    reader_id: int,
    token: TokenData = Depends(currnet_user),
    service: ReaderService = Depends(reader_service)
) -> ResponseReaderWithBooks:
    try:
        return await service.get_with_borrow_books(reader_id=reader_id)
    except NotFoundException as err:
        raise HTTPException(
            status_code=err.status_code,
            detail="Not found reader"
        )