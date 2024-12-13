from typing import Optional, List
from core.deps import get_session
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from models.models import Sabor
from schemas.schemas import Sabor_Schema

router = APIRouter()

@router.post('/add')
def adicionar(sabor: Sabor_Schema, db: Session = Depends(get_session)):
    data = sabor.model_dump()
    model = Sabor(**data)

    with db as session:
        session.add(model)
        session.commit()
    return Response('Sabor Adicionado com sucesso.', status.HTTP_200_OK)


@router.put('/edit/{id}')
def editar(id: int, sabor: Sabor_Schema, db: Session = Depends(get_session)):
    data = sabor.model_dump()
    model_updated = Sabor(**data)

    with db as session:
        model_returned: Sabor = session.query(Sabor).where(Sabor.id == id).one_or_none()
        if model_returned:
            model_returned.nome = model_updated.nome
            session.commit()
            return Response('Sabor Atualizado com sucesso.', status.HTTP_200_OK)
        else:
            return HTTPException(status.HTTP_403_FORBIDDEN, detail='Sabor não encontrado')
        

@router.get('/get/{id}', response_model=Sabor_Schema)
def obter_sabor(id: int, db: Session = Depends(get_session)):
    with db as session:
        model_returned: Sabor = session.query(Sabor).where(Sabor.id == id).one_or_none()

        if model_returned:
            return model_returned
        else: 
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Sabor não encontrado') 
        

@router.get('/get', response_model=List[Sabor_Schema])
def listar_sabor(db: Session = Depends(get_session)):
    with db as session:
        model_returned: List[Sabor] = session.query(Sabor).all()
        return model_returned

