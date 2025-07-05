from repository.database.librarian import LibrarianRepository
from core.models.librarian import Librarian
from core.schemas.librarian import RegisterLibrarian, ResponseLibrarian
from utils.auth_jwt import hash_password, verefy_passowrd
from repository.exception import ClientException

class LibrarianService:
    def __init__(self, session):
        self.repo = LibrarianRepository(model=Librarian, session=session)

    async def create_librarian(
        self, 
        librarian: RegisterLibrarian
    ) -> ResponseLibrarian:
        librarian.password = hash_password(librarian.password)
        db_librarian = await self.repo.create_librarian(
            email=librarian.email,
            passowrd=librarian.password
        )
        return ResponseLibrarian.model_validate(db_librarian)
    
    async def authenticate(
        self, 
        email: str, 
        passowrd: str
    ) -> ResponseLibrarian:
        db_librarian = await self.repo.get_by_email(email=email)
        if verefy_passowrd(
            payload_password=passowrd, 
            hashed_password=db_librarian.password_hash
        ):
            return ResponseLibrarian.model_validate(db_librarian)
        raise ClientException

    async def get_with_reader(
        self, 
        librarian_id: int
    ) -> ResponseLibrarian:
        db_librarian = await self.repo.get_with_readers(librarian_id=librarian_id)
        return ResponseLibrarian.model_validate(db_librarian)