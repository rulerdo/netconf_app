#!/usr/bin/env python3

"""
Script para mostrar como obtener la running config de los equipos de laboratorio usando filtros
Autor: Raul Gomez
email: raul.agobe@gmail.com
"""

from ncclient import manager
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
            filtered_config = m.get_config('running',filter=('subtree',netconf_filter))

        else:
            updated_filter = '<filter>' + netconf_filter + '</filter>'
            filtered_config = m.get_config('running',updated_filter)
    
    return filtered_config

# Llamamos a la funcion get_running_config e imprimimos el resultado en la terminal

if __name__ == '__main__':

    config = get_filtered_config(d.lab_4331,f.usernames)

    print('Aqui la configuracion: ')
    print(config)
