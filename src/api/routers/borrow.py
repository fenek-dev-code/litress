from fastapi import APIRouter, Depends, HTTPException, status
from core.schemas.token import TokenData
from core.service.borrow import BorrowService
from repository.exception import (
    NotFoundException, ClientException,
    BaseException, LimmitException
)
from core.schemas.borrow import (
    BorrowBookCreate, BorrowBookResponse, BorrowBookReturn,
    BorrowBooksBase, ShortBorrowResponse, BorrowWithBook
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
async def create_borrow(
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