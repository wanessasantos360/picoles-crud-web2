# Aplicação de Gerenciamento de Picolés

Este projeto é uma aplicação web para gerenciar dados de produção e vendas de picolés, desenvolvido com **FastAPI**, **SQLAlchemy** e **Docker**.

## Estrutura do Projeto:

- `api/`: Contém os arquivos de rota e lógica de cada recurso (picolés, ingredientes, etc.).

- `core/`: Contém a configuração do banco de dados e dependências da aplicação.

- `models/`: Contém os modelos SQLAlchemy que representam as tabelas do banco de dados.

- `schemas/`: Contém os schemas Pydantic para validação de dados.

- `create_tables.py`: Script para criar tabelas no banco de dados.

- `docker-compose.yml`: Arquivo de configuração dos containers Docker.

- `Dockerfile`: Configuração do ambiente de execução da aplicação.

## Requisitos

- Docker
- Python 3.9 

## Como Rodar a Aplicação

### 1. Clone o Repositório

Clone este repositório em seu ambiente local:
```
git clone https://github.com/wanessasantos360/picoles-crud-web2.git
cd picoles-crud-web2
```

### 2. Configure o Ambiente com Docker Compose

Ajuste o Docker Compose para configurar os containers **PostgreSQL**, **PgAdmin** e a *aplicação principal*.

- postgres_db: Banco de dados PostgreSQL.
- pgadmin: Interface de administração do PostgreSQL.

### 3. Inicie os Containers

Execute o comando abaixo para subir os serviços:

```
docker-compose up --build
```

> Comando para derrubar: `docker-compose down`

FastAPI (Swagger UI): http://localhost:80/docs

PgAdmin: http://localhost:81

### 4. Configure o Banco de Dados

No PgAdmin:

Acesse o PgAdmin em http://localhost:81

Use as credenciais configuradas no docker-compose.yml:

- Email: meuemail@gmail.com

- Senha: PgAdmin2019!

Crie uma conexão com o banco de dados PostgreSQL:

- Host: postgres_db

- Porta: 5432

- Usuário: postgres

- Senha: Postgres2024!

- Database: dbpicoles

### 5. Crie as Tabelas

Execute o script `create_tables.py` 

```
docker exec -it <nome-do-container-da-aplicacao> python create_tables.py
```

### 6. Teste a Aplicação

Acesse a interface do Swagger UI para testar os endpoints da aplicação:

URL: http://localhost:80/docs

Você pode realizar operações como:

- Criar registros de picolés.

- Consultar tabelas.

- Atualizar e deletar informações.

---

## Desenvolvimento Local (Sem Docker)

Se preferir rodar localmente, siga os passos abaixo:

### 1. Crie um ambiente virtual:

```
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate   # Windows
```

### 2. Instale as dependências:

```
pip install -r requirements.txt
```

### 3. Configure o arquivo de conexão ao banco de dados em core/db.py.

É só comentar a outra linha e colocar o nome do host para localhost


~~~python
engine = create_engine(
    "postgresql+psycopg2://postgres:Postgres2024!@localhost:5432/dbpicoles")

'''
engine = create_engine(
"postgresql+psycopg2://postgres:Postgres2024!@postgres_db:5432/dbpicoles")'''
~~~

### 4. Inicie a aplicação:

```
$ uvicorn main:app --reload
```

---

### No Cloud9
```
$ wget https://github.com/wanessasantos360/picoles-crud-web2/archive/refs/heads/main.zip
$ sudo apt-get install unzip python3-venv
$ unzip main.zip
$ cd picoles-crud-web2-main/
```