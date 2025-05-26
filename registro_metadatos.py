import os
from datetime import datetime
from PIL import Image # Pillow, para extraer los datos de formato, mida en pixels, etc..
from tinydb import TinyDB

# Ruta on buscarem les imatges
IMG_FOLDER = os.path.join('.', 'multimedia', 'imgs')

# Obrim TinyDB
db = TinyDB('db_img_metadades.json')

for fname in os.listdir(IMG_FOLDER):
    path = os.path.join(IMG_FOLDER, fname)
    # Solo arxius amb extension d’imatge
    if not os.path.isfile(path) or not fname.lower().endswith(('.jpg','.jpeg','.png','bmp','gif')):
        continue

    # Obtenim metadades amb Pillow
    with Image.open(path) as img:
        width, height = img.size
        fmt = img.format

    # Data de modificació del fitxer
    mtime = os.path.getmtime(path)
    modified = datetime.fromtimestamp(mtime).isoformat(timespec='seconds')

    # Insertem a TinyDB
    fila = {
        'filename': fname,
        'format': fmt,
        'size': [width, height],
        'modified': modified
    }
    db.insert(fila)
    print(f"Afegit: {fila}")

db.close()
print("Totes les metadades s'han registrat a db_img_metadades.json")
