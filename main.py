solicitudes de importación
importar sistema operativo
desde datetime importar datetime

# Variables de entorno
TOKEN DE ACCESO = os.getenv("TOKEN DE PÁGINA DE FB")
ID DE PÁGINA = "720700281430215"

# Crear carpeta de memoria si no existe
os.makedirs("memoria", existe_ok=True)
MEMORY_FILE = "memoria/publicaciones_memoria.txt"

def obtener_publicaciones(page_id, access_token, limit=100):
    url = f"https://graph.facebook.com/v19.0/{page_id}/posts"
    parámetros = {
        "token_de_acceso": token_de_acceso,
        "campos": "id,mensaje,hora_de_creación",
        "límite": límite
    }
    publicaciones = []
    mientras que URL:
        r = solicitudes.get(url, params=params)
        datos = r.json()
        publicaciones.extend(data.get("datos", []))
        url = datos.get("paginación", {}).get("siguiente")
        params = Ninguno # sólo usar params en la primera solicitud
    volver publicaciones

def extraer_nombre_oculto(texto):
    lineas = texto.split("\n")
    para linea en reversa(lineas):
        if any(nombre in linea.lower() for nombre in ["asesor", "contacto", "federico", "juan", "martin"]):
            devolver linea.strip()
    devolver "No identificado"

def guardar_en_memoria(publicaciones):
    con open(MEMORY_FILE, "w", encoding="utf-8") como f:
        para pub en publicaciones:
            mensaje = pub.get("mensaje", "").replace("\n", " ").strip()
            fecha = pub.get("hora_de_creación", "")
            asesor = extraer_nombre_oculto(mensaje)
            f.write(f"{fecha} | ID: {pub['id']} | Asesor: {asesor}\n")
            f.write(f"{mensaje}\n")
            f.write("-" * 60 + "\n")
    print(f"Se guardaron {len(publicaciones)} publicaciones en {MEMORY_FILE}")

si __nombre__ == "__principal__":
    token = TOKEN_DE_ACCESO
    si no es token:
        print("Falta el token de acceso en la variable de entorno FB_PAGE_TOKEN")
    demás:
        publicaciones = obtener_publicaciones(PAGE_ID, token)
        guardar_en_memoria(publicaciones)
