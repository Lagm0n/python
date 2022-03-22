from ModbusFrameWork import *

BLE=AsyncBluetooth()

def scan():
    print("Scanning for bluetooth devices")
    devices =BLE.getDeviceList()
    print("Found {0} devices.\n".format(len(devices)))
    for device in devices:
        print("Device  : %s" %device)
        print("Device name : %s" %device.name)
        print("Device metadata : %s" %device.metadata)
        print("Device Mac Address : %s" %device.address)
        print("\n")
    return()

scan()