from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.configurations.database import get_async_session
from src.schemas import CreateSeller, ReturnedAllSellers, Seller, SellerWithBooks, UpdateSeller
from src.services import SellerService, get_current_seller

sellers_router = APIRouter(prefix="/seller", tags=["sellers"])

DBSession = Annotated[AsyncSession, Depends(get_async_session)]


@sellers_router.post("/", response_model=Seller, status_code=status.HTTP_201_CREATED)
async def create_seller(seller: CreateSeller, session: DBSession):
    new_seller = await SellerService(session).create_seller(seller)
    return new_seller


@sellers_router.get("/", response_model=ReturnedAllSellers)
async def get_all_sellers(session: DBSession):
    sellers = await SellerService(session).get_all_sellers()
    return {"sellers": sellers}


@sellers_router.get("/{seller_id}", response_model=SellerWithBooks)
async def get_seller(
    seller_id: int,
    session: DBSession,
    current_seller=Depends(get_current_seller),
):
    if current_seller.id != seller_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    seller = await SellerService(session).get_seller(seller_id, with_books=True)
    if seller is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return seller


@sellers_router.put("/{seller_id}", response_model=Seller)
async def update_seller(seller_id: int, data: UpdateSeller, session: DBSession):
    updated = await SellerService(session).update_seller(seller_id, data)
    if updated is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return updated


@sellers_router.delete("/{seller_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_seller(seller_id: int, session: DBSession):
    deleted = await SellerService(session).delete_seller(seller_id)
    if not deleted:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

