from typing import Generator
from sqlalchemy.orm import Session
from core.db import my_session

def get_session()-> Generator:

    session: Session = my_session()
    return session
