from fastapi import APIRouter, Depends, HTTPException, status
from core.schemas.token import TokenData
from core.service.borrow import BorrowService

from core.schemas.borrow import (
    BorrowBookCreate, BorrowBookReturn, BorrowFilter,
    BorrowBookResponse, BorrowWithBookAndReader, 
)
from api.deps import borrow_service, currnet_user


router = APIRouter(
    prefix="/borrow",
    tags=['Borrow']
)


@router.post(
    "",
    status_code=status.HTTP_200_OK
)
async def borrow_book(
    borrow: BorrowBookCreate,
    service: BorrowService = Depends(borrow_service),
    token: TokenData = Depends(currnet_user)
) -> BorrowBookResponse:
    return await service.borrow_book(borrow=borrow, librarian_id=token.sub)


@router.post(
    "/return",
    status_code=status.HTTP_200_OK
)
async def return_book(
    borrow_data: BorrowBookReturn,
    token: TokenData = Depends(currnet_user),
    service: BorrowService = Depends(borrow_service)
) -> BorrowBookResponse:
    return await service.return_book(borrow=borrow_data)


@router.get(
    "/{borrow_id}",
    status_code=status.HTTP_200_OK
)
async def get_borrow(
    borrow_id: int,
    token: TokenData = Depends(currnet_user),
    service: BorrowService = Depends(borrow_service)
) -> BorrowWithBookAndReader:

    return await service.get_borrow_by_id(borrow_id)

    
@router.get(
    "",
    status_code=status.HTTP_200_OK
)
async def get_borrow_records(
    filter: BorrowFilter,
    token: TokenData = Depends(currnet_user),
    service: BorrowService = Depends(borrow_service),
):
    return await service.get_borrow_records(filter)


@router.get(
    "/all",
    status_code=status.HTTP_200_OK
)
async def get_all_borrow(
    offset: int = 0,
    limit: int = 25,
    token: TokenData = Depends(currnet_user),
    service: BorrowService = Depends(borrow_service)
):
    return await service.get_all_borrow(offset=offset, limit=limit)
