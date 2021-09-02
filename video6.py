from ncclient import manager
import devices as d
import filters as f

def apply_config(device,new_config):

    with manager.connect(
        host=device['address'],
        port=device['port'],
        username=device['username'],
        password=device['password'],
        hostkey_verify=False) as m:

        if device['commit']:
            netconf_reply = m.edit_config(config=new_config, target="candidate")
            m.commit()
        else:
            netconf_reply = m.edit_config(config=new_config, target="running")
            netconf_save = '<cisco-ia:save-config xmlns:cisco-ia="http://cisco.com/yang/cisco-ia"/>'
            m.dispatch(netconf_save)
        
        return netconf_reply

hostname_config = '''
<config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <hostname>NEW_HOSTNAME</hostname>
    </native>
</config>
'''

new_hostname = input('Escribe el nuevo hostname: ')

new_config = hostname_config.replace('NEW_HOSTNAME',new_hostname)
print(new_config)

netconf_reply = apply_config(d.lab_4331,new_config)
print(netconf_reply)
