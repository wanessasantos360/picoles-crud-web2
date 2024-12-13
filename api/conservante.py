from typing import Optional, List
from core.deps import get_session
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from models.models import Conservante
from schemas.schemas import Conservante_Schema

router = APIRouter()

@router.post('/add')
def adicionar(conservante: Conservante_Schema,db: Session = Depends(get_session)):
    data = conservante.model_dump()
    model = Conservante(**data)

    with db as session:
        session.add(model)
        session.commit()
    return Response('Conservante adicionado com sucesso', status.HTTP_200_OK)


@router.put('/edit/{id}')
def editar(id: int, conservante: Conservante_Schema, db: Session = Depends(get_session)):
    data = conservante.model_dump()
    model = Conservante(**data)

    with db as session:
        model_returned: Conservante = session.query(Conservante).where(Conservante.id == id).one_or_none()
        if model_returned:
            model_returned.nome = model.nome
            model_returned.descricao = model.descricao
            session.commit()
            return  Response('Conservante editado com sucesso.', status.HTTP_200_OK)
        else:
            return HTTPException(status.HTTP_403_FORBIDDEN, detail='Conservante não encontrado.')
 

@router.get('/get', response_model=List[Conservante_Schema])
def listar_conservantes(db: Session = Depends(get_session)):
    with db as session:
        model_returned: List[Conservante] = session.query(Conservante).all()
        return model_returned
    

@router.get('/get/{id}', response_model=Conservante_Schema)
def obter_conservante(id: int, db: Session = Depends(get_session)):
    with db as session:
        model_returned: Conservante = session.query(Conservante).where(Conservante.id == id).one_or_none()
        if model_returned:
            return model_returned
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Conservante não encontrado.')

