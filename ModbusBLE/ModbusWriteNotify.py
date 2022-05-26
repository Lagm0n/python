import asyncio
from bleak import BleakClient

address = "62:00:A1:10:00:5A"
write_uuid = "0000ffe9-0000-1000-8000-00805f9b34fb"
notify_uuid = "0000ffe4-0000-1000-8000-00805f9b34fb"


def notify_callback(sender: int, data: bytearray):
    print('sender: ', sender, 'data: ', data.hex())

def CRCcheck(data):
    print()

async def dataRequest(address, write, notify):    
    async with BleakClient(address) as client:
        print('connected')
        services = await client.get_services()
        for service in services:
            for characteristic in service.characteristics:
                if characteristic.uuid == write:                       
                    if 'write' in characteristic.properties:
                        print('write data')
                        w=bytearray(b'\x05\x03\x02\x10\x00\x2A\xC5\xEC')
                        await client.write_gatt_char(characteristic, w)  
                if characteristic.uuid == notify:
                    if 'notify' in characteristic.properties:
                        print('try to activate notify.')
                        await client.start_notify(characteristic.uuid, notify_callback)
                        await asyncio.sleep(5.0)
                        await client.stop_notify(characteristic.uuid)
    print('disconnect')

loop = asyncio.get_event_loop()
loop.run_until_complete(dataRequest(address, write_uuid, notify_uuid))
print('done')





# [0x05, 0x03, 0x00, 0x20, 0x00, 0x16, 0xC4,0x4A