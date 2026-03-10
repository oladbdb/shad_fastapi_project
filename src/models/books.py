from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel

if TYPE_CHECKING:  # only for type checkers
    from .sellers import Seller

COUNTER = 0  # Каунтер, иметирующий присвоение id в базе данных

# симулируем хранилище данных. Просто сохраняем объекты в память, в словаре.
# {0: {"id": 1, "title": "blabla", ...., "year": 2023}}
fake_storage = {}


# ORM
class Book(BaseModel):
    __tablename__ = "books_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    author: Mapped[str] = mapped_column(String(50), nullable=False)
    year: Mapped[int] = mapped_column(nullable=True)
    pages: Mapped[int]
    seller_id: Mapped[int] = mapped_column(ForeignKey("sellers.id", ondelete="CASCADE"), nullable=False)

    seller: Mapped["Seller"] = relationship(back_populates="books")
