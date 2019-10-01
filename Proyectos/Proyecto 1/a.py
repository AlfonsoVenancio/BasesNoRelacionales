import pymongo
import json
import yaml
import datetime

config = yaml.load(open("config.yaml",'r'),Loader=yaml.Loader)

def init_conexion():
    cliente = pymongo.MongoClient(config['Mongo']['Direccion'])
    base = cliente[config['Mongo']['Base']]
    coleccionAcciones = base[config['Mongo']['ColeccionAcciones']]
    coleccionDividendos = base[config['Mongo']['ColeccionDividendos']]
    return {"Cliente":cliente, "Base": base, "Acciones":coleccionAcciones, "Dividendos": coleccionDividendos}

def inserta_documentos(nombre_coleccion, path_documentos):
    conexion = init_conexion()
    documentos = open(path_documentos,'r').read().split("\n")
    coleccion = conexion[nombre_coleccion]
    for documentoJSON in documentos:
        documento = json.loads(documentoJSON)
        documento["Fecha"] = datetime.datetime.strptime(documento["Fecha"],"%Y-%M-%d")
        coleccion.insert_one(documento)
    print(len(documentos),"insertados a la coleccion",coleccion)

def consulta_general(nombre_coleccion, parametros_filtrado, parametros_impresion, sort_field = None, descending = False):
    conexion = init_conexion()
    coleccion = conexion[nombre_coleccion]
    result = coleccion.find(parametros_filtrado, parametros_impresion)
    if sort_field is not None:
        return result.sort(sort_field, -1 if descending else 1)
    return result

def precio_promedio_accion(id_accion, inicio_periodo, fin_periodo):
    acumulado = 0.0
    dias = 0
    fecha_inicio = datetime.datetime.strptime(inicio_periodo, "%Y-%M-%d")
    fecha_fin = datetime.datetime.strptime(fin_periodo, "%Y-%M-%d")
    filtrado = {"Id" : id_accion, "Fecha":{"$gte":fecha_inicio, "$lt":fecha_fin}}
    impresion = {"_id":0, "CostoAccion" : 1, "Fecha" : 1 }
    documentos = consulta_general("Acciones", filtrado, impresion)
    for documento in documentos:
        acumulado += documento["CostoAccion"]
        dias += 1
    return acumulado/dias

def precio_max_accion(id_accion, inicio_periodo, fin_periodo): 
    fecha_inicio = datetime.datetime.strptime(inicio_periodo, "%Y-%M-%d")
    fecha_fin = datetime.datetime.strptime(fin_periodo, "%Y-%M-%d")
    filtrado = {"Id" : id_accion, "Fecha":{"$gte":fecha_inicio, "$lt":fecha_fin}}
    impresion = {"_id":0, "CostoAccion" : 1, "Fecha" : 1 }
    documentos = consulta_general("Acciones", filtrado, impresion, "CostoAccion", True)
    return documentos.next()["CostoAccion"]

def precio_min_accion(id_accion, inicio_periodo, fin_periodo): 
    fecha_inicio = datetime.datetime.strptime(inicio_periodo, "%Y-%M-%d")
    fecha_fin = datetime.datetime.strptime(fin_periodo, "%Y-%M-%d")
    filtrado = {"Id" : id_accion, "Fecha":{"$gte":fecha_inicio, "$lt":fecha_fin}}
    impresion = {"_id":0, "CostoAccion" : 1, "Fecha" : 1 }
    documentos = consulta_general("Acciones", filtrado, impresion, "CostoAccion")
    return documentos.next()["CostoAccion"]

#inserta_documentos("Acciones", "acciones.jsonl")
#inserta_documentos("Dividendos","dividendos.jsonl")

print(precio_promedio_accion("PEME1","2015-01-01","2016-01-01"))
print(precio_max_accion("PEME1","2015-01-01","2016-01-01"))
print(precio_min_accion("PEME1","2015-01-01","2016-01-01"))