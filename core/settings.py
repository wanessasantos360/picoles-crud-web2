from sqlalchemy.orm import declarative_base

ModelBase = declarative_base()

JWT_SECRET: str = 'AMWv2ZK68wdca61mlH1willKQq-1TBakT36goW34XNc'
ALGORITHM: str = 'HS256'
EXPIRATION_MINUTES: int = 60 * 24 * 7
DATE_FORMAT = '%d/%m/%Y'
