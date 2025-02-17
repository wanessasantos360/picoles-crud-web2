from sqlalchemy import Table, Column, Integer, BigInteger, DECIMAL, DateTime, String, ForeignKey, Boolean
from sqlalchemy import orm
from core.settings import ModelBase
from typing import List, Optional
from datetime import datetime

ingredientes_picoles = Table(
    'ingredientes_picoles',
    ModelBase.metadata,
    Column('id_picole', Integer, ForeignKey('picoles.id')),
    Column('id_ingrediente', Integer, ForeignKey('ingredientes.id'))
)

aditivos_nutritivos_picoles = Table(
    'aditivos_nutritivos_picoles',
    ModelBase.metadata,
    Column('id_aditivo_nutritivo', Integer, ForeignKey('aditivos_nutritivos.id')),
    Column('id_picole', Integer, ForeignKey('picoles.id'))
)

conservantes_picoles = Table(
    'conservantes_picoles',
    ModelBase.metadata,
    Column('id_conservante', Integer, ForeignKey('conservantes.id')),
    Column('id_picole', Integer, ForeignKey('picoles.id'))
)

lotes_notas_fiscais = Table(
    'lotes_notas_fiscais',
    ModelBase.metadata,
    Column('id_lote', Integer, ForeignKey('lotes.id')),
    Column('id_nota_fiscal', Integer, ForeignKey('notas_fiscais.id'))
)

class Aditivo_nutritivo(ModelBase):

    __tablename__ = 'aditivos_nutritivos'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nome = Column(String(45), nullable=False)
    formula_quimica = Column(String(45), nullable=False)

    def __init__(self, **kwargs) -> None:
        self.nome = kwargs['nome']
        self.formula_quimica = kwargs['formula_quimica']

    def __repr__(self):
        return f'ID: {self.id}, Aditivo Nutritivo {self.nome} com Fórmula Química {self.formula_quimica}'
    
class Sabor(ModelBase):

    __tablename__ = 'sabores'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(45), nullable=False)

    def __init__(self, **kwargs) -> None:
        self.nome = kwargs['nome']
    
    def __repr__(self):
        return f'ID: {self.id}, Sabor: {self.nome}'
    
class Tipo_embalagem(ModelBase):
    __tablename__ = 'tipos_embalagens'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(45), nullable=False)

    def __init__(self, **kwargs) -> None:
        self.nome = kwargs['nome']

    def __repr__(self):
        return f'Id: {self.id}, Tipo de embalagem {self.nome}'

class Revendedor(ModelBase):
    __tablename__ = 'revendedores'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cnpj = Column(String(18), nullable=False)
    razao_social = Column(String(45), nullable=False)
    contato = Column(String(45), nullable=False)

    def __init__(self, **kwargs) -> None:
        self.cnpj = kwargs['cnpj']
        self.razao_social = kwargs['razao_social']
        self.contato = kwargs['contato']

    def __repr__(self):
        return f'Id: {self.id} CNPJ: {self.cnpj}, Razão social: {self.razao_social}, Contato: {self.contato}'

class Ingrediente(ModelBase):
    __tablename__ = 'ingredientes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(45), nullable=False)

    def __init__(self, **kwargs) -> None:
        self.nome = kwargs['nome']
        
    def __repr__(self):
        return f'Id: {self.id}, Nome do ingrediente: {self.nome}'

class Conservante(ModelBase):
    __tablename__ = 'conservantes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(45), nullable=False)
    descricao = Column(String(45), nullable=False)

    def __init__(self, **kwargs) -> None:
        self.nome = kwargs['nome']
        self.descricao = kwargs['descricao']

    def __repr__(self):
        return f'Id: {self.id}, Nome: {self.nome}, Descrição: {self.descricao}'

class Tipo_Picole(ModelBase):
    __tablename__ = 'tipos_picoles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(45), nullable=False)

    def __init__(self, **kwargs) -> None:
        self.nome = kwargs['nome']

    def __repr__(self):
        return f'Id: {self.id}, Nome: {self.nome}'

