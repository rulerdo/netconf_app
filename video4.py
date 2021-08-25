#!/usr/bin/env python3

"""
Script para mostrar como obtener la running config de los equipos de laboratorio usando filtros
Autor: Raul Gomez
email: raul.agobe@gmail.com
"""

from ncclient import manager
import xmltodict
import json
import devices as d
import filters as f
from pprint import pprint

# Funcion para conectarse via NETCONF a un equipo de red y obtener la running config usando filtros

def get_filtered_config(device,netconf_filter):

    with manager.connect(host=device['address'], 
                            port=device['port'],
                            username=device['username'],
                            password=device['password'],
                            hostkey_verify=False) as m:

        # Usamos la llave version para decidir el uso del filtro dentro de get_config
        
        if float(device['version']) >= 17.3:
            filtered_config = m.get_config('running',filter=('subtree',netconf_filter)).xml

        else:
            updated_filter = '<filter>' + netconf_filter + '</filter>'
            filtered_config = m.get_config('running',updated_filter).xml
    
    return filtered_config

# Funcion para convertir un dato XML a JSON

def convert_xml_json(xml_data):

    # Convertir XML a diccionario ordenado
    od_data = xmltodict.parse(xml_data)

    # Convertir diccionario ordenado a JSON
    json_data = json.loads(json.dumps(od_data))

    # Obtener los datos dentro de las llaves rpc-reply > data > native

    config = json_data['rpc-reply']['data']['native']

    return config

#Funcion para imprimir los datos obtenidos via netconf, el formato cambia dependiendo de la opcion de configuracion

def config_format(config,config_id):

    response = list()

    if config_id == '1':
        h_response = f'Hostname: {config["hostname"]}\n'
        response.append(h_response)

    elif config_id == '2':

        if type(config["username"]) == list:
            list_config = config
        else:
            list_config = [config]
        for user in list_config["username"]:
            name = user["name"]
            priv = user["privilege"]
            secret = user["secret"]["secret"]
            encryption = user["secret"]["encryption"]
            u_response = f'user: {name}\nprivilegio: {priv}\nencripcion: {encryption}\nsecreto: {secret}\n'
            response.append(u_response)

    elif config_id == '3':

        if type(config["ip"]["route"]["ip-route-interface-forwarding-list"]) == list:
            list_config = config
        else:
            list_config = [config]
        for route in config["ip"]["route"]["ip-route-interface-forwarding-list"]:
            prefix = route["prefix"]
            mask = route["mask"]
            next_hop = route["fwd-list"]['fwd']
            r_response = f'Prefijo: {prefix}\nMascara: {mask}\nNext Hop: {next_hop}\n'
            response.append(r_response)

    elif config_id == '4':
        name = "Loopback10"
        primary = config["interface"]["Loopback"]["ip"]["address"]["primary"]
        ip = primary["address"]
        mask = primary["mask"]
        l_response =  f'{name}\nIP: {ip}\nMascara: {mask}\n'
        response.append(l_response)

    else:
        response.append('Filtro sin soporte')

    return response

# Llamamos nuestras funciones

if __name__ == '__main__':

    # Diccionario de filtros MI FAVORITO!
    dicc_filtros = {
        '1': f.hostname,
        '2': f.usernames,
        '3': f.routes,
        '4': f.loopback10
    }

    # Usamos FOR anidados para imprimir todas las opciones
    for equipo in (d.lab_4331,d.lab_c8000v):

        for config_id,filtro in dicc_filtros.items():

            # Usamos la funcion get_filtered_config (NETCONF)
            xml_config = get_filtered_config(equipo,filtro)

            # Convertimos la respuesta XML a JSON
            config = convert_xml_json(xml_config)

            # Formateamosa los datos, desde JSON es muy facil
            response = config_format(config,config_id)

            # Se imprimen los resultados en la terminal
            [print(line) for line in response]
