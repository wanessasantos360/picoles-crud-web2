from typing import Generator
from sqlalchemy.orm import Session
from core.db import my_session
from core.security import oauth2_schema
from core.settings import JWT_SECRET, ALGORITHM

from sqlalchemy.future import select

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError

from models.models import Usuario


def get_session()-> Generator:

    session: Session = my_session()
    return session


def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_session)) -> Usuario:
    """
    Obtém o usuário atual com base no token JWT.
    Retorna o usuário se o token for válido, caso contrário, levanta uma exceção.
    """
    credential_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not Authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decodifica o token JWT
        payload = jwt.decode(token=token, key=JWT_SECRET, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise credential_error

    except JWTError:
        raise credential_error

    # Consulta síncrona ao banco de dados
    query = select(Usuario).filter(Usuario.id == int(username)).filter(Usuario.disabled == False)
    result = db.execute(query)
    user: Usuario = result.unique().scalar_one_or_none()

    if user is None:
        raise credential_error

    return user

'''async def get_current_user(token: str = Depends(oauth2_schema), db: AsyncSession = Depends(get_session))-> Usuario:

    credential_error = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, 
                                     detail='Not Authenticated', headers={'WWW-Authentication': 'Bearer'})
    
    try:
        payload = jwt.decode(token=token, key= JWT_SECRET, algorithms=[ALGORITHM])
        username = payload.get('sub')

        if username is None:
            raise credential_error

    except JWTError:
        raise credential_error

    
    async with db as session:
        query = select(Usuario).filter(Usuario.id == int(username)).filter(Usuario.active == True)
        result = await session.execute(query)
        user: Usuario = result.unique().scalar_one_or_none()

        if user is None:
            raise credential_error
        
        return user'''