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

def get_options():

    menu=True
    
    while menu:
        device_id = input('''
1) ISR 4331
2) Catalyst 8000v
Selecciona el equipo al que te quieras conectar: ''')

        config_id = input('''
1) Hostname
2) Usuarios
3) Rutas
4) Interfaz Loopback 10
Selecciona la configuracion que quieres obtener: ''')

        if device_id in ['1','2'] and config_id in ['1','2','3','4']:
            menu = False
        else:
            print('Opcion incorrecta, usa los numeros disponibles para seleccionar equipo y configuracion')

    return device_id,config_id   

# Llamamos nuestras funciones

if __name__ == '__main__':

    # Diccionario de filtros MI FAVORITO!
    dicc_filtros = {
        '1': f.hostname,
        '2': f.usernames,
        '3': f.routes,
        '4': f.loopback10
    }

    dicc_equipos = {
        '1': d.lab_4331,
        '2': d.lab_c8000v  
    }

    device_id,config_id = get_options()

    # Obtenemos el equipo y filtro de los diccionarios
    device = dicc_equipos[device_id]
    netconf_filter = dicc_filtros[config_id]

    # Usamos la funcion get_filtered_config (NETCONF)
    print('Obteniendo configuracion solicitada ...')
    xml_config = get_filtered_config(device,netconf_filter)

    # Convertimos la respuesta XML a JSON
    config = convert_xml_json(xml_config)

    # Formateamos los datos, desde JSON es muy facil
    response = config_format(config,config_id)

    # Se imprimen los resultados en la terminal
    print('')
    [print(line) for line in response]
