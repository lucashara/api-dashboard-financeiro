from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from config_bd import SessionLocal  # Importando a configuração do banco de dados
import json
from datetime import datetime

app = FastAPI()

# Habilita o CORS
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
def read_data():
    query = open("liberacao.sql", "r").read()
    try:
        with SessionLocal() as session:
            cursor = session.execute(query)
            columns = [col[0] for col in cursor.cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return Response(content=json.dumps(results, default=convert_datetime), media_type="application/json")
    except SQLAlchemyError as e:
        return Response(content=json.dumps({"error": "Erro ao acessar o banco de dados"}), media_type="application/json")

# Execute o servidor usando: uvicorn main:app --reload --host 0.0.0.0 --port 8001
