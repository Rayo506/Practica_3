"""
Objectiu específic: Integrar consultes amb Oracle i transferència de dades cap a 
TinyDB, treballant sobre documents XML generats prèviament.
Consigna:
1. Accedeix a la base Oracle on semmagatzemen documents XML a la taula 
DocumentsXML.

2. Utilitza XQuery per extreure per cada document:
- producte_id
- quantitat dimatges referenciades
- llista de formats utilitzats
- títol del producte (si està inclòs)

3. Insereix les dades obtingudes a TinyDB amb aquesta estructura:
{'producte_id': 101, 'num_imatges': 3, 'formats': ['jpg', 'png'], 'titol': 'Producte Exemple'}

4. Mostra per consola: X
- Total de productes
- Mitjana dimatges per producte
- Formats més freqüents
"""

import cx_Oracle
import sys
from tinydb import TinyDB
from collections import Counter

# Configuració de la connexió a la base de dades Oracle
DB_USER = "SYSTEM"
DB_PASS = "oracle"
DB_DSN  = "192.168.56.2/FREEPDB1"

db = TinyDB('DocumentsXML')


def acces_DocumentsXML(): #conexion 
    
    #Intenta establir una connexió amb la base de dades Oracle.
    #En cas d'error, mostra missatge i surt del programa.
    
    try:
        conn = cx_Oracle.connect(DB_USER, DB_PASS, DB_DSN)
        return conn
    except cx_Oracle.Error as e:
        print(f"[ERROR] No s'ha pogut connectar a la base de dades: {e}")
        print("Comprova les credencials o la configuració de connexió.")
        sys.exit(1)

from tinydb import TinyDB, Query
import cx_Oracle

db = TinyDB('data.json')
all_items = Query()

def dades_XQuery():
    conn = acces_DocumentsXML()
    cursor = None

    if len(db) > 0:  # Verifica si la base de datos tiene contenido
        db.remove(all_items)

    try:
        cursor = conn.cursor()

        cursor.execute("""
        SELECT extractValue(value(t), '/imatge/@producte_id') as producte_id, 
               extractValue(value(t), '/imatge/@descripcio_imatge') as descripcio_imatge,
               extractValue(value(t), '/imatge/@format_imatge') as format_imatge
        FROM DocumentsXML d,
            TABLE(XMLSequence(
                EXTRACT(d.xml_data, '/producte/imatges/imatge')
            )) t
        """)

        conteo_imatges = {}  # Diccionario para contar imágenes por producto

        for row in cursor:
            pro_id = row.producte_id
            format = row.format_imatge
            titol = row.descripcio_imatge

            if pro_id not in conteo_imatges:
                conteo_imatges[pro_id] = 1
            else:
                conteo_imatges[pro_id] += 1

            db.insert({
                'producte_id': pro_id,
                'num_imatges': conteo_imatges[pro_id],
                'formats': format,
                'titol': titol
            })

    except cx_Oracle.Error as e:
        print(f"Error XQuery: {e}")
    finally:
        if cursor:
            cursor.close()
        conn.close()



def MuestraXConsola():
    # Total de productes
    total = len(db)
    print(f"Total de productes: {total}\n")

    # Mitjana d’imatges per producte
    imatges = [item['num_imatges'] for item in db]
    mitjana = sum(imatges) / len(imatges) if imatges else 0
    print(f"Mitjana d’imatges per producte: {mitjana:.2f}\n")

    # Formats més freqüents
    formats = [item['formats'] for item in db]
    freq = Counter(formats).most_common()

    print("Formats més freqüents:")
    for fmt, count in freq:
        print(f"{fmt}: {count}")
    print()


# Programa principal
if __name__ == "__main__":
    print("Migracion parcial de datos de la tabla de DocumetosXML...")

    # Guardar los datos en TinyDB
    dades_XQuery()

    # Datos que mostrar por terminal
    MuestraXConsola()

    print("Script finalitzado")


