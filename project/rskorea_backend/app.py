import json
import struct
from typing import Dict
from GasData import Gas
from flask import Flask, jsonify, request
from bleak import BleakScanner
from bleak import BleakClient
from crccheck.crc import Crc16Modbus
import asyncio
# from crccheck import Crc16Modbus
app =Flask(__name__)

gasCount = 0
gasBeanList = []
gasValueList = []
address = ''
gasCount = 0

async def setScanList():
    bluetoothList=list()
    devices = await BleakScanner.discover()
    for device in devices:
        jsonstr={'name':device.name, 'address':device.address}
        bluetoothList.append(jsonstr)
    return bluetoothList


@app.route('/scan', methods=['GET'])
async def scanData():
    scanList = await setScanList()
    result = dict()
    result['len'] = len(scanList)
    result['bluetoothList']= scanList
    return jsonify(result)

# @app.route('/scan', methods=['GET'])
# def scanData():
#     asyncio.set_event_loop(asyncio.SelectorEventLoop())
#     loop = asyncio.get_event_loop()
#     scanList = loop.run_until_complete(setScanList())
#     result = dict()
#     result['len'] = len(scanList)
#     result['bluetoothList']= scanList
#     return jsonify(result)
##################################################################################

def setData(inputData:str):
    data = bytes.fromhex(inputData)
    crcData = Crc16Modbus.calchex(data = data, byteorder='little')
    crc = bytes.fromhex(crcData)
    return data + crc

# 일반 파라미터 요청함수(가스 갯수)
def getSystemParameters(sender: int,data: bytearray):
    global gasCount
    datalen=data[2]
    gasdata=data[3:len(data)-2]
    if datalen!=len(gasdata):
        print('The number of requested data and the number of actual data are different\n')
    gasCount=gasdata[1]
    
# 고정 파라미터 요청함수(가스 종류,단위 등등)
def getFixParameters(sender: int, data: bytearray):
    global gasType
    global unitType
    fixParam=Gas()
    datalen=data[2]
    gasdata=data[3:len(data)-2]
    if datalen != len(gasdata):
        print('The number of requested data and the number of actual data are different\n')
    gasBean=fixParam.getGas(gasdata[1])
    unitBean=fixParam.getUnit(gasdata[3])
    gasType = dict()
    unitType = dict()
    
    gasType['name']=gasBean.name
    gasType['formula']=gasBean.formula
    gasType['number']=gasBean.number.decode('utf-8')

    unitType['name']=unitBean.name
    unitType['number']=unitBean.number.decode('utf-8')

# 실시간 파라미터 요청 함수()
def getGasData(sendr:int, data:bytearray):
    global gasValue
    datalen=data[2]
    gasdata=data[3:len(data)-2]
    lVal=gasdata[0:2]
    hval=gasdata[2:4]
    changeLocation=hval+lVal
    if datalen!=len(gasdata):
        print('The number of requested data and the number of actual data are different\n')
    gasValue=round(struct.unpack(">f",changeLocation)[0],3)
    
async def setGasCount(address: str):
    async with BleakClient(address) as client:
        services = await client.get_services()
        for service in services:
            for characteristic in service.characteristics:
                if 'write' in characteristic.properties:
                    sendData=setData('05 03 00 20 00 16')
                    await client.write_gatt_char(characteristic.uuid,sendData)
                if 'notify' in characteristic.properties:
                    await client.start_notify(characteristic.uuid,getSystemParameters)
                    await asyncio.sleep(1.0)
                    await client.stop_notify(characteristic.uuid)
        return int(gasCount)

async def setGasBean(address: str, gasCount: int):
    gasBeanList=list()
    async with BleakClient(address) as client:
        services = await client.get_services()
        for service in services:
            for i in range(1,gasCount+1):
                for characteristic in service.characteristics:
                    if 'write' in characteristic.properties:
                        sendData = setData('05 03 0{0} 10 00 2A'.format(i))
                        await client.write_gatt_char(characteristic.uuid,sendData)
                    if 'notify' in characteristic.properties:
                        await client.start_notify(characteristic.uuid, getFixParameters)
                        await asyncio.sleep(1.0)
                        # await client.stop_notify(characteristic.uuid)
                gasBean=dict()
                gasBean["Gas"]= gasType
                gasBean["Unit"]= unitType
                gasBeanList.append(gasBean)
        return gasBeanList

@app.route('/info',methods=['GET','POST'])
async def gasData():
    global gasCount
    global gasBeanList
    global address
    global gasCount

    if(request.method =='POST'):
        request_data = request.get_data()
        address =request_data.decode('utf-8')
        gasCount= await setGasCount(address)
        gasBeanList= await setGasBean(address=address,gasCount=gasCount)
    else:
        result = dict()
        result['gasCount'] = gasCount
        result['gasBeanList'] = gasBeanList
        return jsonify(result) 
    return ''

async def setGasValue(address:str, gasCount: int):
    gasValueList=list()
    async with BleakClient(address) as client:
        services = await client.get_services()
        for service in services:
            for i in range(1,gasCount+1):
                for characteristic in service.characteristics:
                    if 'write' in characteristic.properties:
                        sendData = setData('05 03 0{0} 52 00 03'.format(i))
                        await client.write_gatt_char(characteristic.uuid,sendData)
                    if 'notify' in characteristic.properties:
                        await client.start_notify(characteristic.uuid, getGasData)
                        await asyncio.sleep(1.0)
                        # await client.stop_notify(characteristic.uuid)
                gasValueList.append(gasValue)
        return gasValueList

@app.route('/value',methods=['GET'])
async def valueData():
    global gasCount
    global gasValueList
    global address
    
    gasValueList = await setGasValue(address,gasCount)
    result = dict()
    result['gasValueList'] = gasValueList
    print(result)
    return jsonify(result)
if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio(app.run(debug=True))