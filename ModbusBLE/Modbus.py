import asyncio
from bleak import BleakClient
from bleak import BleakScanner
from crccheck.crc import Crc16Modbus

async def Scan():
    bluetoothData=dict()
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
    
    bluetoothData['address'] = devices[selectNumber].address
    async with BleakClient(devices[selectNumber].address) as client:
        print("\nConnecting...")
        services = await client.get_services()
        for service in services:
            for characteristic in service.characteristics:
                if 'write' in characteristic.properties:
                    bluetoothData['write'] = characteristic.uuid
                if 'notify' in characteristic.properties:
                    bluetoothData['notify'] = characteristic.uuid

                print("\t\tUUID : %s" %characteristic.uuid)
                print("\t\tproperties : %s\n" %characteristic.properties)
    return bluetoothData            


def notify_callback(sender: int, data: bytearray):
    print('sender: ', sender, 'data: ', data.hex())

async def dataRequest(bluetoothData: dict, data:bytearray):
    async with BleakClient(bluetoothData['address']) as client:
        print('connected')
        services = await client.get_services()
        for service in services:
            for characteristic in service.characteristics:
                if characteristic.uuid == bluetoothData['write']:                       
                    if 'write' in characteristic.properties:
                        print('Requesting data...')
                        # data = bytearray(b'\x05\x03\x02\x10\x00\x2A\xC5\xEC')
                        await client.write_gatt_char(characteristic, data)  
                if characteristic.uuid == bluetoothData['notify']:
                    if 'notify' in characteristic.properties:
                        print('try to activate notify.')
                        await client.start_notify(characteristic.uuid, notify_callback)
                        await asyncio.sleep(5.0)
                        await client.stop_notify(characteristic.uuid)
    print('disconnect')
data = bytearray(b'\x05\x03\x02\x10\x00\x2A')
# 05 03 01 10 00 2A c5 ec
# 05 03 02 50 00 05 85 E4
crc = Crc16Modbus.calchex(data = data)


# loopScan = asyncio.get_event_loop()
# bleData=loopScan.run_until_complete(Scan())
# # print(bleData)

# loopDR = asyncio.get_event_loop()
# loopDR.run_until_complete(dataRequest(bleData,bytearray(b'\x05\x03\x02\x10\x00\x2A\xC5\xEC')))
print(crc)