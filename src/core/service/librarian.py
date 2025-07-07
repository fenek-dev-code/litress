from repository.database.librarian import LibrarianRepository
from core.models.librarian import Librarian
from core.schemas.librarian import RegisterLibrarian, LibrarianResponse, LibrarianWithReadersResponse, UpdateLibrarian
from utils.auth_jwt import hash_password, verefy_passowrd
from repository.exception import ClientException

class LibrarianService:
    def __init__(self, session):
        self.repo = LibrarianRepository(model=Librarian, session=session)

    async def get_by_id(self, id: int):
        await self.repo.get(id)

    async def create_librarian(
        self, 
        librarian: RegisterLibrarian
    ) -> LibrarianResponse:
        librarian.password = hash_password(librarian.password)
        db_librarian = await self.repo.create_librarian(**librarian.model_dump())
        return LibrarianResponse.model_validate(db_librarian)
    
    async def update_librarian(self, id: int, data: UpdateLibrarian) -> LibrarianResponse:
        db_librarian =  await self.repo.update_librarian(
            id=id, data=data.model_dump()
        )
        return LibrarianResponse.model_validate(db_librarian)
        

    async def authenticate(
        self, 
        email: str, 
        password: str
    ) -> LibrarianResponse:
        db_librarian = await self.repo.get_by_email(email=email)
        if verefy_passowrd(
            payload_password=password, 
            hashed_password=db_librarian.password_hash
        ):
            return LibrarianResponse.model_validate(db_librarian)
        raise ClientException

    async def get_with_reader(
        self, 
        librarian_id: int
    ) -> LibrarianWithReadersResponse:
        db_librarian = await self.repo.get_with_readers(librarian_id=librarian_id)
        return LibrarianWithReadersResponse.model_validate(db_librarian)