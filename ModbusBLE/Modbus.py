import asyncio
import struct
from GasData import Gas
from bleak import BleakClient
from bleak import BleakScanner
from crccheck.crc import Crc16Modbus
import requests
import json

#블루투스 장비 스캔 함수
async def Scan():
    #딕셔너리 생성
    bluetoothData=dict()
    #블루투스 리스트
    devices = await BleakScanner.discover()
    #블루투스 몇개 찾았는지 출력
    print("Found {0} devices.\n".format(len(devices)))
    count = 1
    #블루투스 리스트 돌면서 정보 출력
    for device in devices:
        print("Device Number : %s" %count)
        print("Device name : %s" %device.name)
        print("Device Mac Adrress : %s\n" %device.address)
        count = count + 1
    #선택할 디바이스 순서 사용자로부터 입력받기
    selectNumber=int(input("Select the device number to retrieve the UUID from : ")) - 1
    #입력범위 벗어나면 다시 입력
    if len(devices) < selectNumber or selectNumber < 0:
        selectNumber=int(input("Select the device number to retrieve the UUID from : ")) - 1
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

# 일반 파라미터 요청함수(가스 갯수)
def getSystemParameters(sender: int,data: bytearray):
    global gasCount
    #입력받은데이터를 헥사로 변환하여 출력 sender는 서비스uuid 출력시 나오는 handle의 수 크게 의미 없음
    # print('sender : ', sender, 'data: ', data.hex())
    # print('RequestData : ', data[2:len(data)-2],'\n')
    datalen=data[2]
    gasdata=data[3:len(data)-2]
    # print('data requested : actual data >> ', datalen, ' : ', len(gasdata), '\n')
    if datalen!=len(gasdata):
        print('The number of requested data and the number of actual data are different\n')
    gasCount=gasdata[1]
    # print("gasCount : ",gasCount)

# 고정 파라미터 요청함수(가스 종류,단위 등등)
def getFixParameters(sender: int, data: bytearray):
    global gasType
    global unitType
    fixParam=Gas()
    datalen=data[2]
    gasdata=data[3:len(data)-2]
    # print('data requested : actual data >> ', datalen, ' : ', len(gasdata), '\n')
    if datalen != len(gasdata):
        print('The number of requested data and the number of actual data are different\n')
    gasType=fixParam.getGas(gasdata[1])
    unitType=fixParam.getUnit(gasdata[3])
    # print('gasType\t:\t',gasType.formula)
    # print('unitType:\t',unitType.name)
    # print('\n')


# 실시간 파라미터 요청 함수()
def getGasData(sendr:int, data:bytearray):
    global gasValue

    datalen=data[2]
    gasdata=data[3:len(data)-2]
    lVal=gasdata[0:2]
    hval=gasdata[2:4]
    
    changeLocation=hval+lVal
    # print('gasdata : ',gasdata)
    # print('changeLocation : ',changeLocation)

    # valuedata=bytes.fromhex(changeLocation)
    
    # print('data requested : actual data >> ', datalen, ' : ', len(gasdata), '\n')
    if datalen!=len(gasdata):
        print('The number of requested data and the number of actual data are different\n')
    gasValue=round(struct.unpack(">f",changeLocation)[0],3)
    # print(gasValue)

def getGasInformation(gasCount : int, gasSet:dict, gasValue: float):
    ...

#데이터 요청 함수
async def dataRequest(bluetoothData: dict, data:str,num=0):
    #입력받은 주소로 연결 및 client로 변수처리
    async with BleakClient(bluetoothData['address']) as client:
        global gasCount
        global gasType
        global unitType
        global gasValue
        # print('connected\n')
        #연결된 블루투스의 서비스리스트 
        services = await client.get_services()
        #서비스리스트의 내부를 루프돌면서 캐릭터리스트를 찾는다
        while client.is_connected:
            for service in services:
                #캐릭터리스트의 내부를 루프 돌면서 속성에 맞는 작업 진행
                for characteristic in service.characteristics:
                    #캐릭터리스트의 내부 uuid가 bluetoothData의 write uuid와 동일하면 데이터 요청
                    if characteristic.uuid == bluetoothData['write']:                       
                        if 'write' in characteristic.properties:
                            # print('Requesting data...')
                            if num == 0:
                                sendData = setData('05 03 00 20 00 16')
                            elif num == 1:
                                sendData = setData(data)
                            elif num == 2:
                                sendData = setData(data)
                            await client.write_gatt_char(characteristic, sendData) 
                    #캐릭터리스트의 내부 uuid가 bluetoothData의 notify uuid와 동일하면 데이터 읽기
                    if characteristic.uuid == bluetoothData['notify']:
                        if 'notify' in characteristic.properties:
                            # print('try to activate notify.')
                            #데이터 요청 후 읽어들이는 notify 함수 시작
                            if num == 0:
                                await client.start_notify(characteristic.uuid, getSystemParameters)
                            elif num == 1:
                                await client.start_notify(characteristic.uuid, getFixParameters)
                            elif num == 2:
                                await client.start_notify(characteristic.uuid, getGasData)
                            await asyncio.sleep(1.0)
                            #데이터 요청 후 읽어들이는 notify 함수 종료
                            await client.stop_notify(characteristic.uuid)
            # print('gasType\t:\t',gasType.formula)
            # print('unitType:\t',unitType.name)
            if num ==0:
                return gasCount
            elif num ==1:
                gasData=dict()
                gasData['Gas']=gasType
                gasData['Unit']=unitType
                return gasData
            elif num ==2:
                return gasValue
            else:
                print("Num ERROR")
            # count+=1 if count == 0 or count == 1 else count
            # print('...', gasCount)
            client.disconnect()

