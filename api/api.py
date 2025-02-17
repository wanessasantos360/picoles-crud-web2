from fastapi import APIRouter

from api.aditivo_nutritivo import router as aditivo_router
from api.sabor import router as sabor_router
from api.tipo_embalagem import router as tipo_embalagem_router
from api.revendedor import router as revendedor_router
from api.conservante import router as conservante_router
from api.ingrediente import router as ingrediente_router
from api.tipo_picole import router as tipo_picole_router

from api.lote import router as lote_router
from api.nota_fiscal import router as nota_fiscal_router
from api.picoles import router as picoles_router

from api.usuario import router as usuario_router

api_router = APIRouter()

# Usuario
api_router.include_router(usuario_router, prefix='/usuarios', tags=['Usuarios'])

#Tabelas de Entidades PK e Atributos
api_router.include_router(aditivo_router, prefix='/aditivo', tags=['Aditivo Nutritivo'])
api_router.include_router(sabor_router, prefix='/sabor', tags=['Sabor'])
api_router.include_router(tipo_embalagem_router, prefix='/tipo_embalagem', tags=['Tipo de Embalagem'])
api_router.include_router(revendedor_router, prefix='/revendedor', tags=['Revendedor'])
api_router.include_router(conservante_router, prefix='/conservante', tags=['Conservante'])
api_router.include_router(ingrediente_router, prefix='/ingrediente', tags=['Ingrediente'])
api_router.include_router(tipo_picole_router, prefix='/tipo_picole', tags=['Tipo de picolé'])

#Tabelas com FK
api_router.include_router(lote_router, prefix='/lote', tags=['## Lote'])
api_router.include_router(nota_fiscal_router, prefix='/nota_fiscal', tags=['## Nota Fiscal'])
api_router.include_router(picoles_router, prefix='/picoles', tags=['## Picoles'])

