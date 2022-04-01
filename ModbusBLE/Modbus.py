import asyncio
from bleak import BleakClient
from bleak import BleakScanner
from crccheck.crc import Crc16Modbus
#블루투스 장비 스캔 함수
async def Scan():
    #딕셔너리 생성
    bluetoothData=dict()
    #블루투스 리스트
    devices = await BleakScanner.discover()
    #블루투스 몇개 찾았는지 출력
    print("Found {0} devices.\n".format(len(devices)))
    count = 0
    #블루투스 리스트 돌면서 정보 출력
    for device in devices:
        print("Device Number : %s" %count)
        print("Device name : %s" %device.name)
        print("Device Mac Adrress : %s\n" %device.address)
        count = count + 1
    #선택할 디바이스 순서 사용자로부터 입력받기
    selectNumber=int(input("Select the device number to retrieve the UUID from : "))
    #입력범위 벗어나면 다시 입력
    if len(devices) < selectNumber or selectNumber < 0:
        selectNumber=int(input("Select the device number to retrieve the UUID from : "))
    #딕셔너리(bluetoothData)에 key('address')로 선택한 value(주소값) 추가 
    bluetoothData['address'] = devices[selectNumber].address
    #선택한address로 연결하면서 client로 변수처리
    async with BleakClient(devices[selectNumber].address) as client:
        print("\nConnecting...")
        #연결된 블루투스의 서비스리스트
        services = await client.get_services()
        #서비스리스트의 내부를 루프 돌면서 필요한 데이터 딕셔너리(bluetoothData)에 추가
        for service in services:
            #서비스리스트의 내부 캐릭터리스트 돌면서 필요한 정보 수집
            for characteristic in service.characteristics:
                #캐릭터리스트 속성에 'write'가 있으면 딕셔너리(bluetoothData)에 
                #key('write')로 해당UUID를value(write속성을 가진 uuid값) 추가
                if 'write' in characteristic.properties:
                    bluetoothData['write'] = characteristic.uuid
                #캐릭터리스트 속성에 'notify'가 있으면 딕셔너리(bluetoothData)에 
                #key('notify')로 해당UUID를value(notify속성을 가진 uuid값) 추가
                if 'notify' in characteristic.properties:
                    bluetoothData['notify'] = characteristic.uuid
                #리스트의 모든 캐릭터uuid와 캐릭터 속성 출력
                print("\t\tUUID : %s" %characteristic.uuid)
                print("\t\tproperties : %s\n" %characteristic.properties)
    #선택한 블루투스의 데이터 값(주소,write_uuid,notify_uuid) 반환            
    return bluetoothData            


def notify_callback(sender: int, data: bytearray):
    #입력받은데이터를 헥사로 변환하여 출력 sender는 서비스uuid 출력시 나오는 handle의 수 크게 의미 없음
    print('sender: ', sender, 'data: ', data.hex())

#데이터 요청 함수
async def dataRequest(bluetoothData: dict, data:bytearray):
    #입력받은 주소로 연결 및 client로 변수처리
    async with BleakClient(bluetoothData['address']) as client:
        print('connected')
        #연결된 블루투스의 서비스리스트 
        services = await client.get_services()
        #서비스리스트의 내부를 루프돌면서 캐릭터리스트를 찾는다
        for service in services:
            #캐릭터리스트의 내부를 루프 돌면서 속성에 맞는 작업 진행
            for characteristic in service.characteristics:
                #캐릭터리스트의 내부 uuid가 bluetoothData의 write uuid와 동일하면 데이터 요청
                if characteristic.uuid == bluetoothData['write']:                       
                    if 'write' in characteristic.properties:
                        print('Requesting data...')
                        # data = bytearray(b'\x05\x03\x02\x10\x00\x2A\xC5\xEC')
                        await client.write_gatt_char(characteristic, data) 
                #캐릭터리스트의 내부 uuid가 bluetoothData의 notify uuid와 동일하면 데이터 읽기
                if characteristic.uuid == bluetoothData['notify']:
                    if 'notify' in characteristic.properties:
                        print('try to activate notify.')
                        #데이터 요청 후 읽어들이는 notify 함수 시작
                        await client.start_notify(characteristic.uuid, notify_callback)
                        await asyncio.sleep(5.0)
                        #데이터 요청 후 읽어들이는 notify 함수 종료
                        await client.stop_notify(characteristic.uuid)
    print('disconnect')
#입력받은 데이터 가공하는 함수
def setData(inputData:str):
    data=[]
    #스트링 파싱
    datalist = [inputData[i:i+2] for i in range(0,len(inputData),2)]
    #스트링 16진법으로 변환
    for item in datalist:
        data.append(r'\x' + item.upper())
    #리스트를 스트링으로 통합
    data = "".join(data)
    #바이트로 형변환
    data1 = bytes(data, 'utf-8')
    #CRC 함수 사용(타입 : data 바이트,byteorder 바이트 정렬 big or little)
    crc = Crc16Modbus.calchex(data = data1, byteorder='little')
    print(datalist)
    # print(data)
    # print(data1)
    # print(crc)
    return



data  = bytes(b'\x05\x03\x02\x10\x00\x2A')

# 05 03 01 10 00 2A c5 ec
# 05 03 02 50 00 05 85 E4
crc = Crc16Modbus.calchex(data = data, byteorder='little')
# crc=crc.upper()
print(data)
print("----------------")
setData("05030110002A")
print(crc)

# #블루투스 스캔 함수 실행
# loopScan = asyncio.get_event_loop()
# bleData=loopScan.run_until_complete(Scan())

# #데이터 요청 함수 실행
# loopDR = asyncio.get_event_loop()
# loopDR.run_until_complete(dataRequest(bleData,bytearray(b'\x05\x03\x02\x10\x00\x2A\xC5\xEC')))