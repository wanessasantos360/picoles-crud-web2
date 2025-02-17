from typing import Optional, Annotated
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from pytz import timezone
from datetime import datetime, timedelta

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt

from core.settings import JWT_SECRET, ALGORITHM, EXPIRATION_MINUTES

from models.models import Usuario

crypto = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_schema = OAuth2PasswordBearer(tokenUrl='/usuarios/login_user')

def generate_hash(password: str) -> str:
    return crypto.hash(password)

def verify_password(password: str, hash: str)-> bool:
    return crypto.verify(password, hash)

def _generate_token(token_type: str, expiration: timedelta, subject: str)-> str:
    payload = {}
    rec = timezone('America/Recife')
    now = datetime.now(rec)
    exp = now + expiration

    payload['token type'] = token_type
    payload['iat'] = now
    payload['exp'] = exp
    payload['sub'] = str(subject)

    return jwt.encode(claims=payload, key=JWT_SECRET, algorithm= ALGORITHM)


def generate_access_token(subject: str)-> str:

    return _generate_token(token_type='access_token', expiration=timedelta(minutes=EXPIRATION_MINUTES), subject=subject)


def authenticate(username: str, password: str, db: Session) -> Optional[Usuario]:
    query = select(Usuario).filter(Usuario.email == username).filter(Usuario.disabled == False)
    result = db.execute(query)

    # Obtém o usuário
    user: Usuario = result.unique().scalar_one_or_none()

    # Verifica se o usuário existe e se a senha está correta
    if user and verify_password(password=password, hash=user.hashed_password):
        return user
    else:
        return None
