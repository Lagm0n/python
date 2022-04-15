import struct
a='41 9E A3 D7'
a='00 08 17 58'
ad=bytes.fromhex(a)
# ad=bytes(b'\x00\x08\x17:')
# # a = 102.18
# data=float(d)
# print(data)
gasValue=round(struct.unpack(">f",'00 08 17 58')[0])

print(gasValue)
