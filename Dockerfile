# define a imagem base
FROM continuumio/miniconda3

# define o mantenedor da imagem
LABEL maintainer="wanessa"

COPY api/ ./api/
COPY core/ ./core/
COPY models/ ./models/
COPY schemas/ ./schemas/
COPY ./main.py ./main.py
COPY ./requirements.txt ./requirements.txt


RUN pip install -r requirements.txt
RUN conda install psycopg2


# Expoe a porta 80
EXPOSE 80

# Comando para iniciar o UVICORN no Container
CMD ["uvicorn", "main:app" , "--host", "0.0.0.0", "--port", "80"]