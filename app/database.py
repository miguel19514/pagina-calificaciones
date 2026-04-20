import psycopg2
from dotenv import load_dotenv
import os

# Carga las variables del archivo .env
load_dotenv()


def get_connection():
    """
    Crea y retorna una conexión a la base de datos.
    Se llama cada vez que necesitamos hablar con PostgreSQL.
    """
    connection = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        port=os.getenv('DB_PORT')
    )
    return connection