#입력받은 데이터 가공하는 함수
def setData(inputData:str):
    data = bytes.fromhex(inputData)
    crcData = Crc16Modbus.calchex(data = data, byteorder='little')
    crc = bytes.fromhex(crcData)
    return data + crc


# def main():
#     gCount=0
    
#     # #블루투스 스캔 함수 실행
#     loop = asyncio.get_event_loop()
#     bleData=loop.run_until_complete(Scan())
#     print("===========================일반 파라미터 요청===========================")
#     loop = asyncio.get_event_loop()
#     gCount=loop.run_until_complete(dataRequest(bleData,'05 03 00 20 00 16'))
#     print("===========================고정 파라미터 요청===========================")
#     gasSetList=list()
#     loop = asyncio.get_event_loop()
#     for i in range(1,gCount+1):
#         gasSetList.append(loop.run_until_complete(dataRequest(bleData,'05 03 0{0} 10 00 2A'.format(i),1)))
#     # print(gasSetList)
#     print("===========================실시간 파라미터 요청===========================")
#     loop = asyncio.get_event_loop()
#     for i in range(1,gCount):
#         loop.run_until_complete(dataRequest(bleData,'05 03 0{0} 52 00 03'.format(i),2))


def main():
    gasSetList=list()
    loop = asyncio.get_event_loop()
    bleData=loop.run_until_complete(Scan())
    gCount =loop.run_until_complete(dataRequest(bleData,'05 03 00 20 00 16'))
    for i in range(1,gCount+1):
        gasSetList.append(loop.run_until_complete(dataRequest(bleData,'05 03 0{0} 10 00 2A'.format(i),1)))
    while True:
        print('명령어 목록 ')
        print('1. 디바이스 가스 수 ')
        print('2. 가스명 - 단위 목록')
        print('3. 실시간 데이터 불러오기')
        print('4. 데이터 전송 ')
        print('9. 프로그램 종료')
        selectNumber=int(input("실행할 명령어를 선택해 주세요. : "))
        if (5 < selectNumber and selectNumber < 9)or (selectNumber < 1 and 9 < selectNumber):
            selectNumber=int(input("실행할 명령어를 선택해 주세요. : "))
            print('\n')
        if selectNumber == 1:
            print('가스 수: {0}개'.format(gCount))
        elif selectNumber ==2:
            for idx,item in enumerate(gasSetList,1):
                print('{0}. {1} - {2}'.format(idx,item['Gas'].name,item['Unit'].name))
        elif selectNumber ==3:
            for idx,item in enumerate(gasSetList,1):
                value=loop.run_until_complete(dataRequest(bleData,'05 03 0{0} 52 00 03'.format(idx),2))
                print('{0}. {1} : {2} {3}'.format(idx,item['Gas'].name,value,item['Unit'].name))
        elif selectNumber ==4:
            url='http://html.cielpia.com/rskorea/api/test2.php'
            jsonList=list()
            for idx,item in enumerate(gasSetList,1):
                value=loop.run_until_complete(dataRequest(bleData,'05 03 0{0} 52 00 03'.format(idx),2))
                jsonstr={'gas': '{0}'.format(item['Gas'].name), 'figure':'{0}'.format(value), 'unit':'{0}'.format(item['Unit'].name)}
                jsonList.append(jsonstr)
            jsonstr=json.dumps(jsonList)
            sendData = {"gastiger":jsonstr}
            resp = requests.post(url=url, data=sendData)
            print(resp.text)
        elif selectNumber ==9:
            break
        print('\n')



if __name__=='__main__':
    try:
        main()
    except:
        main()
