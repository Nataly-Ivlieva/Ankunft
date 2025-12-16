from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.session import get_session
from app.models.user import User
from app.models.session import SessionToken


async def get_current_user(
    authorization: str = Header(...),
    db: AsyncSession = Depends(get_session),
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header")

    token = authorization.replace("Bearer ", "")

    result = await db.execute(
        select(SessionToken)
        .options(selectinload(SessionToken.user))
        .where(SessionToken.token == token)
    )

    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    if session.expires_at < session.created_at.utcnow():
        raise HTTPException(status_code=401, detail="Token expired")

    return session.user


async def admin_required(
    user: User = Depends(get_current_user),
):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admins only",
        )
    return user
