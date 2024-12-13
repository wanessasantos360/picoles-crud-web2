from typing import Optional, List
from core.deps import get_session
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from models.models import Lote
from schemas.schemas import Lote_Schema

router = APIRouter()

@router.get('/get', response_model=List[Lote_Schema])
def listar_lote(db: Session = Depends(get_session)):
    with db as session:
        model_returned: List[Lote] = session.query(Lote).all()
        return model_returned
    
@router.get('/get/{id}', response_model=Lote_Schema)
def obter_lote(id: int, db: Session = Depends(get_session)):
    with db as session:
        model_returned: Lote = session.query(Lote).where(Lote.id == id).one_or_none()

        if model_returned:
            return model_returned
        else: 
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Lote não encontrado') 
        
@router.post('/add')
def adicionar(lote: Lote_Schema, db: Session = Depends(get_session)):
    data = lote.model_dump()
    model = Lote(**data)

    with db as session:
        session.add(model)
        session.commit()
    return Response('Lote Adicionado com sucesso.', status.HTTP_200_OK)

@router.put('/edit/{id}')
def editar(id: int, lote: Lote_Schema, db: Session = Depends(get_session)):
    data = lote.model_dump()
    model_updated = Lote(**data)

    with db as session:
        model_returned: Lote = session.query(Lote).where(Lote.id == id).one_or_none()
        if model_returned:
            model_returned.quantidade = model_updated.quantidade
            session.commit()
            return Response('Lote Atualizado com sucesso.', status.HTTP_200_OK)
        else:
            return HTTPException(status.HTTP_403_FORBIDDEN, detail='Lote não encontrado')
        

