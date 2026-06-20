import os
import logging
from fastapi import FastAPI, Depends, HTTPException, Form
from sqlalchemy import text
from sqlalchemy.orm import Session
from conection import get_db
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite peticiones desde cualquier lugar (perfecto para desarrollo)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (POST, GET, etc.)
    allow_headers=["*"],
)

@app.post("/register")
def register(
    user_name: str = Form(...), 
    password: str = Form(...), 
    db: Session = Depends(get_db)
):
    # 1. Verificar si el usuario ya existe
    # ESTA ES LA CORRECTA (Usa el nombre real de la columna)
    query_check = text("SELECT user_id FROM users WHERE user_name = :user_name")
    result = db.execute(query_check, {"user_name": user_name}).fetchone()
    
    if result:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    
    if os.getenv("ENV") == "development":
        logger.debug(f"Intentando registrar usuario: {user_name}")
    
    # 2. Insertar en tabla 'users'
    # 1. Insertar el nombre de usuario
    insert_user = text("INSERT INTO users (user_name) VALUES (:user_name)")
    db.execute(insert_user, {"user_name": user_name})

    # 2. Recuperar el ID generado automáticamente por la BD
    # Esto es vital para saber qué ID le asignó la base de datos al nuevo usuario
    result = db.execute(text("SELECT last_insert_rowid()"))
    user_id = result.scalar()

    #print(f"DEBUG - Tipo de password: {type(password)}")
    #print(f"DEBUG - Valor de password: {password}")
    # 1. Aseguramos que sea una cadena y la cortamos a 72 caracteres
    safe_password = str(password)[:72]
    
    # 2. Hasheamos con una lógica muy robusta
    try:
        hashed_password = pwd_context.hash(safe_password)
    except Exception as e:
        print(f"DEBUG: Error al hashear: {e}")
        raise HTTPException(status_code=500, detail="Error interno de seguridad")
    insert_auth = text("INSERT INTO user_auth (user_id, password_hash) VALUES (:user_id, :password_hash)")
    db.execute(insert_auth, {"user_id": user_id, "password_hash": hashed_password})
    
    db.commit()
    return {
        "message": "Usuario registrado exitosamente",
        "username": user_name,
        "status": "success"
    }

@app.post("/login")
def login(
    username: str = Form(...), # FastAPI recibe esto como 'username' del formulario
    password: str = Form(...), 
    db: Session = Depends(get_db)
):
    # CORRECCIÓN: Usamos 'user_name' (el nombre de la columna real)
    # pero pasamos el valor que recibimos del parámetro 'username'
    query = text("""
        SELECT auth.password_hash 
        FROM users u
        JOIN user_auth auth ON u.user_id = auth.user_id
        WHERE u.user_name = :user_name
    """)
    
    # Aquí mapeamos el valor recibido al parámetro de la consulta
    result = db.execute(query, {"user_name": username}).fetchone()
    
    if not result or not pwd_context.verify(password, result[0]):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
        
    return {"message": "Login exitoso"}