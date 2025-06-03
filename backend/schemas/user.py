from pydantic import BaseModel, EmailStr

# Общие поля пользователя
class UserBase(BaseModel):
    email: EmailStr

# Схема для регистрации (принимаем пароль)
class UserCreate(UserBase):
    password: str

# Схема для логина (принимаем email и пароль)
class UserLogin(UserBase):
    password: str

# Схема для ответа (не отдаём пароль)
class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True
