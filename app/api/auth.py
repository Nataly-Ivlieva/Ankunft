from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from datetime import datetime

from app.db.session import get_session
from app.models.user import User
from app.models.session import SessionToken
from app.api.schemas_auth import SignUpRequest, LoginRequest, SessionResponse
from app.core.security import hash_password, verify_password, generate_session_token, token_expiration

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=SessionResponse)
async def signup(data: SignUpRequest, db: AsyncSession = Depends(get_session)):
    q = select(User).where(User.email == data.email)
    existing = (await db.execute(q)).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        role=data.role
    )
    db.add(user)
    await db.flush()

    token = SessionToken(
        token=generate_session_token(),
        user_id=user.id,
        expires_at=token_expiration()
    )
    db.add(token)
    await db.commit()

    return SessionResponse(token=token.token, role=user.role)


@router.post("/login", response_model=SessionResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_session)):
    q = select(User).where(User.email == data.email)
    user = (await db.execute(q)).scalar_one_or_none()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    await db.execute(
        delete(SessionToken).where(SessionToken.user_id == user.id)
    )
    session = SessionToken(
        token=generate_session_token(),
        user_id=user.id,
        expires_at=token_expiration()
    )
    db.add(session)
    await db.commit()

    return SessionResponse(token=session.token, role=user.role)



@router.post("/logout")
async def logout(token: str, db: AsyncSession = Depends(get_session)):
    q = delete(SessionToken).where(SessionToken.token == token)
    await db.execute(q)
    await db.commit()
    return {"status": "ok"}
