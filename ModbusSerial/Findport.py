import serial.tools.list_ports 


def macAddfinder():
    res='None'
    dev = serial.tools.list_ports.comports()
    port=[]
    for com in dev:
        port.append((com.device, com.hwid))
    macAddress = "6200a110005a"
    print('\n')
    print("port List \n ->")
    print(port)
    print('\n')

    for device in port:
        if macAddress in device[1]:
            res = str(device[0])
    print("\nBluetooth MAC Address is [" + macAddress + "]\nDevice detected serial ports:")
    return res

if __name__ == '__main__':
    print("-> Port is [" + macAddfinder() + "]")