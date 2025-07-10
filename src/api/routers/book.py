from fastapi import APIRouter, Depends, status
from core.service.book import BookService
from core.schemas.book import BookSearchFilters, ShortBookResponse, ResponseBook, CreateBook, UpdateBook, ResponseBookWithBorrow
from api.deps import book_service, currnet_user
from core.schemas.token import TokenData
from typing import Annotated

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

    return await service.create_book(book_data, token.sub)


@router.get(
    "",
    status_code=status.HTTP_200_OK
)
async def get_books(
    offset: int = 0,
    limit: int = 25,
    service: BookService = Depends(book_service)
) -> list[ShortBookResponse]:
    return await service.get_books(offset=offset, limit=limit)

    
@router.delete(
    "/{book_id}",
    status_code=status.HTTP_200_OK
)
async def delete_book(
    book_id: int,
    token: TokenData = Depends(currnet_user),
    service: BookService = Depends(book_service)
):
    return await service.delete_book(book_id=book_id)


@router.patch(
    "/{book_id}",
    status_code=status.HTTP_200_OK
)
async def update_book(
    book_id: int,
    book_data: UpdateBook,
    token: TokenData = Depends(currnet_user),
    service: BookService = Depends(book_service),
) -> ResponseBook:
    return await service.update_book(book_id=book_id, book=book_data)


@router.get(
    "/{book_id}",
    status_code=status.HTTP_200_OK
)
async def get_book_by_id(
    book_id: int,
    service: BookService = Depends(book_service)
) -> ShortBookResponse:
    return await service.get_book(id=book_id)

@router.get(
    "/{book_id}/borrow",
    status_code=status.HTTP_200_OK
)
async def book_with_borrow(
    book_id: int,
    token: TokenData = Depends(currnet_user),
    service: BookService = Depends(book_service)
) -> ResponseBookWithBorrow:
    return await service.get_book_with_borrow(book_id=book_id)

@router.get(
    "/search",
    status_code=status.HTTP_200_OK
)
async def search_book(
    search_params: BookSearchFilters,
    service: BookService = Depends(book_service)
) -> list[ShortBookResponse]:
    return await service.search_book(search_params) 
