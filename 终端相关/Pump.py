import pyb
from pyb import Pin
pin_out = Pin('X2'，Pin.OUT_PP)
pin_out.high()
state = 0

def Pump_on():
    pin_out.low()
    state = 1
    
def Pump_off():
    pin_out.high()
    state = 0
    
def getState():
    return state