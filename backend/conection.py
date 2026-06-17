import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 1. Obtenemos la ruta absoluta de la carpeta 'backend'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Construimos la ruta hacia el archivo .db: 
#    Subimos un nivel (..) desde 'backend' hacia la raíz, y luego entramos a 'Data'
DATABASE_PATH = os.path.join(os.path.dirname(BASE_DIR), "Data", "Data_info.db")

# 3. Formateamos correctamente la URL para SQLite (necesita el prefijo sqlite:///)
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Configuración de conexión
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()