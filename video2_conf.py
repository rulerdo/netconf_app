#!/usr/bin/env python3

"""
Script para mostrar como obtener la running config de los equipos de laboratorio
Autor: Raul Gomez
email: raul.agobe@gmail.com
"""

from ncclient import manager
import devices as d

# Funcion para conectarse via NETCONF a un equipo de red y obtener la running config

def get_running_config(device):

    with manager.connect(host=device['address'], 
                            port=device['port'],
                            username=device['username'],
                            password=device['password'],
                            hostkey_verify=False) as m:

        running_config = m.get_config('running')
    
    return running_config

# Llamamos a la funcion get_running_config e imprimimos el resultado en la terminal

if __name__ == '__main__':

    device = d.lab_4331

    config = get_running_config(device)

    print('Aqui la configuracion: ')
    print(config)
    print('')
