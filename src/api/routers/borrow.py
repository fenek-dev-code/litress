from fastapi import APIRouter, Depends, HTTPException, status
from core.schemas.token import TokenData
from core.service.borrow import BorrowService
from repository.exception import (
    NotFoundException, ClientException,
    BaseException, LimmitException
)
from core.schemas.borrow import (
    BorrowBookCreate, BorrowBookResponse, BorrowBookReturn,
    BorrowBooksBase, ShortBorrowResponse, BorrowWithBook,
    BorrowFilter
)
from api.deps import borrow_service, currnet_user


router = APIRouter(
    prefix="/borrow",
    tags=['Borrow']
)


@router.post(
    "/record",
    status_code=status.HTTP_200_OK
)
async def borrow_book(
    borrow: BorrowBooksBase,
    service: BorrowService = Depends(borrow_service),
    token: TokenData = Depends(currnet_user)
) -> BorrowBookResponse:
    try:
        return await service.borrow_book(borrow=borrow, librarian_id=token.sub)
    except NotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="meessage"
        )
    except BaseException:
        raise HTTPException(
            status_code=500
        )
    except LimmitException:
        raise HTTPException(
            status_code=500
        )

@router.post(
    "/return",
    status_code=status.HTTP_200_OK
)
async def return_book(
    borrow_data: BorrowBookReturn,
    token: TokenData = Depends(currnet_user),
    service: BorrowService = Depends(borrow_service)
) -> BorrowWithBook:
    try:
        return await service.return_book(borrow=borrow_data)
    except BaseException:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="server Error"
        ) 
    except NotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found borrow"
        )

@router.get(
    "/{borrow_id}",
    status_code=status.HTTP_200_OK
)
async def get_borrow(
    borrow_id: int,
    token: TokenData = Depends(currnet_user),
    service: BorrowService = Depends(borrow_service)
) -> BorrowWithBook:
    try:
        return await service.get_borrow_by_id(borrow_id)
    except NotFoundException as err:
        raise HTTPException(
            status_code=err.status_code,
            detail="Not found"
        )
    except BaseException as err:
        raise HTTPException(
            status_code=err.status_code,
            detail="Server error"
        )
    
@router.get(
    "",
    status_code=status.HTTP_200_OK
)
async def get_borrow_records(
    filter: BorrowFilter,
    token: TokenData = Depends(currnet_user),
    service: BorrowService = Depends(borrow_service),
):
    try:
        return await service.get_borrow_records(filter)
    except:
        pass

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
    try:
        return await service.get_all_borrow(offset=offset, limit=limit)
    except:
        pass