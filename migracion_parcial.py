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
from tinydb import TinyDB, Query
from collections import Counter

# Configuració de la connexió a la base de dades Oracle
DB_USER = "SYSTEM"
DB_PASS = "oracle"
DB_DSN  = "192.168.56.2/FREEPDB1"

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

def dades_XQuery():

    # Extaccion por cada documento
    # Inserccion de datos obtinidos a TinyDB

    conn = acces_DocumentsXML()
    cursor = None

    db = TinyDB('DocumentsXML')
    if (db.get(all) > 0): #Si tiene contenido reescribirlo
        db.remove(all)

    #### MODIFICAR [
    try:
        cursor = conn.cursor()

        cursor.execute("""
        SELECT id, extractValue(value(t), '/imatge/@producte_id') as producte_id, 
        extractValue(value(t), '/imatge/@descripcio_imatge') as descripcio_imatge,
        extractValue(value(t), '/imatge/@format_imatge') as format_imatge
        FROM DocumentsXML d,
            TABLE(XMLSequence(
                EXTRACT(d.xml_data, '/producte/imatges/imatge')
            )) t
        """)
        for row in cursor:
            pro_id = row.producte_id
            format =  row.format_imatge
            titol = row.descripcio_imatge

            id_prducto = pro_id # modificar Como con una array o cua, para poder guardar los id's oara verificar que existe ya y sumar 1

            num_img = 1

            if (pro_id == id_prducto): # if mirar que tenga el mismo nombre entonces 
                num_img # sumar 1
            
            
            db.insert({'producte_id': pro_id, 'num_imatges': num_img, 'formats': format, 'titol': titol})

            # AQUI ponemos el proceso para guardarlo

    except cx_Oracle.Error as e:
        print(f"Error XQuery: {e}")
    finally:
        if cursor:
            cursor.close()
        conn.close()

    #### MODIFICAR  ]

    ##SE SUPONE QUE FUNCIONA
    db = TinyDB('DocumentsXML')
    if (db.get(all) > 0): #Si tiene contenido reescribirlo
        db.remove(all)

    # Bucle que por cada XML guarda los datos en el db.

    # con un cursor por cada 
    pro_id = 101 # valor extraido
    num_img = 3 # valor extraido
    format = 'png' # valor extraido  ['jpg', 'png']
    titol = 'Producte Exemple' #valor extarido

    db.insert({'producte_id': pro_id, 'num_imatges': num_img, 'formats': format, 'titol': titol})
    ##

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



#####
db = TinyDB('datos.json')

#Limpieza para no generar todo el rato los valores cuando iniciar el programa
db.remove(all)

db.insert({'nombre': 'Laura', 'edad': 28})
db.insert_multiple([
    {'nombre': 'Pedro', 'edad': 32},
    {'nombre': 'Ana', 'edad': 22}
])

# Leer todos los documentos
#print("Todos los documentos")

#print(db.all(),"\n")

#print("Consulta con filtro de edad > 25")

# Consultar con filtros simples
from tinydb import Query

Persona = Query()
resultado = db.search(Persona.edad > 25)
#print(resultado, "\n")


#Consultas con varios criterios (AND/OR)
#print("Consultas con varios criterios (AND/OR)")
#print("AND")
resultado = db.search((Persona.edad > 25) & (Persona.nombre == 'Pedro'))
#print(resultado, "\n")

#print("OR")
resultado = db.search((Persona.nombre == 'Pedro') | (Persona.nombre == 'Ana'))
#print(resultado, "\n")

# Consultas sobre subdocumentos
#print("Subdocumentos (ciudad)")

db.insert({
    'nombre': 'Carlos',
    'direccion': {
        'ciudad': 'Madrid',
        'codigo_postal': 28001
    }
})
resultado = db.search(Persona.direccion.test(lambda d: d['ciudad'] == 'Madrid'))
#print(resultado)


# Actualizar documentos
db.update({'edad': 29}, Persona.nombre == 'Laura')
#print(db.all(), "\n")

# Actualizaciones parciales con funciones
db.update(lambda d: d.update({'edad': d['edad'] + 1}), Persona.nombre == 'Pedro')
#print(db.all(), "\n")

# Eliminar documentos
db.remove(Persona.nombre == 'Ana')
#print(db.all(), "\n")

# Uso de tablas (simular colecciones)
usuarios = db.table('usuarios')
usuarios.insert({'nombre': 'Lucía'})

pedidos = db.table('pedidos')
pedidos.insert({'producto': 'Libro', 'precio': 12.99})

#print("Users: ", usuarios.all())

#print("Pedidos: ", pedidos.all())

## Ejercicios
#Ejercicio 1: Registro y consulta básica
#Objetivo: crear una base de datos de estudiantes y buscar por edad.
#Requisitos:
#Crear una base de datos llamada estudiantes.json.
#Insertar al menos 3 estudiantes con nombre, edad y curso.
#Buscar todos los estudiantes mayores de 20 años.
from tinydb import TinyDB

tiny = TinyDB('estudiantes.json')
tiny.remove(all) #Para ejecutar varias veces y no tener valores repetidos

tiny.insert_multiple([
    {'nombre': 'Pedro', 'edad': 32, "curso" : 2},
    {'nombre': 'Ana', 'edad': 22, "curso" : 1},
    {'nombre': 'Juan', 'edad': 19, "curso" : 1}
])

Estudiate = Query()
salida = tiny.search(Estudiate.edad > 20)
print(salida)


#Ejercicio 2: Subdocumentos y actualización
#Objetivo: trabajar con subdocumentos (anidamiento) y actualizar campos.
#Requisitos:
#Cada estudiante tendrá una dirección (ciudad, código_postal) como subdocumento.
#Actualizar la ciudad de un estudiante.

tiny.update({'direccion': {
        'ciudad': 'Madrid',
        'codigo_postal': 28001
    }}, Persona.nombre == 'Pedro')
tiny.update({'direccion': {
        'ciudad': 'Barcelona',
        'codigo_postal': 18025 
    }}, Persona.nombre == 'Juan')
tiny.update({'direccion': {
        'ciudad': 'Alacant',
        'codigo_postal': 13001
    }}, Persona.nombre == 'Ana')

print(tiny.all())


#Ejercicio 3: Simulación de sistema de pedidos
#Objetivo: simular dos colecciones con relación por ID.
#Requisitos:
#Crear una tabla de clientes y otra de pedidos.
#Relacionar clientes con pedidos por un campo id_cliente.
#Mostrar todos los pedidos de un cliente por su nombre.
clientes = tiny.table('usuarios')
clientes.insert({'id_cliente ':1, 'nombre': 'Lucía'})

pedidos = tiny.table('pedidos')
pedidos.insert({'id_cliente': 1,'producto': 'Libro', 'precio': 12.99})
pedidos.insert({'id_cliente': 1,'producto': 'Manga', 'precio': 8.50})

Pedido = Query()
resultado = pedidos.search((Pedido.id_cliente == 0))
print("\nTodos los pedidos de un cliente por su nombre")
print(resultado)

clientes.remove(all) 
pedidos.remove(all)