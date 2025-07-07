from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from api.deps import librarian_service, currnet_user
from core.schemas.token import Token, TokenData
from core.schemas.librarian import (
    LibrarianWithReadersResponse, LogInLibrarian,  
    LibrarianResponse, RegisterLibrarian, UpdateLibrarian
)
from repository.exception import (
    BaseException, ClientException,
    ConflictException, NotFoundException
)

from core.service.librarian import LibrarianService
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
    
@router.patch(
    "/librarian",
    status_code=status.HTTP_202_ACCEPTED
)
async def update_librarian(
    data: UpdateLibrarian,
    token: TokenData = Depends(currnet_user),
    service: LibrarianService = Depends(librarian_service)
):
    try:
        return await service.update_librarian(token.sub, data)
    except (NotFoundException, BaseException) as err:
        raise HTTPException(
            status_code=err.status_code,
            detail="Не удалось обновить информацию"
        )


