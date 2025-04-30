import requests
import csv

# Token de acceso de tu página (pegá aquí tu token completo entre comillas)
ACCESS_TOKEN = 'EAARIliGvlXUBOxvx9K2cZBEsA0WmC61LDn6rBEUOCpVJz7n32MXXZALl0SXbrOb60Vz0Sck041PcD2VeCjdS8MCQCZBO7OqZB3vFcZAo0a6GhHF9YhY30XpkZCcyG5ZCK8x3mZBJLvb7MCTVLVApdkeSXOFtRs1W4ge9lqiKssU0QsN381cDXZCvqaErW2R2z'

# ID de tu página
PAGE_ID = '720700281430215'

# URL de consulta para traer los grupos
url = f'https://graph.facebook.com/v19.0/{PAGE_ID}/groups?access_token={ACCESS_TOKEN}'

# Hacer la solicitud
response = requests.get(url)
data = response.json()

# Mostrar los grupos en consola
print("Grupos encontrados:\n")
groups = data.get('data', [])

if not groups:
    print("No se encontraron grupos asociados.")
else:
    for group in groups:
        print(f"Nombre: {group.get('name')} | ID: {group.get('id')}")

    # Guardar en un CSV
    with open('grupos_pagina.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nombre del Grupo', 'ID del Grupo'])
        for group in groups:
            writer.writerow([group.get('name'), group.get('id')])

    print("\n¡Grupos guardados en grupos_pagina.csv!")