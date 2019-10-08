import pymongo
import json
import yaml
import datetime
import matplotlib.pyplot as pyplot

config = yaml.load(open("config.yaml",'r'), Loader=yaml.Loader)

# Se genera la conexión y se regresan los objetos de conexion
def init_conexion():
    cliente = pymongo.MongoClient(config['Mongo']['Direccion'])
    base = cliente[config['Mongo']['Base']]
    coleccionAcciones = base[config['Mongo']['ColeccionAcciones']]
    coleccionDividendos = base[config['Mongo']['ColeccionDividendos']]
    return {"Cliente":cliente, "Base": base, "Acciones":coleccionAcciones, "Dividendos": coleccionDividendos}

# Para cada uno de los documentos en una coleccion, se insertan a una coleccion de mongo
def inserta_documentos(nombre_coleccion, path_documentos):
    conexion = init_conexion()
    documentos = open(path_documentos,'r').read().split("\n")
    coleccion = conexion[nombre_coleccion]
    for documentoJSON in documentos:
        documento = json.loads(documentoJSON)
        # Para tener ISODate en mongo
        documento["Fecha"] = datetime.datetime.strptime(documento["Fecha"],"%Y-%M-%d")
        coleccion.insert_one(documento)
    print(len(documentos),"insertados a la coleccion",nombre_coleccion)

# Manejador general de consulta, se obtienen los diccionarios con los parametros de filtrado y de presentacion
def consulta_general(nombre_coleccion, parametros_filtrado, parametros_impresion, sort_field = None, descending = False):
    conexion = init_conexion()
    coleccion = conexion[nombre_coleccion]
    result = coleccion.find(parametros_filtrado, parametros_impresion)
    # Se ordenan los datos si el parametro sort_field no es nulo, por default ascendente
    if sort_field is not None:
        return result.sort(sort_field, -1 if descending else 1)
    return result

# Precio promedio de una accion en un periodo
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

# Precio maximo de una accion en un periodo
def precio_max_accion(id_accion, inicio_periodo, fin_periodo): 
    fecha_inicio = datetime.datetime.strptime(inicio_periodo, "%Y-%M-%d")
    fecha_fin = datetime.datetime.strptime(fin_periodo, "%Y-%M-%d")
    filtrado = {"Id" : id_accion, "Fecha":{"$gte":fecha_inicio, "$lt":fecha_fin}}
    impresion = {"_id":0, "CostoAccion" : 1, "Fecha" : 1 }
    # Se ordena descendente con el CostoAccion y se devuelve el primer dato
    documentos = consulta_general("Acciones", filtrado, impresion, "CostoAccion", True)
    return documentos.next()["CostoAccion"]

# Precio minimo de una accion en un periodo
def precio_min_accion(id_accion, inicio_periodo, fin_periodo): 
    fecha_inicio = datetime.datetime.strptime(inicio_periodo, "%Y-%M-%d")
    fecha_fin = datetime.datetime.strptime(fin_periodo, "%Y-%M-%d")
    filtrado = {"Id" : id_accion, "Fecha":{"$gte":fecha_inicio, "$lt":fecha_fin}}
    impresion = {"_id":0, "CostoAccion" : 1, "Fecha" : 1 }
    # Se ordena ascendente con el CostoAccion y se devuelve el primer dato
    documentos = consulta_general("Acciones", filtrado, impresion, "CostoAccion")
    return documentos.next()["CostoAccion"]

# Accion con mayor costo en una empresa en un dia en especifico
def mejor_accion_empresa(nombre_empresa, fecha):
    fecha_accion = datetime.datetime.strptime(fecha, "%Y-%M-%d")
    filtrado = {"Empresa" : nombre_empresa, "Fecha":fecha_accion}
    impresion = {"_id":0}
    # Se ordenan las acciones de la empresa en ese dia, descendente y se devuelve el primer dato
    documentos = consulta_general("Acciones", filtrado, impresion, "CostoAccion", True)
    return documentos.next()

# El pago total de dividendos de una accion en un periodo
def pago_total_dividendo(id_accion, inicio_periodo, fin_periodo):
    acumulado = 0.0
    fecha_inicio = datetime.datetime.strptime(inicio_periodo, "%Y-%M-%d")
    fecha_fin = datetime.datetime.strptime(fin_periodo, "%Y-%M-%d")
    filtrado = {"Id" : id_accion, "Fecha":{"$gte":fecha_inicio, "$lt":fecha_fin}}
    impresion = {"_id":0, "Pago" : 1}
    documentos = consulta_general("Dividendos", filtrado, impresion)
    for documento in documentos:
        acumulado += documento["Pago"]
    return acumulado

