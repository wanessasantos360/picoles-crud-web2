from core.db import engine
from core.settings import ModelBase

def create_tables():
    global engine

    from models import models
    ModelBase.metadata.drop_all(engine)
    ModelBase.metadata.create_all(engine)

create_tables()