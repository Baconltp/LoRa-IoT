import pyb
from pyb import Pin
p_in=Pin('Y12',Pin.IN,Pin.PULL_UP)
adc=pyb.ADC(Pin('Y11'))
adc=pyb.ADC(pyb.Pin.board.Y11)

def getMoisAo():
    return adc.read()
def getMoisDo():
    return p_in.value