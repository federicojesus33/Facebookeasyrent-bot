import requests
import os
from datetime import datetime

# Variables de entorno
ACCESS_TOKEN = os.getenv("FB_PAGE_TOKEN")
PAGE_ID = "720700281430215"

# Crear carpeta de memoria si no existe
os.makedirs("memoria", exist_ok=True)
MEMORY_FILE = "memoria/publicaciones_memoria.txt"

def obtener_publicaciones(page_id, access_token, limit=100):
    url = f"https://graph.facebook.com/v19.0/{page_id}/posts"
    params = {
        "access_token": access_token,
        "fields": "id,message,created_time",
        "limit": limit
    }
    publicaciones = []
    while url:
        r = requests.get(url, params=params)
        data = r.json()
        publicaciones.extend(data.get("data", []))
        url = data.get("paging", {}).get("next")
        params = None  # Solo en la primera solicitud
    return publicaciones

def extraer_nombre_oculto(texto):
    lineas = texto.split("\n")
    for linea in reversed(lineas):
        if any(nombre in linea.lower() for nombre in ["asesor", "contacto", "federico", "juan", "martin"]):
            return linea.strip()
    return "No identificado"

def guardar_en_memoria(publicaciones):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        for pub in publicaciones:
            mensaje = pub.get("message", "").replace("\n", " ").strip()
            fecha = pub.get("created_time", "")
            asesor = extraer_nombre_oculto(mensaje)
            f.write(f"{fecha} | ID: {pub['id']} | Asesor: {asesor}\n")
            f.write(f"{mensaje}\n")
            f.write("-" * 60 + "\n")
    print(f"Se guardaron {len(publicaciones)} publicaciones en {MEMORY_FILE}")

if __name__ == "__main__":
    token = ACCESS_TOKEN
    if not token:
        print("Falta el token de acceso en la variable de entorno FB_PAGE_TOKEN")
    else:
        publicaciones = obtener_publicaciones(PAGE_ID, token)
        guardar_en_memoria(publicaciones)
