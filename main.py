import funciones as fn

device_id,filter_id = fn.get_options_menu()
device,netconf_filter = fn.get_device_filter(device_id,filter_id)

print('Obteniendo configuracion solicitada ...')
xml_config = fn.get_filtered_config(device,netconf_filter)

config = fn.xml_to_json(xml_config)

f_config = fn.config_format(config,filter_id)

print('')
[print(line) for line in f_config]

configure = input('Escribe "SI" si deseas modificar la configuracion: ')

if configure == 'SI':

    new_config = fn.buil_config_xml(filter_id)
    response = fn.send_config(device,new_config)

else:
    response = 'ADIOS!'

print(response)