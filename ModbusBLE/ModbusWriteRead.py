import asyncio
from bleak import BleakClient

address = "62:00:A1:10:00:5A"
write_uuid = "0000ffe9-0000-1000-8000-00805f9b34fb"
read_uuid = "0000ffe6-0000-1000-8000-00805f9b34fb"

async def run(address):    
    async with BleakClient(address) as client:
        print('connected')
        services = await client.get_services()        
        for service in services:
            for characteristic in service.characteristics:
                if characteristic.uuid == write_uuid:                       
                    # 데이터 쓰기전 원래 데이터 읽기
                    if 'read' in characteristic.properties:
                        read_data = await client.read_gatt_char(characteristic)
                        print('read before writing: ', read_data)
                    # 데이터 쓰기
                    if 'write' in characteristic.properties:
                        w=bytearray(b'\x05\x03\x02\x10\x00\x2A\xC5\xEC')
                        await client.no
                        await client.write_gatt_char(characteristic, w)                        
                    # 쓰기 이후 데이터 읽기
                    if 'read' in characteristic.properties:
                        read_data = await client.read_gatt_char(characteristic)
                        print('read after writing: ', read_data)
    
    print('disconnect')

loop = asyncio.get_event_loop()
loop.run_until_complete(run(address))
print('done')