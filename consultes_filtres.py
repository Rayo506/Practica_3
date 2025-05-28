import json  # Per treballar amb fitxers JSON

# Ruta relativa del fitxer JSON amb les metadades de les imatges
JSON_PATH = "db_img_metadades.json"

# Obrim i llegim el fitxer JSON
with open(JSON_PATH, 'r') as f:
    data = json.load(f)  # Carreguem el JSON sencer com un diccionari Python

# El JSON té una clau "_default" que conté un diccionari amb les imatges
images_dict = data.get("_default", {})  # Obtenim el diccionari d’imatges, o un dict buit si no existeix

# Convertim el diccionari d’imatges (clau: "1", "2", etc.) a una llista amb només els valors (els dicts de cada imatge)
images = list(images_dict.values())

# ----------------------------
# Funcions per fer consultes
# ----------------------------

def list_images_by_format(images, format_type):
    """
    Retorna una llista amb les imatges que tenen el format indicat.
    El format no diferencia majúscules/minúscules.
    """
    return [img for img in images if img['format'].upper() == format_type.upper()]

def list_images_after_date(images, date_str):
    """
    Retorna les imatges modificades després d’una data concreta.
    El camp 'modified' té format "YYYY-MM-DDTHH:MM:SS", per això només agafem els primers 10 caràcters (la data).
    La data a filtrar ha de ser en format "YYYY-MM-DD".
    """
    return [img for img in images if img['modified'][:10] > date_str]

def average_resolution(images):
    """
    Calcula la resolució mitjana (ample i alt) de les imatges.
    El camp 'size' és una llista [ample, alt].
    Si no hi ha imatges, retorna (0, 0).
    """
    if not images:
        return 0, 0
    total_width = sum(img['size'][0] for img in images)    # Sumem totes les amplades
    total_height = sum(img['size'][1] for img in images)   # Sumem totes les alçades
    n = len(images)                                        # Nombre total d’imatges
    return total_width // n, total_height // n             # Mitjana arrodonida per baix (enter)

# ----------------------------
# Executem les consultes
# ----------------------------

jpeg_images = list_images_by_format(images, "JPEG")       # Imatges JPEG
png_images = list_images_by_format(images, "PNG")         # Imatges PNG
webp_images = list_images_by_format(images, "WEBP")       # Imatges WEBP
recent_images = list_images_after_date(images, "2025-05-25")  # Imatges modificades després del 25 de maig 2025

avg_w, avg_h = average_resolution(images)                 # Resolució mitjana de totes les imatges

# ----------------------------
# Preparem el diccionari amb tots els resultats a exportar
# ----------------------------

resultats = {
    "jpeg_images": jpeg_images,
    "png_images": png_images,
    "webp_images": webp_images,
    "recent_images": recent_images,
    "average_resolution": {
        "width": avg_w,
        "height": avg_h
    }
}

# ----------------------------
# Exportem tot el diccionari a un sol fitxer JSON amb indentació per facilitar la lectura
# ----------------------------

with open("resultats_complets.json", "w") as f:
    json.dump(resultats, f, indent=4)   # Guardem 'resultats' a 'resultats_complets.json'

# ----------------------------
# Informem per pantalla dels resultats obtinguts
# ----------------------------

print("Resultats exportats a 'resultats_complets.json'")
print(f"Resolució mitjana: {avg_w}x{avg_h}")
print(f"Imatges JPEG: {len(jpeg_images)}")
print(f"Imatges PNG: {len(png_images)}")
print(f"Imatges WEBP: {len(webp_images)}")
print(f"Imatges modificades després del 2025-05-25: {len(recent_images)}")
