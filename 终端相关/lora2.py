#    LoRa.py
#Communication module: LoRa.
#Communication method with gateway via LoRa.
#Uart port drive LoRa module.
#Parse JSON between device and gateway via LoRa channel.
#LoRa module: E32-TTL-100
#Pin specification:
#Module         MCU
#MD0       <--> Y4     #mode setting, can not hang
#AUX       <--> Y3     #mode setting, can not hang
#RXD(IN)   <--> Y1     #UART4
#TXD(OUT)  <--> Y2     #UART4
#VCC       <--> 3.3V
#GND       <--> GND
#from lora import Lora
from pyb import UART 
from pyb import Pin
import pyb
class Lora():
	def __init__(self, AUXPin='Y3', MD0Pin='Y4', baudrate=9600):#M0输入，M1输出
		self.m = Pin('Y3', Pin.IN)
		self.M1 = Pin(MD0Pin, Pin.OUT_PP)
		self.m.irq(handler=self.__saved_data, trigger=Pin.IRQ_FALLING)#设置中断函数
		#根据模块手册，接收或发送数据时aux呈现高电平，发送接收完成时电平拉低
		#设置引脚中断，当电平变低时__save_data函数被调用，__save_data被调用时数据接收完毕
		self.count = 0#中断回掉函数调用计数
		self.M1.low()
		self.u4 = UART(6,baudrate)
		self.u4.init(baudrate, bits=8, parity=None, stop=1)
	def __saved_data(self, b):
		self.count = 1 + self.count
	def md0low(self):
		self.M1.low()
	def md0high(self):
		self.M1.high()

	def enterConfig(self):#进入设置模式，md0拉高，波特率设为115200
		self.M1.high()
		self.u4 = UART(6,115200)
		self.u4.init(115200, bits=8, parity=None, stop=1)
	def exitConfig(self, baudrate=9600):#退出设置模式，md0拉低，更改波特率
		self.M1.low()
		self.u4 = UART(6,baudrate)
		self.u4.init(baudrate, bits=8, parity=None, stop=1)

	def send(self, data):
		return self.u4.write(data)
	def recv(self, cycle=100):
		self.count = 0
		save_data = b''#收到的数据
		while True:
			if self.count == 1:#__save_data每调用一次，count+1
				if self.u4.any() > 0:
					save_data = save_data + self.u4.read()
				return save_data.decode('utf-8')
			if self.u4.any() > 12:
				save_data = save_data + self.u4.read()
			pyb.delay(cycle)#循环间隔100ms
			
	def getb(self):#获取二进制数据
		len = self.u4.any()
		if len > 0:
			recv = self.u4.read()
			return recv
		else:
			return -1
	def get(self):
		len = self.u4.any()
		if len > 0:
			recv = self.u4.read().decode('utf-8')
			return recv
		else:
			return -1
#	串口对应GPIO

#	UART(4) is on XA: (TX, RX) = (X1, X2)  = (PA0,  PA1)
#	UART(1) is on XB: (TX, RX) = (X9, X10) = (PB6,  PB7)
#	UART(6) is on YA: (TX, RX) = (Y1, Y2)  = (PC6,  PC7)
#	UART(3) is on YB: (TX, RX) = (Y9, Y10) = (PB10, PB11)
#	UART(2) is on:    (TX, RX) = (X3, X4)  = (PA2,  PA3)