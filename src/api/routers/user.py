from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from api.deps import librarian_service, currnet_user
from core.schemas.token import Token, TokenData
from core.schemas.librarian import (
    LibrarianWithReadersResponse, LogInLibrarian,  
    LibrarianResponse, RegisterLibrarian, UpdateLibrarian
)
from typing import Annotated

from core.service.librarian import LibrarianService
from utils.auth_jwt import encode_jwt

router = APIRouter(
    prefix='/librarian',
    tags=['Librarian']
)

@router.post(
    "/regiser",
    status_code=status.HTTP_201_CREATED,
    summary="Create User"
)
async def create_librarian(
    user: RegisterLibrarian,
    service: LibrarianService = Depends(librarian_service)
) -> LibrarianResponse:
    return await service.create_librarian(user)

@router.get(
    "",
    status_code=status.HTTP_200_OK
)
async def get_librarian(
    token: TokenData = Depends(currnet_user),
    service: LibrarianService = Depends(librarian_service)
) -> LibrarianWithReadersResponse:
    return await service.get_with_reader(token.sub)

@router.post(
    "/token",
    status_code=status.HTTP_200_OK
)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: LibrarianService = Depends(librarian_service)  
) -> Token:
    result = await service.authenticate(form_data.username, form_data.password)
    token = encode_jwt(payload={
        "sub":result.id,
        "role":"librarian"
    })
    return Token(
        access_token=token
    )

    
@router.patch(
    "",
    status_code=status.HTTP_202_ACCEPTED
)
async def update_librarian(
    data: Annotated[UpdateLibrarian, Depends()],
    token: TokenData = Depends(currnet_user),
    service: LibrarianService = Depends(librarian_service)
):
    return await service.update_librarian(token.sub, data)


