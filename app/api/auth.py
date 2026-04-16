from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from app.core.security import (
    create_token, verify_password, get_password_hash, decode_token, 
    ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
)
# Додаємо імпорти для роботи з базою
from app.models.database import db
from app.repository.user_repo import UserRepository
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["Auth"])

# Схема для Swagger
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate):
    # 1. Перевіряємо, чи такий юзер вже є
    existing_user = await UserRepository.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Користувач з таким ім'ям вже існує"
        )
    
    # 2. Хешуємо пароль
    hashed_password = get_password_hash(user_data.password)
    
    # 3. Зберігаємо в MongoDB
    new_user = await UserRepository.create_user(db, user_data.username, hashed_password)
    return new_user

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Шукаємо юзера в реальній базі замість FAKE_USERS_DB
    user = await UserRepository.get_user_by_username(db, form_data.username)
    
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Невірне ім'я користувача або пароль"
        )

    access_token = create_token(
        data={"sub": user["username"], "type": "access"}, 
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_token(
        data={"sub": user["username"], "type": "refresh"}, 
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        token_type="refresh"
    )
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/refresh")
async def refresh_token_endpoint(refresh_token: str):
    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Невалідний refresh токен")
    
    username = payload.get("sub")
    new_access_token = create_token(data={"sub": username, "type": "access"})
    return {"access_token": new_access_token, "token_type": "bearer"}