from typing import Optional, List
from core.deps import get_session, get_current_user
from core.security import generate_hash, verify_password, generate_access_token,authenticate
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import Usuario
from schemas.schemas import Usuario_Schema, Cadastrar_Usuario_Schema

router = APIRouter()

@router.post('/registro')
def registrar(usuario: Cadastrar_Usuario_Schema, db: Session = Depends(get_session)):
    with db as session:
        existe_user = session.query(Usuario).filter(Usuario.email == usuario.email).one_or_none()
        
        if existe_user:
            raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail='Digite outro Usuário')
        
        hashed_password = generate_hash(usuario.password)
        new_user = Usuario(email=usuario.email, hashed_password=hashed_password, username=usuario.username, disabled=False)

        session.add(new_user)
        session.commit()
        return Response('Usuário registrado com sucesso.', status.HTTP_200_OK)


@router.post('/login_user') 
def login(form_data: OAuth2PasswordRequestForm= Depends(), db: Session = Depends(get_session)):
    
    with db as session:
        user: Usuario = authenticate(username= form_data.username, password=form_data.password, db= session)
        if user:
            return JSONResponse(content={'token_type': 'bearer', 'access_token': generate_access_token(user.id)}, status_code= status.HTTP_200_OK)
        else:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail= 'Bad Credentials')
    

@router.get("/users/me", response_model=Usuario_Schema)
def users_me(current_user: Usuario= Depends(get_current_user)):
    return current_user

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)): # Usa o OAuth2PasswordRequestForm
    # Verifica se o usuário existe
    user = db.query(Usuario).filter(Usuario.username == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verifica a senha
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Gera o token de acesso
    access_token = generate_access_token(data={"sub": user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }