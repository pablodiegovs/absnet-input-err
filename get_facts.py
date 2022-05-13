import napalm
import yaml
import getpass
from tabulate import tabulate

def main():
    user = input("Ingrese usuario: ")
    pasw = getpass.getpass(prompt="Ingrese su password: ")
    print("#"*100 + "\n")
    ### Obtener parametros de anillos
    ciudad = input("Seleccione la ciudad donde quiere realizar el analisis (LPZ/SCZ/CBB): ")
    anillo = input("Seleccione el anillo de la red de acceso(ha4/cl1/ijk/test): ")
    print("#"*100 + "\n")
    ### Obtener parametrizacion de sistemas operativos
    driver_ios = napalm.get_network_driver("ios")
    driver_hvrp = napalm.get_network_driver("huawei_vrp")
    ### Crear una lista de dispositivos desde un archivo YAML
    with open('devices/scz-{}-devices.yml'.format(anillo)) as file:
        device_yaml = yaml.load(file, Loader=yaml.FullLoader)
    device_list = device_yaml['devices'].keys()
    ### Establecer parametros de conectividad con los dispositivos dependiendo de su sistema operativo
    network_devices = []
    for device in device_list:
        if device_yaml['devices'][device]['os'] == 'ios':
            network_devices.append(
                            driver_ios(
                                hostname = device_yaml['devices'][device]['connections']['cli']['ip'],
                                username = user,
                                password = pasw
                            )
            )
        elif device_yaml['devices'][device]['os'] == 'huawei_vrp':
            network_devices.append(
                            driver_hvrp(
                                hostname = device_yaml['devices'][device]['connections']['cli']['ip'],
                                username = user,
                                password = pasw
                            )
            )
    
    devices_table = [["HOSTNAME", "IP-GESTION", "FABRICANTE", "MODELO", "VERSION SO", "SERIAL_NUMBER"]]  # Variable utilizada para tabular resultados
    ### Obtener datos de dispositivos
    for device in network_devices:
        print("Conectando a {} ...".format(device.hostname))
        device.open()

        print("Obteniendo parametros...")
        device_facts = device.get_facts()
        
        ### Parsing de datos
        
        devices_table.append([device_facts["hostname"],
                                device.hostname,
                                device_facts["vendor"],
                                device_facts["model"],
                                device_facts["os_version"],
                                device_facts["serial_number"]
                                ])
        device.close()
    print("#"*100 + "\n")
    print(tabulate(devices_table, headers="firstrow"))
    print("\n"+"#"*100 + "\n")

if __name__ == '__main__':
    main()
