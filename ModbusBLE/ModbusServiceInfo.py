import asyncio
from bleak import BleakClient

address = "62:00:A1:10:00:5A"
async def serviceInfoScan(address):    
    async with BleakClient(address) as client:
        print('connected')
        services = await client.get_services()        
        for service in services:
            print(service)             
            print('\tuuid:', service.uuid)
            print('\tcharacteristic list:')
            for characteristic in service.characteristics:
                print('\t\t', characteristic)
                print('\t\tuuid:', characteristic.uuid)
                print('\t\tdescription :', characteristic.description)
                print('\t\tproperties :', characteristic.properties)
                print('\n')
    print('disconnect')

loop = asyncio.get_event_loop()
loop.run_until_complete(serviceInfoScan(address))
print('done')