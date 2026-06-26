import requests

# URL de tu API (donde Burp la capturó)
url = "http://127.0.0.1:8000/login"

# Lista de payloads (datos maliciosos para probar inyecciones)
payloads = [
    "' OR '1'='1",
    "<script>alert(1)</script>",
    "'; DROP TABLE users;--",
    "admin' --",
    "{\"username\": {\"$gt\": \"\"}}" # Intento de inyección NoSQL
]

def run_fuzzer():
    print(f"Iniciando pruebas de seguridad en: {url}\n")
    
    for payload in payloads:
        data = {"username": "test_user", "password": payload}
        try:
            response = requests.post(url, json=data)
            print(f"Payload: {payload} | Status Code: {response.status_code}")
            
            # Si el código no es 401 o 422, es una posible vulnerabilidad
            if response.status_code not in [401, 422]:
                print(f"!!! POSIBLE VULNERABILIDAD ENCONTRADA CON: {payload} !!!")
        except Exception as e:
            print(f"Error al conectar: {e}")

if __name__ == "__main__":
    run_fuzzer()