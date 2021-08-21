#!/usr/bin/env python3

"""
Script para mostrar los formatos de datos XML, Diccionarios Ordenados y JSON utilizando las librerias xmltodict y json
Autor: Raul Gomez
email: raul.agobe@gmail.com
"""

import xmltodict
import json

# Datos originales en formato XML que vamos a manipular con los modulos
data_email = '<email><para>Brenda</para><de>Raul</de><titulo>Felicidades!</titulo><mensaje>Feliz cumple querida Brenda</mensaje></email>'

# Imprimir los datos originales
print('Datos originales:')
print(data_email)
print('')

# Convertimos los datos de XML a un Diccionario Ordenado e imprimimos el resultado
odict_email = xmltodict.parse(data_email)
print('Datos convertidos a un diccionario ordenado:')
print(odict_email)
print('')

# Convertimos los datos de un Diccionario Ordenado a json e imprimimos el resultado
json_email = json.loads(json.dumps(odict_email))
print('Datos convertidos a json:')
print(json_email)
print('')

# Usamos el archivo json para imprimir los datos con formato
print('Datos del email con formato:')
for key,value in json_email['email'].items():
    print(key + ': ' + value)
print('')

# Finalmente convertimos el json a XML para volver a los datos originales
xml_email = xmltodict.unparse(json_email)
print('Datos de vuelta a formato XML:')
print(xml_email)
print('')

# Ejercicio: Utiliza el codigo como ejemplo y convierte el XML de frutas a diccionario, json y de vuelta a XML, imprime los resultados

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
