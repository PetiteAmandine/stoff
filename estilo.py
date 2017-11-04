import pandas as pd
import numpy as np
import requests
import re

#Funciones y variables globales


#Elimina formato innecesario, separa por párrafos y los almacena en un DataFrame
def divide_parrafos(texto):
    return pd.DataFrame({'parrafo':[x.replace('\r\n', ' ') for x in texto.split('\r\n\r\n')]})

#Obtiene el número de palabras en un párrafo
def lon_parrafo(parrafo):
    return len(parrafo.split())

#Obtiene la longitud promedio de cada una de las palabras de un párrafo.
#NaN son párrafos vacíos
def lon_palabra(parrafo):
    return np.mean([len(x) for x in parrafo.split()])

#Calcula el promedio de palabras por cada oración en un párrafo
#NaN son párrafos vacíos
def lon_prom_oracion(parrafo):
    oracion = re.split('\!|\.|\?', parrafo)
    lista_aux = [len(re.findall(r"['\w']+", x)) for x in oracion]
    lista_fin = []
    for i in lista_aux:
        if i!=0:
            lista_fin.append(i)
    return np.mean(lista_fin)
    
#Encuentra el número de signos de puntuación en un párrafo
def total_punt(parrafo):
    lista_fin = []
    for i in re.findall('\W', parrafo):
        if i != ' ':
            lista_fin.append(i)
    return len(lista_fin)

lista_variables = [lon_parrafo, lon_palabra, lon_prom_oracion, total_punt]

#Obtiene el texto de un link, le da estructura y le aplica las funciones anteriores
def estructura_texto(link):
    texto = requests.get(link).text
    clean = divide_parrafos(texto)
    clean = clean.parrafo.apply(lista_variables)
    return clean[clean.lon_prom_oracion.notnull()]