import csv
import re
import os
import psycopg2
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine

# Copiado de: https://github.com/juanluisacebal/airflow_mis_dags/blob/main/CSV_SERVER_CSV_upload_ctas_postgres.py


BASE_DIR = os.getcwd()

# Cargar .env desde BASE_DIR
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))

PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_DATABASE = os.getenv("PG_DATABASE")

# CSV en subdirectorio 'files'
LOCAL_CSV = os.path.join(BASE_DIR, "files", "Data_example_-_Python_Coding_Challenge_-_GraphQL.csv")

def load_csv_and_create_table_postgres():
    """
    Carga un CSV local y lo inserta en PostgreSQL.
    1. Crea una tabla staging.
    2. Inserta los datos.
    3. Crea la tabla final `challenge_graphql_nlp_api`.
    """
    print("Cargando CSV y creando tabla en PostgreSQL...")
    connection = psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        user=PG_USER,
        password=PG_PASSWORD,
        dbname=PG_DATABASE
    )
    cursor = connection.cursor()

    print("Leyendo y parseando CSV...")
    print(f"Ruta absoluta esperada del CSV: {LOCAL_CSV}")

    import urllib.request

    CSV_URL = "https://file.notion.so/f/f/8bdb40ef-cc0d-4853-862c-95ff2b4790ca/b82763a3-3ac0-4c8a-99bb-d763c0b00b54/Data_example_-_Python_Coding_Challenge_-_GraphQL.csv?table=block&id=3e5c15a8-875d-43ae-b866-c1515de08c01&spaceId=8bdb40ef-cc0d-4853-862c-95ff2b4790ca&expirationTimestamp=1745366400000&signature=AmH4rnK8MxZKqA66BRo-5RvzpY1K29pBns_AHzmf_3w&downloadName=Data+example+-+Python+Coding+Challenge+-+GraphQL.csv"

    if not os.path.exists(LOCAL_CSV):
        print(f"🔽 Descargando CSV desde {CSV_URL}...")
        os.makedirs(os.path.dirname(LOCAL_CSV), exist_ok=True)
        urllib.request.urlretrieve(CSV_URL, LOCAL_CSV)
        print(f"✅ Archivo descargado en {LOCAL_CSV}")

    if not os.path.exists(LOCAL_CSV):
        raise FileNotFoundError(f"❌ No se encontró el archivo CSV en {LOCAL_CSV}. Verifica que esté en la ruta esperada.")

    print("Cargando CSV con pandas...")
    df = pd.read_csv(LOCAL_CSV)

    print("Insertando CSV como tabla en PostgreSQL...")
    engine = create_engine(f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}")
    df.to_sql("stg_challenge_graphql_nlp_api", engine, index=False, if_exists="replace")

    # 3. Crear tabla final
    print("Creando tabla final...")
    cursor.execute("""
        DROP TABLE IF EXISTS challenge_graphql_nlp_api;
        CREATE TABLE challenge_graphql_nlp_api AS
        SELECT * FROM stg_challenge_graphql_nlp_api;
    """)
    connection.commit()
    connection.close()


if __name__ == "__main__":
    print("Main")
    load_csv_and_create_table_postgres()