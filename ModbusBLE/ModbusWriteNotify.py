import asyncio
from pickletools import bytes8
from bleak import BleakClient

address = "62:00:A1:10:00:5A"
write_uuid = "0000ffe9-0000-1000-8000-00805f9b34fb"
notify_uuid = "0000ffe4-0000-1000-8000-00805f9b34fb"


def notify_callback(sender: int, data: bytearray):
    print('sender: ', sender, 'data: ', data)

async def run(address, write, notify):    
    async with BleakClient(address) as client:
        print('connected')
        services = await client.get_services()        
        for service in services:
            for characteristic in service.characteristics:
                if characteristic.uuid == write:                       
                    if 'write' in characteristic.properties:
                        print('write data')
                        await client.write_gatt_char(characteristic, bytes8(b'05030210002AC5EC'))   
                if characteristic.uuid == notify:
                    if 'notify' in characteristic.properties:
                        print('try to activate notify.')
                        await client.start_notify(characteristic, notify_callback)
    
    print('disconnect')

loop = asyncio.get_event_loop()
loop.run_until_complete(run(address, write_uuid, notify_uuid))
print('done')