from sqlalchemy import String, LargeBinary, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .base import Base
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .reader import Reader
    from .order import BorrowRecord


class Librarian(Base):
    __tablename__ = "librarians"  

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[bytes] = mapped_column(LargeBinary(60), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    
    readers: Mapped[list["Reader"]] = relationship(back_populates="librarian") 
    issued_books: Mapped[List["BorrowRecord"]] = relationship(
        back_populates="librarian"
    )
    __table_args__ = (
        {'sqlite_autoincrement': True}
    )