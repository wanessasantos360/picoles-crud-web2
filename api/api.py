from fastapi import APIRouter

api_router = APIRouter()

#Tabelas de Entidades PK e Atributos
api_router.include_router(aditivo_router, prefix='/aditivo', tags=['Aditivo Nutritivo'])
