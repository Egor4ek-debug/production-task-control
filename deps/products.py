from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import get_session
from crud.products import ProductsRepository
from services.products import ProductsService

def get_product_repo(session: AsyncSession = Depends(get_session)) -> ProductsRepository:
    return ProductsRepository(session)

def get_product_service(repo: ProductsRepository = Depends(get_product_repo)) -> ProductsService:
    return ProductsService(repo)
