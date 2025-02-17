from typing import Optional, List
from core.deps import get_session, get_current_user
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from models.models import Ingrediente, Usuario
from schemas.schemas import Ingrediente_Schema

router = APIRouter()


  
@router.post('/add')
def adicionar(ingrediente: Ingrediente_Schema, db: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    data = ingrediente.model_dump()
    model = Ingrediente(**data)

    with db as session:
        session.add(model)
        session.commit()
    return Response('Ingrediente Adicionado com sucesso.', status.HTTP_200_OK)

@router.put('/edit/{id}')
def editar(id: int, ingrediente: Ingrediente_Schema, db: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    data = ingrediente.model_dump()
    model_updated = Ingrediente(**data)

    with db as session:
        model_returned: Ingrediente = session.query(Ingrediente).where(Ingrediente.id == id).one_or_none()
        if model_returned:
            model_returned.nome = model_updated.nome
            session.commit()
            return Response('Ingrediente Atualizado com sucesso.', status.HTTP_200_OK)
        else:
            return HTTPException(status.HTTP_403_FORBIDDEN, detail='Ingrediente não encontrado')
        
@router.get('/get/{id}', response_model=Ingrediente_Schema)
def obter_ingrediente(id: int, db: Session = Depends(get_session)):
    with db as session:
        model_returned: Ingrediente = session.query(Ingrediente).where(Ingrediente.id == id).one_or_none()

        if model_returned:
            return model_returned
        else: 
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Ingrediente não encontrado') 

@router.get('/get', response_model=List[Ingrediente_Schema])
def listar_ingrediente(db: Session = Depends(get_session)):
    with db as session:
        model_returned: List[Ingrediente] = session.query(Ingrediente).all()
        return model_returned
    