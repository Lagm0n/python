import asyncio
from bleak import BleakClient
address = "62:00:A1:10:00:5A"
MODEL_NBR_UUID = "0000ffe6-0000-1000-8000-00805f9b34fb"
async def main(address):
    client = BleakClient(address)
    try:
        await client.connect()
        model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        print("Model Number: {0}".format("".join(map(chr, model_number))))
    except Exception as e:
        print(e)
    finally:
        await client.disconnect()
asyncio.run(main(address))
