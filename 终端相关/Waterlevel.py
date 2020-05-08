import pyb
from pyb import Pin

adc=pyb.ADC(Pin('A7'))
adc=pyb.ADC(pyb.Pin.board.X8)

def getWaterLevel():
    return adc.read()