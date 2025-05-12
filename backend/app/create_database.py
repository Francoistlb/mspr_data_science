import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis .env
load_dotenv()

# Extraire les infos de connexion de l'URL complète
from urllib.parse import urlparse

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL non défini dans le fichier .env")

# Parser l'URL
parsed = urlparse(DATABASE_URL)
user = parsed.username
password = parsed.password
host = parsed.hostname
port = parsed.port or 5432
db_name = parsed.path.lstrip('/')


try:
    conn = psycopg2.connect(
        dbname='postgres', 
        user=user,
        password=password,
        host=host,
        port=port
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    cur.execute(f"CREATE DATABASE {db_name} ENCODING 'UTF8' TEMPLATE template0;")
    print(f"✅ Base de données '{db_name}' créée avec succès.")

except psycopg2.errors.DuplicateDatabase:
    print(f"⚠️ La base de données '{db_name}' existe déjà.")
except Exception as e:
    print(f"❌ Erreur lors de la création : {e}")
finally:
    if conn:
        conn.close()
