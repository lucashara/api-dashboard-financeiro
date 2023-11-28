from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from config_bd import SessionLocal, text
import json
from datetime import datetime
from decimal import Decimal


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def convert_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

@app.get("/liberacao")
def read_liberacao_data():
    query = open("liberacao.sql", "r").read()
    return execute_query(query)

@app.get("/pcprest")
def read_pcprest_data():
    query = open("pcprest.sql", "r").read()
    return execute_query(query)

def execute_query(query):
    try:
        with SessionLocal() as session:
            cursor = session.execute(text(query))
            columns = [col[0] for col in cursor.cursor.description]
            results = []
            for row in cursor.fetchall():
                row_dict = {}
                for col_name, value in zip(columns, row):
                    if col_name == 'DATAVENCIMENTO' and isinstance(value, datetime):
                        row_dict[col_name] = value.strftime('%Y-%m-%d')
                    elif isinstance(value, Decimal):
                        row_dict[col_name] = float(value)
                    else:
                        row_dict[col_name] = value
                results.append(row_dict)

            return Response(content=json.dumps(results, default=convert_datetime), media_type="application/json")
    except SQLAlchemyError as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        return Response(content=json.dumps({"error": "Erro ao acessar o banco de dados"}), media_type="application/json")

    
def convert_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, Decimal):  # Adiciona esta linha para lidar com objetos Decimal
        return float(obj)  # Ou str(obj) se você preferir representar os decimais como strings
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


# Para executar o servidor use: uvicorn main:app --reload --host 0.0.0.0 --port 8001
