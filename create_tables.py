from core.db import engine
from core.settings import ModelBase
from models import all_models

def create_tables():
    global engine

    ModelBase.metadata.drop_all(engine)
    ModelBase.metadata.create_all(engine)

create_tables()