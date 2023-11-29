from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from sqlalchemy.exc import SQLAlchemyError
from config_bd import SessionLocal, text
import json
from datetime import datetime, timedelta
from decimal import Decimal

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuração do Middleware GZip para compressão das respostas
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Função de conversão personalizada para JSON
def convert_datetime(obj):
    """
    Converte objetos datetime e Decimal para serem serializáveis em JSON.
    :param obj: Objeto a ser convertido.
    :return: Representação string do objeto.
    """
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

# Cache para armazenar as consultas e seus tempos
cache = {}

# Função de cache para consultas SQL
def cached_query(query: str, expire_delta: timedelta):
    """
    Executa a consulta SQL e armazena o resultado no cache.
    :param query: Consulta SQL como string.
    :param expire_delta: Tempo para expiração do cache.
    :return: Resultado da consulta.
    """
    now = datetime.now()
    if query not in cache or (now - cache[query]['time']).total_seconds() > expire_delta.total_seconds():
        with SessionLocal() as session:
            cursor = session.execute(text(query))
            columns = [col[0] for col in cursor.cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            cache[query] = {'time': now, 'data': results}
    return cache[query]['data']

# Endpoint para a rota "/liberacao"
@app.get("/liberacao")
def read_liberacao_data():
    """
    Endpoint para obter dados de liberação.
    :return: Dados de liberação em formato JSON.
    """
    query = open("liberacao.sql", "r").read()
    return Response(content=json.dumps(cached_query(query, timedelta(seconds=60)), default=convert_datetime), media_type="application/json")

# Endpoint para a rota "/pcprest"
@app.get("/pcprest")
def read_pcprest_data():
    """
    Endpoint para obter dados do PCPrest.
    :return: Dados do PCPrest em formato JSON.
    """
    query = open("pcprest.sql", "r").read()
    return Response(content=json.dumps(cached_query(query, timedelta(seconds=60)), default=convert_datetime), media_type="application/json")

# Comando para execução do servidor (normalmente colocado fora do arquivo main.py)
# uvicorn main:app --reload --host 0.0.0.0 --port 8001