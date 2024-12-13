from typing import Optional, List
from core.deps import get_session
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from models.models import Picole
from schemas.schemas import Picole_Schema

router = APIRouter()

@router.post('/add')
def adicionar(picole: Picole_Schema, db: Session = Depends(get_session)):
    data = picole.model_dump()
    model = Picole(**data)

    with db as session:
        session.merge(model)
        session.commit()
    return Response('Picolé Adicionado com sucesso.', status.HTTP_200_OK)

@router.put('/edit/{id}')
def editar(id: int, picole: Picole_Schema, db: Session = Depends(get_session)):
    data = picole.model_dump()
    model_updated = Picole(**data)

    with db as session:
        model_returned: Picole = session.query(Picole).where(Picole.id == id).one_or_none()
        if model_returned:
            model_returned.preco = model_updated.preco
            model_returned.id_sabor = model_updated.id_sabor
            model_returned.id_tipo_embalagem = model_updated.id_tipo_embalagem
            model_returned.id_tipo_picole = model_updated.id_tipo_picole
            session.commit()
            return Response('Picolé Atualizado com sucesso.', status.HTTP_200_OK)
        else:
            return HTTPException(status.HTTP_403_FORBIDDEN, detail='Picolé não encontrado')

@router.get('/get/{id}', response_model=Picole_Schema)
def obter_picole(id: int, db: Session = Depends(get_session)):
    with db as session:
        model_returned: Picole = session.query(Picole).where(Picole.id == id).one_or_none()

        if model_returned:
            return model_returned
        else: 
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Picolé não encontrado')

@router.get('/get', response_model=List[Picole_Schema])
def listar_picole(db: Session = Depends(get_session)):
    with db as session:
        model_returned: List[Picole] = session.query(Picole).all()
        return model_returned
