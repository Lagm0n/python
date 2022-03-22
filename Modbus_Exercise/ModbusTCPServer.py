from pyModbusTcCP.server import ModbusServer, DataBank
from time import sleep
from random import uniform

server = ModbusServer('127.0.0.1',502, no_block=True)

try:
    print('start server..')
    server.start()
    print('server is online')
    state=[0]
    while True:
        DataBank.set_words(0,(int(uniform(0,100))))
        if state != DataBank.get_words(1):
            state = DataBank.get_words(1)
            print("Value of Register 1 has changed to " + str(state))
            sleep(0.5)
except:
    print('shutdown server...')
    server.stop()
    print('server i offline')