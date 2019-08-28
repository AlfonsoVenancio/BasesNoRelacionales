def multiplicar_matrices(A, B):
    m = len(A)
    # Verificacion de las dimensiones de las matrices A(m,n) y B(n,p) para que puedan ser multiplicadas
    if len(A[0]) != len(B):
        raise Exception("Las matrices no tienen las dimensiones necesarias para ser multiplicadas")
    n = len(A[0])
    p = len(B[0])
    matriz_resultado = []
    for i in range(m):
        matriz_resultado.append([])
        for k in range(p):
            # Para cada fila de A, generar la listas con los valores en las columnas de B y multiplicarlos elemento por elemento
            # Sumar todos los elementos de la lista resultante y guardarlos en el resultado
            resultado = sum([a*b for a, b in zip(A[i], [B[j][k] for j in range(n)])])
            matriz_resultado[i].append(resultado)
    return matriz_resultado


def sumar_polinomios(path_archivo):
    # Se lee el archivo, primero se separa por lineas y despues por espacios entre los numeros
    polinomios = open(path_archivo, 'r').read().split("\n")
    # Para poderlos ocupar como numeros, hacemos map y despues a lista debido a que es Python3
    A = list(map(float, polinomios[0].split(" ")))
    B = list(map(float, polinomios[1].split(" ")))
    diccionario_A = {}
    diccionario_B = {}
    diccionario_resultado = {}
    # Recorremos la lista A de dos en dos, sin offset para los coeficientes y con un offset de 1 para los exponentes
    # Esto para cada una de las listas de numeros
    for coeficiente, exponente in zip(A[::2], A[1::2]):
        if not coeficiente == exponente == -1:
            diccionario_A[exponente] = coeficiente
    for coeficiente, exponente in zip(B[::2], B[1::2]):
        if not coeficiente == exponente == -1:
            diccionario_B[exponente] = coeficiente
    # Hacemos una lista conjunta con todos los exponentes de ambos polinomios, set para eliminar repetidos
    exponentes = list(set(A[1:-2:2] + B[1:-2:2]))
    for exponente in exponentes:
        # Si la suma de coeficientes es diferente de 0, guardarlo
        if diccionario_A.get(exponente, 0) + diccionario_B.get(exponente, 0) != 0.0:
            diccionario_resultado[exponente] = diccionario_A.get(exponente, 0) + diccionario_B.get(exponente, 0)
    return diccionario_resultado


def multiplicar_polinomios(path_archivo):
    # Se lee el archivo, primero se separa por lineas y despues por espacios entre los numeros
    polinomios = open(path_archivo, 'r').read().split("\n")
    # Para poderlos ocupar como numeros, hacemos map y despues a lista debido a que es Python3
    A = list(map(float, polinomios[0].split(" ")))
    B = list(map(float, polinomios[1].split(" ")))
    diccionario_resultado = {}
    # Recorremos la lista A de dos en dos, sin offset para los coeficientes y con un offset de 1 para los exponentes
    for coeficiente_A, exponente_A in zip(A[:-2:2], A[1:-2:2]):
        for coeficiente_B, exponente_B in zip(B[:-2:2], B[1:-2:2]):
            # Multiplicamos coeficientes y sumamos exponentes
            diccionario_resultado[exponente_A + exponente_B] = diccionario_resultado.get(exponente_A + exponente_B, 0) + coeficiente_A * coeficiente_B
    return diccionario_resultado


def formatear_polinomios(diccionario):
    # Formato +-cX^e
    # Se ordenan los exponentes del diccionario de forma descentente
    # Para cada uno de los eponentes, si el coeficiente correspondiente es positivo
    # Añadir a la lista el miembro del polinomio con un "+" al inicio, en caso contrario el coeficiente ya incluirá el "-" correspondiente
    return ''.join("+"+str(diccionario[exponente])+"X^"+str(int(exponente))+" " if diccionario[exponente] > 0 else str(diccionario[exponente])+"X^"+str(int(exponente))+" " for exponente in sorted(diccionario.keys(), reverse = True))


def encontrar_substrings(A, B):
    contador = 0
    inicio_busqueda = 0
    # Hasta que no se encuentre otra ocurencia de B en A
    while True:
        indice = A.find(B, inicio_busqueda)
        # Ya no se encontro B en A
        if indice == -1:
            return contador
        contador += 1
        # Nos movemos un caracter despues de donde se encontro la ocurrencia para encontrar sobrelapados
        inicio_busqueda = indice + 1


def contar_palabras(path_archivo):
    # Se lee el archivo como una linea y se separa por espacios
    texto = open(path_archivo, 'r').read().replace("\n", " ").split(" ")
    resultado = {}
    for palabra in texto:
        # Acumulador
        resultado[palabra] = resultado.get(palabra, 0) + 1
    # Se devuelve la cubeta contadora de palabras y el numero de elementos que contiene
    return (resultado, len(resultado.keys()))


def contar_valores(coleccion):
    contador = 0
    # Se unifica el valor en el que se va a buscar, en caso de una lista es la propia lista
    if isinstance(coleccion, list):
        lista_valores = coleccion
    # En caso de un diccionario, en sus valores
    elif isinstance(coleccion, dict):
        lista_valores = coleccion.values()
    for valor in lista_valores:
        # Si el elemnto es una lista o un diccionario, debemos de hacer una busqueda mas profunda
        if isinstance(valor, list) or isinstance(valor, dict):
            contador += contar_valores(valor)
        # Valores primitivos listos para ser contados
        else:
            contador += 1
    return contador


def rango_lexicografico(path_archivo):
    resultado = []
    # Se leen ambos delimitadores del rango
    izquierda = input("Ingresa el rango delimitador izquierdo del rango:")
    derecha = input("Ingresa el rango delimitador derecho del rango:")
    if len(izquierda) > 7 or len(derecha) > 7:
        raise Exception("El string puede ser de 7 caracteres maximo")
    if izquierda >= derecha:
        raise Exception("Las lineas introducidas no generan un rango lexicografico")
    texto = open(path_archivo, 'r').read().split("\n")
    for linea in texto:
        # Se verifica que los primeros 7 caracteres de cada linea se encuentren en el rango y se guarda la linea
        if izquierda <= linea[:7] <= derecha:
            resultado.append(linea)
    return resultado

print("===== MULTIPLICACION DE MATRICES =====")
matriz_A = [[1, -2, 3], [1, 0, -1], [5, 6, 7]]
matriz_B = [[1, 4], [2, 5], [3, 6]]
print(multiplicar_matrices(matriz_A, matriz_B))

print("===== CONTAR OCURRENCIAS DE SUBSTRING =====")
string_A = "azcbobobegghakl"
string_B = "bob"
print(encontrar_substrings(string_A, string_B))

print("===== CONTAR PALABRAS =====")
print(contar_palabras("texto.txt"))

print("===== CONTAR VALORES EN UN DICCIONARIO =====")
diccionario = {"valor1": matriz_A, "valor2": [1, 2, 3, 4], "valor3": string_A}
print(contar_valores(diccionario))

print("===== LINEAS EN EL RANGO LEXICOGRAFICO =====")
print(rango_lexicografico("texto.txt"))

print("===== SUMA DE POLINOMIOS =====")
print(formatear_polinomios(sumar_polinomios("polinomios.txt")))

print("===== MULTIPLICACION DE POLINOMIOS =====")
print(formatear_polinomios(multiplicar_polinomios("polinomios.txt")))
