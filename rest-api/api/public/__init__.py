from fastapi import APIRouter
from api.public.articles import views as articles

api = APIRouter()

api.include_router(articles.router, prefix="/search-articles", tags=["the-guardian"])
