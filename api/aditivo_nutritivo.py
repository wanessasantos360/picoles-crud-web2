from typing import Optional, List
from core.deps import get_session, get_current_user
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from models.models import Aditivo_nutritivo, Usuario
from schemas.schemas import Aditivo_Nutritivo_Schema

router = APIRouter()

@router.post('/add')
def adicionar(aditivo_nutritivo: Aditivo_Nutritivo_Schema, db:Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    data = aditivo_nutritivo.model_dump() # Dict
    model = Aditivo_nutritivo(**data)

    with db as session:
        session.add(model)
        session.commit()
    return Response('Aditivo Nutritivo adicionado com sucesso.', status.HTTP_200_OK) 
    
@router.put('/edit/{id}')
def editar(id: int, aditivo_nutritivo: Aditivo_Nutritivo_Schema, db:Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    data = aditivo_nutritivo.model_dump()
    model = Aditivo_nutritivo(**data)

    with db as session:
        model_returned: Aditivo_nutritivo = session.query(Aditivo_nutritivo).where(Aditivo_nutritivo.id == id).one_or_none()
        if model_returned:
            model_returned.nome = model.nome
            model_returned.formula_quimica = model.formula_quimica
            session.commit()
            return  Response('Aditivo nutritivo editado com sucesso.', status.HTTP_200_OK)
        else:
            return HTTPException(status.HTTP_403_FORBIDDEN, detail='Aditivo nutritivo não encontrado.')
    
@router.get('/get/{id}', response_model=Aditivo_Nutritivo_Schema)
def obter_aditivo(id: int, db: Session = Depends(get_session)):
    with db as session:
        model_returned: Aditivo_nutritivo = session.query(Aditivo_nutritivo).where(Aditivo_nutritivo.id == id).one_or_none()
        if model_returned:
            return model_returned
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Aditivo nutritivo não encontrado.')

@router.get('/get', response_model=List[Aditivo_Nutritivo_Schema])
def listar_aditivos(db: Session = Depends(get_session)):
    with db as session:
        model_returned: List[Aditivo_nutritivo] = session.query(Aditivo_nutritivo).all()
        return model_returned
        