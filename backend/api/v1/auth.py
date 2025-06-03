from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from schemas.user import UserCreate, UserLogin, UserResponse       # схема вывода для публичных данных пользователя
from models.user import User as DBUser      # ORM-модель пользователя
from db.session import get_db              # зависимость для сессии БД
from core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    get_current_user
)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["auth"],
)

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_in: UserCreate,
    db: Session = Depends(get_db),
):
    # проверяем, нет ли пользователя с таким email
    existing = db.query(DBUser).filter(DBUser.email == user_in.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # хешируем пароль и сохраняем в БД
    hashed = get_password_hash(user_in.password)
    new_user = DBUser(
        email=user_in.email,
        hashed_password=hashed,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post(
    "/login",
    response_model=dict[str, str],  # {"access_token": "...", "token_type": "bearer"}
)
def login(
    user_in: UserLogin,
    db: Session = Depends(get_db),
):
    # ищем пользователя по email
    user = db.query(DBUser).filter(DBUser.email == user_in.email).first()
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # формируем JWT
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить текущего авторизованного пользователя",
)
def read_current_user(
    current_user: DBUser = Depends(get_current_user),
):
    return current_user
