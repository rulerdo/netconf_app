#!/usr/bin/env python3

"""
Script para demostrar datos en formatos XML, Diccionarios Ordenados y JSON utilizando las librerias xmltodict json y collections.OrderedDict
Author: Raul Gomez
email: raul.agobe@gmail.com
"""

import xmltodict
import json
from collections import OrderedDict

# Datos originales en formato XML que vamos a manipular con los modulos
data_email = '<email><para>Juan</para><de>Raul</de><encabezado>Felicidades!</encabezado><mensaje>Querido Juan, que pases un feliz cumpleaños. Te mando un abrazo.</mensaje></email>'

# Imprimir los datos originales
print('Datos originales:')
print(data_email)

# Convertimos los datos de XML a un Diccionario Ordenado e imprimimos el resultado
dict_email = xmltodict.parse(data_email)
print('Datos convertidos a un diccionario ordenado')
print(dict_email)

# Convertimos los datos de un Diccionario Ordenado a json e imprimimos el resultado
json_email = json.dumps(dict_email)
print('Datos convertidos a json')
print(json_email)

# Convertimos los datos de json a XML e imprimimos el resultado
xml_email = data = json.JSONDecoder(object_pairs_hook=OrderedDict).decode(json_email)
print('Datos de vuelta a formato XML')
print(data_email)


# Ejercicio: Modifica el codigo y convierte el XML de frutas a diccionario, json y de vuelta a XML, imprime los resultados

data_frutas = '''
<frutas>
    <manzana>
        <color>roja</color>
        <sabor>delicioso</sabor>
    </manzana>
    <platano>
        <color>amarillo</color>
        <sabor>neutro</sabor>
    </platano>
    <melon>
        <color>naranja</color>
        <sabor>dulce</sabor>
    </melon>
    <limon>
        <color>verde</color>
        <sabor>amargo</sabor>
    </limon>
</frutas>
'''