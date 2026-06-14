from fastapi import FastAPI, UploadFile, File
import pandas as pd
import io

app = FastAPI()

@app.post("/procesar-csv/")
async def procesar_csv(file: UploadFile = File(...)):
    # Leemos el archivo recibido
    content = await file.read()
    df = pd.read_csv(io.BytesIO(content))
    
    # --- AQUÍ HACES LA MAGIA ---
    # Ejemplo: Calcular estadística básica
    resumen = df.describe().to_dict()
    
    return {"mensaje": "Procesado", "estadisticas": resumen}