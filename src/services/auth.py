__all__ = ["AuthService", "get_current_seller"]

from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.configurations.database import get_async_session
from src.models.sellers import Seller

JWT_SECRET_KEY = "changeme-secret-key"  # для учебного проекта
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 60


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def authenticate_seller(self, e_mail: str, password: str) -> Seller | None:
        stmt = select(Seller).where(Seller.e_mail == e_mail, Seller.password == password)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    def create_access_token(self, seller: Seller) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MINUTES)
        payload = {"sub": str(seller.id), "exp": expire}
        return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    async def get_seller_from_token(self, token: str) -> Seller | None:
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            seller_id = int(payload.get("sub"))
        except Exception:
            return None

        return await self.session.get(Seller, seller_id)


security = HTTPBearer()

DBSessionDep = Annotated[AsyncSession, Depends(get_async_session)]
CredentialsDep = Annotated[HTTPAuthorizationCredentials, Depends(security)]


async def get_current_seller(
    credentials: CredentialsDep,
    session: DBSessionDep,
) -> Seller:
    auth_service = AuthService(session)
    seller = await auth_service.get_seller_from_token(credentials.credentials)
    if seller is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    return seller

