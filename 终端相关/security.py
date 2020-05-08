import pyb
from pyb import Pin
motion_detect = Pin('Y8',Pin.IN,Pin.PULL_UP)

def detectMotion():
	return motion_detect.value()