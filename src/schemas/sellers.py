from pydantic import BaseModel, EmailStr

from .books import ReturnedBook


class BaseSeller(BaseModel):
    first_name: str
    last_name: str
    e_mail: EmailStr


class CreateSeller(BaseSeller):
    password: str


class UpdateSeller(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    e_mail: EmailStr | None = None


class Seller(BaseSeller):
    id: int


class SellerWithBooks(Seller):
    books: list[ReturnedBook]


class ReturnedAllSellers(BaseModel):
    sellers: list[Seller]


__all__ = [
    "CreateSeller",
    "UpdateSeller",
    "Seller",
    "SellerWithBooks",
    "ReturnedAllSellers",
]

