import os
import requests

# Variables de entorno
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PAGE_ID = os.getenv("PAGE_ID", "720700281430215")
API_VERSION = os.getenv("API_VERSION", "v22.0")
MEMORY_FILE = "memoria/publicaciones_memoria.txt"

os.makedirs("memoria", exist_ok=True)

def obtener_publicaciones(page_id, access_token, limit=100):
    url = f"https://graph.facebook.com/{API_VERSION}/{page_id}/posts"
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
        params = None  # Solo usar en la primera request
    return publicaciones

def extraer_nombre_oculto(texto):
    if not texto:
        return "No identificado"
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
    if not ACCESS_TOKEN:
        print("Falta la variable de entorno ACCESS_TOKEN.")
    else:
        publicaciones = obtener_publicaciones(PAGE_ID, ACCESS_TOKEN)
        guardar_en_memoria(publicaciones)
