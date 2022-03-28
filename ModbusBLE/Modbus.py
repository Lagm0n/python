import asyncio
from bleak import BleakClient
from bleak import BleakScanner

# def scan():
#     print("Scanning for bluetooth devices")
#     devices =BLE.getDeviceList()
#     print("Found {0} devices.\n".format(len(devices)))
#     count = 0
#     for device in devices:
#         print("Device Number : %s" %count)
#         print("Device name : %s" %device.name)
#         print("Device Mac Adrress : %s\n" %device.address)
#         count = count + 1
#     selectNumber=int(input("Select the device number to retrieve the UUID from : "))
#     return devices[selectNumber].address


WRITE_UUID = "0000ffe9-0000-1000-8000-00805f9b34fb"
NOTIFY_UUID = "0000ffe4-0000-1000-8000-00805f9b34fb"

async def Scan():
    devices = await BleakScanner.discover()
    print("Found {0} devices.\n".format(len(devices)))
    count = 0
    for device in devices:
        print("Device Number : %s" %count)
        print("Device name : %s" %device.name)
        print("Device Mac Adrress : %s\n" %device.address)
        count = count + 1

    selectNumber=int(input("Select the device number to retrieve the UUID from : "))

    if len(devices) < selectNumber or selectNumber < 0:
        selectNumber=int(input("Select the device number to retrieve the UUID from : "))
        
    async with BleakClient(devices[selectNumber].address) as client:
        print("\nConnecting...")
        services = await client.get_services()
        for service in services:
            for characteristic in service.characteristics:
                print("\t\tUUID : %s" %characteristic.uuid)
                print("\t\tproperties : %s\n" %characteristic.properties)
    return devices[selectNumber].address            


def notify_callback(sender: int, data: bytearray):
    print('sender: ', sender, 'data: ', data.hex())

async def dataRequest(address: str, data:bytearray):
    async with BleakClient(address) as client:
        print('connected')
        services = await client.get_services()
        for service in services:
            for characteristic in service.characteristics:
                if characteristic.uuid == WRITE_UUID:                       
                    if 'write' in characteristic.properties:
                        print('write data')
                        # data = bytearray(b'\x05\x03\x02\x10\x00\x2A\xC5\xEC')
                        await client.write_gatt_char(characteristic, data)  
                if characteristic.uuid == NOTIFY_UUID:
                    if 'notify' in characteristic.properties:
                        print('try to activate notify.')
                        await client.start_notify(characteristic.uuid, notify_callback)
                        await asyncio.sleep(5.0)
                        await client.stop_notify(characteristic.uuid)
    print('disconnect')



loopScan = asyncio.get_event_loop()
addr=loopScan.run_until_complete(Scan())

loopDR = asyncio.get_event_loop()
loopDR.run_until_complete(dataRequest(addr,bytearray(b'\x05\x03\x02\x10\x00\x2A\xC5\xEC')))