from typing import Optional, List
from core.deps import get_session, get_current_user
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from models.models import Tipo_Picole, Usuario
from schemas.schemas import Tipo_Picole_Schema

router = APIRouter()

        
@router.post('/add')
def adicionar(tipo_picole: Tipo_Picole_Schema, db: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    data = tipo_picole.model_dump()
    model = Tipo_Picole(**data)

    with db as session:
        session.add(model)
        session.commit()
    return Response('Tipo de picolé adicionado com sucesso.', status.HTTP_200_OK)

@router.put('/edit/{id}')
def editar(id: int, tipo_picole: Tipo_Picole_Schema, db: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    data = tipo_picole.model_dump()
    model_updated = Tipo_Picole(**data)

    with db as session:
        model_returned: Tipo_Picole = session.query(Tipo_Picole).where(Tipo_Picole.id == id).one_or_none()
        if model_returned:
            model_returned.nome = model_updated.nome
            session.commit()
            return Response('Tipo de picolé atualizado com sucesso.', status.HTTP_200_OK)
        else:
            return HTTPException(status.HTTP_403_FORBIDDEN, detail='Tipo de picolé não encontrado')
        

@router.get('/get/{id}', response_model=Tipo_Picole_Schema)
def obter_tipo_picole(id: int, db: Session = Depends(get_session)):
    with db as session:
        model_returned: Tipo_Picole = session.query(Tipo_Picole).where(Tipo_Picole.id == id).one_or_none()

        if model_returned:
            return model_returned
        else: 
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Tipo de picolé não encontrado') 
        

@router.get('/get', response_model=List[Tipo_Picole_Schema])
def listar_tipo_picole(db: Session = Depends(get_session)):
    with db as session:
        model_returned: List[Tipo_Picole] = session.query(Tipo_Picole).all()
        return model_returned
    