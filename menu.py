"""
Sistema de Consulta Multimèdia amb TinyDB
Opcions:
1. Indexar nous productes des de documents XML (simulats)
2. Cercar productes per format d’imatge (ex: JPG)
3. Modificar el títol d’un producte
4. Eliminar productes sense imatges
5. Mostrar resum estadístic global
6. Sortir
"""

import os
import glob
import xml.etree.ElementTree as ET
from tinydb import TinyDB, Query
from collections import Counter

DB_PATH = "DocumentsXML"
XML_FOLDER = "./xml_samples/"

def parse_producte_xml(filepath):
    """
    Extreu dades d'un fitxer XML de producte.
    Retorna un diccionari amb: producte_id, num_imatges, formats, titol
    """
    tree = ET.parse(filepath)
    root = tree.getroot()
    producte_id = int(root.findtext("producte_id"))
    titol = root.findtext("titol", default="")
    imatges = root.find("imatges")
    formats = []
    if imatges is not None:
        for imatge in imatges.findall("imatge"):
            fmt = imatge.get("format")
            if fmt:
                formats.append(fmt.lower())
    return {
        "producte_id": producte_id,
        "num_imatges": len(formats),
        "formats": list(set(formats)),  # sense duplicats
        "titol": titol
    }

def indexar_xmls(db):
    """
    Opció 1: Indexa tots els XML de la carpeta xml_samples/ a TinyDB.
    """
    xml_files = glob.glob(os.path.join(XML_FOLDER, "*.xml"))
    nous = 0
    for xml in xml_files:
        dades = parse_producte_xml(xml)
        # Evita duplicats pel producte_id
        if not db.search(Query().producte_id == dades["producte_id"]):
            db.insert(dades)
            nous += 1
    print(f"{nous} productes nous indexats.")

def cercar_per_format(db):
    """
    Opció 2: Cerca productes que continguin imatges d’un format determinat.
    """
    fmt = input("Introdueix el format d’imatge (ex: jpg): ").strip().lower()
    Producte = Query()
    resultats = db.search(Producte.formats.any([fmt]))
    if not resultats:
        print("Cap producte trobat amb aquest format.")
    else:
        print(f"Productes amb imatges format {fmt.upper()}:")
        for prod in resultats:
            print(f"- ID: {prod['producte_id']} | Títol: {prod['titol']} | #Imatges: {prod['num_imatges']} | Formats: {', '.join(prod['formats'])}")

def modificar_titol(db):
    """
    Opció 3: Modifica el títol d’un producte pel seu producte_id.
    """
    try:
        pid = int(input("Introdueix el producte_id: "))
    except ValueError:
        print("ID no vàlid.")
        return
    nou_titol = input("Nou títol: ").strip()
    Producte = Query()
    if db.update({"titol": nou_titol}, Producte.producte_id == pid):
        print("Títol actualitzat.")
    else:
        print("No s'ha trobat cap producte amb aquest ID.")

def eliminar_sense_imatges(db):
    """
    Opció 4: Elimina productes amb num_imatges = 0.
    """
    Producte = Query()
    eliminats = db.remove(Producte.num_imatges == 0)
    print(f"{len(eliminats)} productes eliminats.")

def mostrar_estadistiques(db):
    """
    Opció 5: Mostra estadístiques generals.
    """
    tots = db.all()
    if not tots:
        print("No hi ha productes a la base de dades.")
        return
    total = len(tots)
    mitjana = sum(p["num_imatges"] for p in tots) / total
    # Comptar tots els formats
    tots_formats = []
    for p in tots:
        tots_formats.extend(p["formats"])
    if tots_formats:
        format_mes_comu, freq = Counter(tots_formats).most_common(1)[0]
    else:
        format_mes_comu, freq = "Cap", 0
    print(f"Total de productes: {total}")
    print(f"Mitjana d’imatges per producte: {mitjana:.2f}")
    print(f"Format més comú: {format_mes_comu.upper()} ({freq} vegades)")

def main():
    db = TinyDB(DB_PATH)
    while True:
        print("\n--- Menú de Gestió Multimèdia ---")
        print("1. Indexar nous productes des de documents XML")
        print("2. Cercar productes per format d’imatge")
        print("3. Modificar el títol d’un producte")
        print("4. Eliminar productes sense imatges")
        print("5. Mostrar resum estadístic global")
        print("6. Sortir")
        op = input("Opció? ").strip()
        if op == "1":
            indexar_xmls(db)
        elif op == "2":
            cercar_per_format(db)
        elif op == "3":
            modificar_titol(db)
        elif op == "4":
            eliminar_sense_imatges(db)
        elif op == "5":
            mostrar_estadistiques(db)
        elif op == "6":
            print("Sortint...")
            db.close()
            break
        else:
            print("Opció no vàlida.")

if __name__ == "__main__":
    main()