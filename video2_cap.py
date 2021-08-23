#!/usr/bin/env python3

"""
Script para mostrar como obtener las capabilities de NETCONF en los equipos del laboratorio
Autor: Raul Gomez
email: raul.agobe@gmail.com
"""

from ncclient import manager
import devices as d


# Funcion para conectarse via NETCONF a un equipo de red y obtener los capabilities

def get_capabilities(device):

    with manager.connect(host=device['address'], 
                            port=device['port'],
                            username=device['username'],
                            password=device['password'],
                            hostkey_verify=False) as m:

        cap = m.server_capabilities
    
    return cap

# Llamamos a la funcion get_capabilities e imprimimos el resultado en la terminal

if __name__ == '__main__':

    device = d.lab_4331

    cap = get_capabilities(device)

    print('Aqui los capabilities: ')
    for line in cap:
        print(line)
    print('')
    