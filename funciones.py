from ncclient import manager,xml_
import xmltodict
import json
import devices as d
import filters as f
from ncclient.operations import RPCError

def get_filtered_config(device,netconf_filter):

    with manager.connect(host=device['address'], 
                            port=device['port'],
                            username=device['username'],
                            password=device['password'],
                            hostkey_verify=False) as m:

        
        if float(device['version']) >= 17.3:
            filtered_config = m.get_config('running',filter=('subtree',netconf_filter)).xml

        else:
            updated_filter = '<filter>' + netconf_filter + '</filter>'
            filtered_config = m.get_config('running',updated_filter).xml
    
    return filtered_config


def xml_to_json(xml_data):

    od_data = xmltodict.parse(xml_data)
    json_data = json.loads(json.dumps(od_data))
    config = json_data['rpc-reply']['data']['native']

    return config


def get_options_menu():

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


def get_device_filter(device_id,filter_id):
    
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

    device = dicc_equipos[device_id]
    netconf_filter = dicc_filtros[filter_id]

    return device,netconf_filter


def config_format(config,config_id):

    f_config = list()

    if config_id == '1':
        h_response = f'Hostname: {config["hostname"]}\n'
        f_config.append(h_response)

    elif config_id == '2':

        if type(config["username"]) == list:
            list_config = config["username"]
        else:
            list_config = [config["username"]]
        for user in list_config:
            n = user["name"]
            p = user["privilege"]
            s = user["secret"]["secret"]
            c = user["secret"]["encryption"]
            u_response = f'user: {n}\nprivilegio: {p}\nsecreto: {s}\ncifrado: {c}\n'
            f_config.append(u_response)

    elif config_id == '3':

        if type(config["ip"]["route"]["ip-route-interface-forwarding-list"]) == list:
            list_config = config["ip"]["route"]["ip-route-interface-forwarding-list"]
        else:
            list_config = [config["ip"]["route"]["ip-route-interface-forwarding-list"]]
        for route in list_config:
            p = route["prefix"]
            m = route["mask"]
            n = route["fwd-list"]['fwd']
            r_response = f'Prefijo: {p}\nMascara: {m}\nNext Hop: {n}\n'
            f_config.append(r_response)

    elif config_id == '4':
        name = "Loopback10"
        primary = config["interface"]["Loopback"]["ip"]["address"]["primary"]
        ip = primary["address"]
        mask = primary["mask"]
        l_response =  f'{name}\nIP: {ip}\nMascara: {mask}\n'
        f_config.append(l_response)

    else:
        print('Formato no soportado aun')
        f_config.append(config)

    return f_config
 

def get_config_filter(device,new_config):

    if new_config == None:
        netconf_reply = ('Configuracion no soportada aun ... ADIOS!')

    else:

        with manager.connect(
            host=device['address'],
            port=device['port'],
            username=device['username'],
            password=device['password'],
            hostkey_verify=False) as m:

            if device['commit']:
                netconf_reply = m.edit_config(config=new_config,target='candidate')
                m.commit()
            else:
                netconf_reply = m.edit_config(config=new_config,target='running')
                netconf_save = '<cisco-ia:save-config xmlns:cisco-ia="http://cisco.com/yang/cisco-ia"/>'
                m.dispatch(xml_.to_ele(netconf_save))

    return netconf_reply


def buil_config_xml(filter_id):

    if filter_id == '1':

        h = input('Escribe el nuevo hostname: ')

        new_config = f'''
                    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                            <hostname>{h}</hostname>
                        </native>
                    </config>'''


    elif filter_id == '2':

        u = input('Escribe el nuevo usuario: ')
        p = input('Escribe el nuevo privilegio [0-15]: ')
        s = input('Escribe el nuevo secreto [Texto plano]: ')
        
        new_config = f'''
                    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                            <username>
                                <name>{u}</name>
                                <privilege>{p}</privilege>
                                <secret>
                                    <encryption>0</encryption>
                                    <secret>{s}</secret>
                                </secret>
                            </username>
                        </native>
                    </config>'''

    elif filter_id == '3':

        p = input('Escribe el nuevo prefijo [ex. 192.168.1.0]: ')
        m = input('Escribe la nueva mascara [ex. 255.255.255.252]: ')
        n = input('Escribe el nuevo next hop [ex. 10.1.1.1]: ')

        new_config = f'''
                    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                            <ip>
                                <route>
                                    <ip-route-interface-forwarding-list>
                                        <prefix>{p}</prefix>
                                        <mask>{m}</mask>
                                        <fwd-list>
                                            <fwd>{n}</fwd>
                                        </fwd-list>
                                    </ip-route-interface-forwarding-list>
                                </route>
                            </ip>
                        </native>
                    </config>'''


    elif filter_id == '4':
        
        i = input('Escribe la nueva ip de Loopback 10 [ex. 192.168.1.1]: ')
        m = input('Escribe la nueva mascara [ex. 255.255.255.0]: ')

        new_config = f'''
                    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                        <native	xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                            <interface>
                                <Loopback>
                                    <name>10</name>
                                    <ip>
                                        <address>
                                            <primary>
                                                <address>{i}</address>
                                                <mask>{m}</mask>
                                            </primary>
                                        </address>
                                    </ip>
                                </Loopback>
                            </interface>
                        </native>
                    </config>'''
        
    else:
        new_config = None

    return new_config

def send_config(device,new_config):

    try:

        get_config_filter(device,new_config)
        response = ('Configuracion aplicada')

    except RPCError as error:

        response = ('Problemas con la configuracion\nError:',error._message)
    
    return response