# Para cada uno de los documentos en una lista de JSON, se agrupan dependiendo de un parametro
def prepara_documentos(documentos, llave_agrupamiento):
    diccionario = {}
    for documento in documentos:
        valor_llave = documento[llave_agrupamiento]
        if valor_llave not in diccionario:
            diccionario[valor_llave] = {}
        # Para cada uno de los valores en ese documento, agrupar y guardar los datos en el diccionario
        for llave, valor in documento.items():
            # No queremos guardar el valor de la llave de agrupamiento, pues esa es la llave de este diccionario
            if llave != llave_agrupamiento:
                if llave not in diccionario[valor_llave]:
                    diccionario[valor_llave][llave] = []
                else:
                    # Se le agrega el valor a la lista
                    diccionario[valor_llave][llave].append(valor)
    return diccionario

# Grafica del costo de todas las acciones en todo el periodo registrado
def grafica_costo_acciones():
    filtrado = {}
    impresion = {"_id": 0, "Id": 1, "CostoAccion": 1}
    documentos = consulta_general("Acciones", filtrado, impresion)
    diccionario_valores = prepara_documentos(documentos, "Id")
    pyplot.figure()
    pyplot.title("Costo de la accion")
    pyplot.xlabel("Días")
    pyplot.ylabel("Costo de la acción")
    for accion, valores_accion in diccionario_valores.items():
        for valores in valores_accion.values():
            # Para cada una de las acciones se obtiene la lista de sus valores diarios
            pyplot.plot(valores, label = accion)
    pyplot.legend()
    pyplot.show()

# Grafica del costo de una accion en un periodo dado
def grafica_costo_accion(id_accion, inicio_periodo, fin_periodo):
    fecha_inicio = datetime.datetime.strptime(inicio_periodo, "%Y-%M-%d")
    fecha_fin = datetime.datetime.strptime(fin_periodo, "%Y-%M-%d")
    filtrado = {"Id": id_accion, "Fecha":{"$gte":fecha_inicio, "$lt":fecha_fin}}
    impresion = {"_id": 0, "Id": 1, "CostoAccion": 1}
    documentos = consulta_general("Acciones", filtrado, impresion)
    # Se agrupan los valores por el Id de cada una de las acciones
    diccionario_valores = prepara_documentos(documentos, "Id")
    pyplot.figure()
    pyplot.title("Costo de la accion")
    pyplot.xlabel("Días")
    pyplot.ylabel("Costo de la acción")
    for accion, valores_accion in diccionario_valores.items():
        for valores in valores_accion.values():
            # Se accede a la lista de los costos de la accion y se grafica
            pyplot.plot(valores, label = accion)
    pyplot.legend()
    pyplot.show()

# Grafica del total del pago de dividendos de varias acciones en un periodo
def grafica_pago_dividendos(ids_acciones, inicio_periodo, fin_periodo):
    pagos = []
    # Para cada una de las acciones en id_acciones, se obtiene su pago total de dividendos en ese periodo
    for id_accion in ids_acciones:
        pagos.append(pago_total_dividendo(id_accion, inicio_periodo, fin_periodo))
    pyplot.figure()
    pyplot.title("Pago total de dividendos")
    pyplot.xlabel("Acciones")
    pyplot.ylabel("Pago total de dividendos en el periodo")
    # Se grafican los pagos de dividendos de cada accion, con el id_accion como etiqueta de la barra
    pyplot.bar(ids_acciones, pagos)
    pyplot.show()


#inserta_documentos("Acciones", "acciones.jsonl")
#inserta_documentos("Dividendos","dividendos.jsonl")

print(precio_promedio_accion("PEME1","2015-01-01","2016-01-01"))
print(precio_max_accion("PEME1","2015-01-01","2016-01-01"))
print(precio_min_accion("PEME1","2015-01-01","2016-01-01"))
print(mejor_accion_empresa("PEMEX","2016-05-20"))
print(pago_total_dividendo("PEME1","2015-01-01","2016-01-01"))
grafica_costo_acciones()
grafica_costo_accion("PEME1","2015-01-01","2016-01-01")
grafica_pago_dividendos(["PEME1", "PEME5"],"2015-01-01","2016-01-01")