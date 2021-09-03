from ncclient import manager,xml_
import devices as d

def get_config_filter(device,new_config):
    
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

new_hostname = input('Escribe el nuevo hostname: ')

hostname_config = f'''
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <hostname>{new_hostname}</hostname>
    </native>
</config>
'''

print(hostname_config)

netconf_reply = get_config_filter(d.lab_c8000v,hostname_config)
print(netconf_reply)