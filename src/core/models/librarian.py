from sqlalchemy import String, LargeBinary, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .base import Base


class Librarian(Base):
    __tablename__ = "librarians"  # Changed to plural for convention

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[bytes] = mapped_column(LargeBinary(60), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    readers: Mapped[list["Reader"]] = relationship(back_populates="librarian")
    books: Mapped[list["Book"]] = relationship(back_populates="librarian")
    
    __table_args__ = (
        {'sqlite_autoincrement': True}
    )