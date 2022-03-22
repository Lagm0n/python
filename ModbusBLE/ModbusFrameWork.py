import asyncio
from bleak import BleakScanner
from bleak import BleakClient

class Bluetooth:
    #비동기 클래스 필수 함수 1
    async def __aenter__(self):
        self.BleakScanner = BleakScanner()
        self.BleakClient = BleakScanner()
        self.bleak = await self.BleakScanner.__aenter__()
        self.bleak = await self.BleakClient.__aenter__()
        return self
    #비동기 클래스 필수 함수 2
    async def __aexit__(self, *args, **kwargs):
        await self._conn.__aexit__(*args, **kwargs)

    #디바이스 스캐닝
    async def GeDeviceList(self):
        async with BleakScanner() as scanner:
            #대기시간 단위 초
            await asyncio.sleep(3.0)
            #검색된 장치 얻어오기
            devices = scanner.discovered_devices
        #검색된 리스트 출력
        # for device in devices:
        #     print(device)
        return devices

    async def SetConnect(self, addr):
        client = BleakClient(addr)
        try:
            client.set_disconnected_callback(self.OnDisconnect)
            await client.connect()
            print(addr+" connected Success")
        except Exception as e:
            print('error:', e)
        finally:
            print(addr + " connection status : " + str(client.is_connected))

        return client.is_connected
        
    # async def SetDisconnet(self):
    #     await client.disconnect()
    #     return bool
class AsyncBluetooth:
    def __init__(self):
        self.ble = Bluetooth()
        self.loop = asyncio.get_event_loop()
    
    # 장치와 연결해제시 발생하는 콜백 이벤트
    def OnDisconnect(self, client):
        print("Client with address {} got disconnected".format(client.address))

    def getDeviceList(self):
        return self.loop.run_until_complete(self.asyncGetDeviceList())

    def connectDevice(self, addr):
        print(addr)
        return self.loop.run_until_complete(self.asyncConnect(addr))
    
    async def asyncConnect(self, addr):
        await self.ble.SetConnect(addr)
        return await Bluetooth.SetConnect(self, addr)

    async def asyncGetDeviceList(self):
        await self.ble.GeDeviceList()
        return await Bluetooth.GeDeviceList(self)


