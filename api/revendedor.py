from typing import Optional, List
from core.deps import get_session
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from models.models import Revendedor
from schemas.schemas import Revendedor_Schema

router = APIRouter()

@router.post('/add')
def adicionar(revendedor: Revendedor_Schema,db: Session = Depends(get_session)):
    data = revendedor.model_dump()
    model = Revendedor(**data)

    with db as session:
        session.add(model)
        session.commit()
    return Response('Revendedor adicionado com sucesso', status.HTTP_200_OK)


@router.put('/edit/{id}')
def editar(id: int, revendedor: Revendedor_Schema, db: Session = Depends(get_session)):
    data = revendedor.model_dump()
    model = Revendedor(**data)

    with db as session:
        model_returned: Revendedor = session.query(Revendedor).where(Revendedor.id == id).one_or_none()
        if model_returned:
            model_returned.cnpj = model.cnpj
            model_returned.razao_social = model.razao_social
            model_returned.contato = model.contato
            session.commit()
            return  Response('Revendedor editado com sucesso.', status.HTTP_200_OK)
        else:
            return HTTPException(status.HTTP_403_FORBIDDEN, detail='Revendedor não encontrado.')
 

@router.get('/get', response_model=List[Revendedor_Schema])
def listar_revendedores(db: Session = Depends(get_session)):
    with db as session:
        model_returned: List[Revendedor] = session.query(Revendedor).all()
        return model_returned
    

@router.get('/get/{id}', response_model=Revendedor_Schema)
def obter_revendedor(id: int, db: Session = Depends(get_session)):
    with db as session:
        model_returned: Revendedor = session.query(Revendedor).where(Revendedor.id == id).one_or_none()
        if model_returned:
            return model_returned
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Revendedor não encontrado.')


