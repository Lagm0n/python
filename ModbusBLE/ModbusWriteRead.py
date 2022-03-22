import asyncio
from bleak import BleakClient

address = "8c:aa:b5:84:db:52"
read_write_charcteristic_uuid = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

async def run(address):    
    async with BleakClient(address) as client:
        print('connected')
        services = await client.get_services()        
        for service in services:
            for characteristic in service.characteristics:
                if characteristic.uuid == read_write_charcteristic_uuid:                       
                    # 데이터 쓰기전 원래 데이터 읽기
                    if 'read' in characteristic.properties:
                        read_data = await client.read_gatt_char(characteristic)
                        print('read before writing: ', read_data)
                    # 데이터 쓰기
                    if 'write' in characteristic.properties:
                        await client.write_gatt_char(characteristic, bytes(b'hello world'))                        
                    # 쓰기 이후 데이터 읽기
                    if 'read' in characteristic.properties:
                        read_data = await client.read_gatt_char(characteristic)
                        print('read after writing: ', read_data)
    
    print('disconnect')

loop = asyncio.get_event_loop()
loop.run_until_complete(run(address))
print('done')