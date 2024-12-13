from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


#engine = create_engine("postgresql+psycopg2://postgres:Postgres2024!@localhost:5432/dbpicoles")
engine = create_engine("postgresql+psycopg2://postgres:Postgres2024!@postgres_db:5432/dbpicoles")

my_session = sessionmaker(bind=engine)
