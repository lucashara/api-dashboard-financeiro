from fastapi import FastAPI, Response, Query, HTTPException
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
app.add_middleware(GZipMiddleware, minimum_size=500)

# Função de conversão personalizada para JSON
def convert_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

# Cache para armazenar as consultas e seus tempos
cache = {}

# Função para validar formato de data
def validate_date(date_str):
    try:
        return datetime.strptime(date_str, '%d-%m-%Y')
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de data inválido. Use DD-MM-AAAA.")

# Função de cache para consultas SQL
def cached_query(query: str, datainicial: str, datafinal: str, expire_delta: timedelta):
    # Validação das datas
    data_ini = validate_date(datainicial)
    data_fin = validate_date(datafinal)

    if data_ini > data_fin:
        raise HTTPException(status_code=400, detail="Data inicial deve ser anterior ou igual à data final.")

    now = datetime.now()
    cache_key = f"{query}-{datainicial}-{datafinal}"
    if cache_key not in cache or (now - cache[cache_key]['time']).total_seconds() > expire_delta.total_seconds():
        with SessionLocal() as session:
            cursor = session.execute(text(query), {"DATAINICIAL": datainicial, "DATAFINAL": datafinal})
            columns = [col[0] for col in cursor.cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            cache[cache_key] = {'time': now, 'data': results}
    return cache[cache_key]['data']

# Endpoint genérico com parâmetros de data
def create_data_endpoint(path: str, query_file: str):
    @app.get(path)
    def endpoint(datainicial: str = Query(...), datafinal: str = Query(...)):
        query = open(query_file, "r").read()
        return Response(content=json.dumps(cached_query(query, datainicial, datafinal, timedelta(seconds=60)), default=convert_datetime), media_type="application/json")
    return endpoint

# Criando endpoints
create_data_endpoint("/liberacao", "liberacao.sql")
create_data_endpoint("/pcprest", "pcprest.sql")
create_data_endpoint("/pago", "pago.sql")
create_data_endpoint("/inadimplente", "inadimplente.sql")
create_data_endpoint("/receber", "receber.sql")
create_data_endpoint("/bonificado", "bonificado.sql")
create_data_endpoint("/pedidos", "pedidos.sql")

# uvicorn main:app --reload --host 0.0.0.0 --port 8001

# https://sga.grupobrf1.com:8445/

# https://sga.grupobrf1.com:4444/pago?datainicial=28-12-2023&datafinal=28-12-2023
# https://sga.grupobrf1.com:4444/pago?datainicial=28-12-2023&datafinal=28-12-2023
# https://sga.grupobrf1.com:4444/liberacao?datainicial=28-12-2023&datafinal=28-12-2023
# https://sga.grupobrf1.com:4444/pago?datainicial=28-12-2023&datafinal=28-12-2023
# https://sga.grupobrf1.com:4444/inadimplente?datainicial=28-12-2023&datafinal=28-12-2023
# https://sga.grupobrf1.com:4444/receber?datainicial=28-12-2023&datafinal=28-12-2023
# https://sga.grupobrf1.com:4444/pcprest?datainicial=28-12-2023&datafinal=28-12-2023
