from crccheck.crc import Crc16Modbus


def setData(inputData:str):
    data = bytes.fromhex(inputData)
    crcData = Crc16Modbus.calchex(data = data, byteorder='little')
    crc = bytes.fromhex(crcData)
    return data + crc

g0=setData('05 03 01 52 00 03')
g1=setData('05 03 02 52 00 03')
g2=setData('05 03 03 52 00 03')
g3=setData('05 03 04 52 00 03')
g4=setData('05 03 05 52 00 03')
g5=setData('05 03 06 52 00 03')

print(g0.hex())
print(g1.hex())
print(g2.hex())
print(g3.hex())
print(g4.hex())
print(g5.hex())