from fastapi import APIRouter, status, HTTPException, Depends
from core.service.reader import ReaderService
from core.schemas.token import TokenData
from core.schemas.reader import (
    ReaderWithRecordsResponse, ResponseReader, ResponseReaderWithBooks, CreateReader, 
    BaseReader, ShortBookResponse, ShortBorrowResponse, ShortReaderResponse
)
from api.deps import currnet_user, reader_service


router = APIRouter(
    prefix="/reader",
    tags=['Readers']
)

@router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
async def create_reader(
    reader: CreateReader,
    service: ReaderService = Depends(reader_service),
    token_data: TokenData = Depends(currnet_user)
) -> ShortReaderResponse:
    return await service.create_reader(reader, token_data.sub)


@router.get(
    "",
    status_code=status.HTTP_200_OK
)
async def get_readers(
    offset: int, limit: int,
    service: ReaderService = Depends(reader_service),
    token: TokenData = Depends(currnet_user)
):
    return await service.get_readers(offset, limit)


@router.get(
    "/{reader_id}",
    status_code=status.HTTP_200_OK
)
async def get_reader(
    reader_id: int,
    service: ReaderService = Depends(reader_service),
    token_data: TokenData = Depends(currnet_user)
) -> ReaderWithRecordsResponse:
    return await service.get_with_borro(reader_id=reader_id)

@router.get(
    "/{reader_id}/books",
    status_code=status.HTTP_200_OK
)
async def get_reader_with_books(
    reader_id: int,
    token: TokenData = Depends(currnet_user),
    service: ReaderService = Depends(reader_service)
) -> ResponseReaderWithBooks:
    return await service.get_with_borrow_books(reader_id=reader_id)
