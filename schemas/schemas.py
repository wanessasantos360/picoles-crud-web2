from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, field_validator



# Entidades 
class Aditivo_Nutritivo_Schema(BaseModel):
    id: Optional[int]
    nome: str
    formula_quimica: str

    class Config:
        orm_mode = True

class Sabor_Schema(BaseModel):
    id: Optional[int]
    nome: str

    class Config:
        orm_mode = True

class Tipo_Embalagem_Schema(BaseModel):
    id: Optional[int]
    nome: str

    class Config:
        orm_mode = True

class Conservante_Schema(BaseModel):
    id: Optional[int]
    nome: str
    descricao: str

    class Config:
        orm_mode = True

class Ingrediente_Schema(BaseModel):
    id: Optional[int]
    nome: str

    class Config:
        orm_mode = True

class Revendedor_Schema(BaseModel):
    id: Optional[int]
    cnpj: str
    razao_social: str
    contato: str

    class Config:
        orm_mode = True

class Tipo_Picole_Schema(BaseModel):
    id: Optional[int]
    nome: str

    class Config:
        orm_mode = True


# Com chave estrangeira

class Lote_Schema(BaseModel):
    id: Optional[int]
    quantidade: int

    id_tipo_picole: int
    tipo_picole: Tipo_Picole_Schema

    class Config:
        orm_mode = True

class Nota_Fiscal_Schema(BaseModel):
    id: Optional[int]
    data: datetime
    valor: float
    numero_serie: str
    descricao: str
    id_revendedor: int
    revendedor: List[Revendedor_Schema]
    lotes: List[Lote_Schema]

    class Config:
        orm_mode = True

class Picole_Schema(BaseModel):
    id: Optional[int]
    preco: float
    id_sabor: int
    #sabor: Sabor_Schema
    id_tipo_embalagem: int
    tipo_embalagem: Tipo_Embalagem_Schema
    id_tipo_picole: int
    tipo_picole: Tipo_Picole_Schema
    ingredientes: List[Ingrediente_Schema]
    conservantes: List[Conservante_Schema]
    aditivos_nutritivos: List[Aditivo_Nutritivo_Schema]

    class Config:
        orm_mode = True

