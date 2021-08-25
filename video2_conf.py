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

# Ejercicio, modifica los scripts de capabilities y config para conectarte a tu propio router
# Si no cuentas con equipo a la mano puedes usar alguno de los sandbox "Always on" de cisco
# Al momento de hacer el video este es el link: https://developer.cisco.com/site/sandbox/
# Si cambio seguramente puedes encontrarlo en buscando en google cisco devnet sandbox