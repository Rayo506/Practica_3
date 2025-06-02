# Practica_3
## Configurar Perfil:
En caso de no poder utilizar el codigo de py de los dos casos modifica las variables para poder haceder a su Base de datos

## Partes
# 1
registro_metadatos.py

Lee imágenes de `multimedia/imgs/` y guarda sus metadatos en `db_img_metadades.json`.
# 2
consultes_filtres.py
Hace consultas sobre los metadatos de imágenes y exporta resultados a un JSON.
# 3
migracion_parcial.py
Lee XML desde Oracle y los guarda en TinyDB (`DocumentsXML`). Solo si tienes Oracle.
# 4
menu.py
Menú interactivo para gestionar productos desde los XML de `xml_samples/`.

## Ejemplo de XML de producto
<producte>
  <producte_id>101</producte_id>
  <titol>Producte Exemple</titol>
  <imatges>
      <imatge format="jpg"/>
      <imatge format="png"/>
  </imatges>
</producte>