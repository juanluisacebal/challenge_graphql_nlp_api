import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

from .models import Base, ChallengeData
from .database import engine

def init_db():
    """
    Inicializa la base de datos y carga los datos del CSV.
    """
    # Crear tablas
    Base.metadata.create_all(bind=engine)

    # Cargar datos del CSV
    csv_path = os.path.join(os.getcwd(), "files", "Data_example_-_Python_Coding_Challenge_-_GraphQL.csv")
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"No se encontró el archivo CSV en {csv_path}")

    # Leer CSV con pandas
    df = pd.read_csv(csv_path)
    
    # Insertar datos en la base de datos
    df.to_sql(
        "challenge_graphql_nlp_api",
        engine,
        if_exists="replace",
        index=False
    )

if __name__ == "__main__":
    init_db() 