class Picole(ModelBase):
     
    __tablename__ = 'picoles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    preco = Column(DECIMAL(7,2))
    id_sabor = Column(Integer, ForeignKey('sabores.id'))
    sabor:Sabor = orm.relationship('Sabor', lazy='joined', innerjoin = True)

    id_tipo_embalagem = Column(Integer, ForeignKey('tipos_embalagens.id'))
    tipo_embalagem:Tipo_embalagem = orm.relationship('Tipo_embalagem', lazy='joined', innerjoin = True)

    id_tipo_picole = Column(Integer, ForeignKey('tipos_picoles.id'))
    tipo_picole:Tipo_Picole = orm.relationship('Tipo_Picole', lazy='joined', innerjoin = True)


    ingredientes:List[Ingrediente] = orm.relationship('Ingrediente', secondary=ingredientes_picoles, lazy='joined', innerjoin = True, backref='ingrediente')

    conservantes:Optional[List[Conservante]] = orm.relationship(
        'Conservante', 
        secondary=conservantes_picoles, 
        lazy='joined', innerjoin = True,
        backref='conservante'
    )

    aditivos_nutritivos:Optional[List[Aditivo_nutritivo]] = orm.relationship(
        'Aditivo_nutritivo', 
        secondary=aditivos_nutritivos_picoles, 
        lazy='joined', innerjoin = True, 
        backref='aditivo_nutritivo'
    )
    
    def __init__(self, **kwargs):
        self.preco = kwargs['preco']
        self.id_sabor = kwargs['id_sabor']
        self.id_tipo_embalagem = kwargs['id_tipo_embalagem']
        self.id_tipo_picole = kwargs['id_tipo_picole']

        temp_ingredientes = kwargs['ingredientes']
        temp_conservantes = kwargs['conservantes']
        temp_aditivos_nutritivos = kwargs['aditivos_nutritivos']

        ingredientes = []
        conservantes = []
        aditivos_nutritivos = []

        for ingrediente in temp_ingredientes:
            ingrediente_model = Ingrediente(**ingrediente)
            ingrediente_model.id = ingrediente['id']
            ingredientes.append(ingrediente_model)
        
        for conservante in temp_conservantes:
            conservante_model = Conservante(**conservante)
            conservante_model.id = conservante['id']
            conservantes.append(conservante_model)
            
        for aditivo_nutritivo in temp_aditivos_nutritivos:
            aditivos_nutritivo_model = Aditivo_nutritivo(**aditivo_nutritivo)
            aditivos_nutritivo_model.id = aditivo_nutritivo['id']
            aditivos_nutritivos.append(aditivos_nutritivo_model)
        
        self.ingredientes = ingredientes
        self.conservantes = conservantes
        self.aditivos_nutritivos = aditivos_nutritivos

    def __repr__(self):
        return f'Id: {self.id}, Preço: {self.preco}, Picole de: {self.sabor.nome}'

class Lote(ModelBase):

    __tablename__ = 'lotes'

    id = Column(Integer, primary_key=True, autoincrement= True)
    quantidade = Column(Integer)

    id_tipo_picole = Column(Integer, ForeignKey('tipos_picoles.id'))
    tipo_picole:Tipo_Picole = orm.relationship('Tipo_Picole', lazy='joined', innerjoin = True)


    def __init__(self, **kwargs) -> None:
        self.id = kwargs['id']
        self.quantidade = kwargs['quantidade']
        #self.id_tipo_picole = kwargs['id_tipo_picole']

    def __repr__(self):
        return f'Id: {self.id}, Quantidade: {self.quantidade}, Id Tipo Picole: {self.id_tipo_picole}'

class Nota_Fiscal(ModelBase):

    __tablename__ = 'notas_fiscais'

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(DateTime, default=datetime.now)
    valor = Column(DECIMAL(8,2), nullable=False)
    numero_serie = Column(String, nullable=False)
    descricao = Column(String(200), nullable=False)

    id_revendedor = Column(Integer, ForeignKey('revendedores.id'))
    revendedor:Revendedor = orm.relationship('Revendedor', lazy='joined', innerjoin = True)

    lotes:List[Lote] = orm.relationship(
        'Lote', 
        secondary=lotes_notas_fiscais,
        backref='lote',
        lazy='dynamic'
    )

    def __repr__(self):
        return f'Nota fiscal: {self.numero_serie}'

class Usuario (ModelBase):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String(45), unique=True, nullable=False, index=True)
    email = Column(String(45), unique=True, nullable=False)
    hashed_password = Column(String(), nullable=False)
    disabled = Column(Boolean, default=False)