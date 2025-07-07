from fastapi import APIRouter, Depends, HTTPException, status
from core.service.book import BookService
from core.schemas.book import ShortBookResponse, ResponseBook, CreateBook
from repository.exception import NotFoundException, BaseException, UnauthorizedException
from api.deps import book_service, currnet_user
from core.schemas.token import TokenData

router = APIRouter(
    prefix="/book",
    tags=['Books']
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
async def create_book(
    book_data: CreateBook,
    service: BookService = Depends(book_service),
    token: TokenData = Depends(currnet_user)
) -> ResponseBook:
    try:
        return await service.create_book(book_data, token.sub)
    except BaseException as err:
        raise HTTPException(
            status_code=err.status_code,
            detail="Server Error"
        )

@router.get(
    "",
    status_code=status.HTTP_200_OK
)
async def get_books(
    offset: int = 0,
    limit: int = 25,
    service: BookService = Depends(book_service)
) -> list[ShortBookResponse]:
    try:
        return await service.get_books(offset=offset, limit=limit)
    except BaseException as err:
        raise HTTPException(
            status_code=err.status_code,
            detail="Server Error"
        )
    

@router.get(
    "/{book_id}",
    status_code=status.HTTP_200_OK
)
async def get_book_by_id(
    book_id: int,
    service: BookService = Depends(book_service)
) -> ShortBookResponse:
    try:
        return await service.get_book(id=book_id)
    except NotFoundException as err:
        raise HTTPException(
            status_code=err.status_code,
            detail="Not Found a Book"
        )
    except BaseException as err:
        raise HTTPException(
            status_code=err.status_code,
            detail="Server Error"
        )
