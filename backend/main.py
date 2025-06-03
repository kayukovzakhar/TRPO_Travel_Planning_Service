from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.base    import Base
from db.session import engine
from models.route import Route
from models.bookmark import Bookmark


from api.v1 import auth, bookmarks   # импортируем файл bookmarks

app = FastAPI(redirect_slashes=False)

Base.metadata.create_all(bind=engine)

# CORS (если ещё не стоит)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры. Поскольку у bookmarks.router уже префикс = "/api/v1/bookmarks",
# здесь include_router без второго аргумента
app.include_router(auth.router)
app.include_router(bookmarks.router)

