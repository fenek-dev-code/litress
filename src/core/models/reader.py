from typing import List  
from datetime import datetime
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from .base import Base

class Reader(Base):
    __tablename__ = "readers"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    books: Mapped[List["Book"]] = relationship(back_populates="reader") 
    librarian_id: Mapped[int] = mapped_column(Integer, ForeignKey("librarians.id"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    librarian: Mapped["Librarian"] = relationship(back_populates="readers")