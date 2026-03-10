__all__ = ["SellerService"]

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.sellers import Seller
from src.schemas.sellers import CreateSeller, Seller as SellerSchema, UpdateSeller


class SellerService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_seller(self, data: CreateSeller) -> Seller:
        seller = Seller(
            first_name=data.first_name,
            last_name=data.last_name,
            e_mail=data.e_mail,
            password=data.password,
        )
        self.session.add(seller)
        await self.session.flush()
        return seller

    async def get_all_sellers(self) -> list[Seller]:
        result = await self.session.execute(select(Seller))
        return result.scalars().all()

    async def get_seller(self, seller_id: int, with_books: bool = False) -> Seller | None:
        options = []
        if with_books:
            options.append(selectinload(Seller.books))

        stmt = select(Seller).where(Seller.id == seller_id).options(*options)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_seller(self, seller_id: int, data: UpdateSeller) -> Seller | None:
        seller = await self.session.get(Seller, seller_id)
        if not seller:
            return None

        if data.first_name is not None and data.first_name != seller.first_name:
            seller.first_name = data.first_name
        if data.last_name is not None and data.last_name != seller.last_name:
            seller.last_name = data.last_name
        if data.e_mail is not None and data.e_mail != seller.e_mail:
            seller.e_mail = data.e_mail

        await self.session.flush()
        return seller

    async def delete_seller(self, seller_id: int) -> bool:
        seller = await self.session.get(Seller, seller_id)
        if not seller:
            return False

        await self.session.delete(seller)
        return True

