from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel

if TYPE_CHECKING:  # only for type checkers
    from .books import Book


class Seller(BaseModel):
    __tablename__ = "sellers"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    e_mail: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    books: Mapped[list["Book"]] = relationship(
        back_populates="seller",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


__all__ = ["Seller"]

