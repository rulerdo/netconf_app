from ncclient import manager,xml_
from ncclient.operations import RPCError
import devices as d


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

        h_config = f'''
                    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                            <hostname>{h}</hostname>
                        </native>
                    </config>'''

        new_config = h_config

    elif filter_id == '2':

        u = input('Escribe el nuevo usuario: ')
        p = input('Escribe el nuevo privilegio [0-15]: ')
        s = input('Escribe el nuevo secreto [Texto plano]: ')
        
        u_config = f'''
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

        new_config = u_config

    elif filter_id == '3':

        p = input('Escribe el nuevo prefijo [ex. 192.168.1.0]: ')
        m = input('Escribe la nueva mascara [ex. 255.255.255.252]: ')
        n = input('Escribe el nuevo next hop [ex. 10.1.1.1]: ')

        r_config = f'''
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

        new_config = r_config

    elif filter_id == '4':
        
        i = input('Escribe la nueva ip de Loopback 10 [ex. 192.168.1.1]: ')
        m = input('Escribe la nueva mascara [ex. 255.255.255.0]: ')

        l_config = f'''
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

        new_config = l_config
        
    else:
        new_config = None

    return new_config


new_config = buil_config_xml('3')

try:
    get_config_filter(d.lab_c8000v,new_config)
    print('OK')
except RPCError as error:
    print('Problemas con la configuracion')
    print('Error:',error._message)
