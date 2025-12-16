from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from app.models.session import SessionToken


async def verify_session_token(
    db: AsyncSession,
    token: str
) -> SessionToken | None:
    result = await db.execute(
        select(SessionToken).where(SessionToken.token == token)
    )
    session = result.scalar_one_or_none()

    if not session:
        return None

    if session.expires_at < datetime.utcnow():
        return None

    session.last_used = datetime.utcnow()
    await db.commit()

    return session
