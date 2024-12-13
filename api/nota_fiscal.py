from typing import Optional, List
from core.deps import get_session
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from models.models import Nota_Fiscal
from schemas.schemas import Nota_Fiscal_Schema

router = APIRouter()

@router.post('/add')
def adicionar(nota_fiscal: Nota_Fiscal_Schema, db: Session = Depends(get_session)):
    data = nota_fiscal.model_dump()
    model = Nota_Fiscal(**data)

    with db as session:
        session.add(model)
        session.commit()
    return Response('Nota Fiscal Adicionada com sucesso.', status.HTTP_200_OK)

@router.put('/edit/{id}')
def editar(id: int, nota_fiscal: Nota_Fiscal_Schema, db: Session = Depends(get_session)):
    data = nota_fiscal.model_dump()
    model_updated = Nota_Fiscal(**data)

    with db as session:
        model_returned: Nota_Fiscal = session.query(Nota_Fiscal).where(Nota_Fiscal.id == id).one_or_none()
        if model_returned:
            model_returned.valor_total = model_updated.valor_total
            model_returned.id_revendedor = model_updated.id_revendedor
            model_returned.data_emissao = model_updated.data_emissao
            session.commit()
            return Response('Nota Fiscal Atualizada com sucesso.', status.HTTP_200_OK)
        else:
            return HTTPException(status.HTTP_403_FORBIDDEN, detail='Nota Fiscal não encontrada')

@router.get('/get/{id}', response_model=Nota_Fiscal_Schema)
def obter_nota_fiscal(id: int, db: Session = Depends(get_session)):
    with db as session:
        model_returned: Nota_Fiscal = session.query(Nota_Fiscal).where(Nota_Fiscal.id == id).one_or_none()

        if model_returned:
            return model_returned
        else: 
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Nota Fiscal não encontrada')

@router.get('/get', response_model=List[Nota_Fiscal_Schema])
def listar_nota_fiscal(db: Session = Depends(get_session)):
    with db as session:
        model_returned: List[Nota_Fiscal] = session.query(Nota_Fiscal).all()
        return model_returned
