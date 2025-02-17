from typing import Optional, List
from core.deps import get_session, get_current_user
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from models.models import Tipo_embalagem, Usuario
from schemas.schemas import Tipo_Embalagem_Schema

router = APIRouter()

@router.post('/add')
def adicionar(tipo_embalagem: Tipo_Embalagem_Schema, db:Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    data = tipo_embalagem.model_dump()
    model = Tipo_embalagem(**data)

    with db as session:
        session.add(model)
        session.commit()
    return Response('Tipo de embalagem adicionado com sucesso.', status.HTTP_200_OK)

@router.put('/edit/{id}')
def editar(id: int, tipo_embalagem: Tipo_Embalagem_Schema, db: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    data = tipo_embalagem.model_dump()
    model = Tipo_embalagem(**data)

    with db as session:
        model_returned: Tipo_embalagem = session.query(Tipo_embalagem).where(Tipo_embalagem.id == id).one_or_none()

        if model_returned:
            model_returned.nome = model.nome
            session.commit()
            return Response('Tipo de embalagem alterado com sucesso', status.HTTP_200_OK)
        else:
            return HTTPException(status.HTTP_403_FORBIDDEN, detail='Tipo de embalagem não encontrada.')

@router.get('/get/{id}', response_model=Tipo_Embalagem_Schema)
def obter_tipo_embalagem(id: int, db: Session = Depends(get_session)):
    with db as session:
        model_returned: Tipo_embalagem = session.query(Tipo_embalagem).where(Tipo_embalagem.id == id).one_or_none()
        if model_returned: 
            return model_returned
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Tipo de embalagem não encontrada.')
        
@router.get('/get', response_model=List[Tipo_Embalagem_Schema])
def listar_embalagens(db: Session = Depends(get_session)):
    with db as session: 
        model_returned: List[Tipo_embalagem] = session.query(Tipo_embalagem).all()
        return model_returned