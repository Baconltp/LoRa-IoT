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
	def __init__(self, M0Pin='Y3', M1Pin='Y4', baudrate=9600):#M0输入，M1输出
		#self.M0 = Pin(M0Pin, Pin.OUT_PP)
		self.M1 = Pin(M1Pin, Pin.OUT_PP)
		#self.M0.low()
		self.M1.low()
		self.u4 = UART(6,baudrate)
		self.u4.init(baudrate, bits=8, parity=None, stop=1)
	def md0high(self):
		self.M1.high()
	def md0low(self):
		self.M1.low()
	def send(self, data):
		return self.u4.write(data)
	def recv(self, cycle=100, timeout=500):
		wait_time = 0#等待次数
		curr_size = 0#当前数据大小
		save_data = ''#收到的数据
		wait_max = timeout/100#最多等待次数
		while True:
			size = self.u4.any()
			if size != 0:
				curr_size = size#当前数据大小
				recv_size = 0
				while True:
					if wait_time >= wait_max :#如果等待次数超过最多等待次数就返回数据
						if size != 0:#返回数据前将缓冲区的数据接收
							save_data = save_data + self.u4.read().decode('utf-8')
						return save_data
					if size >= 58:#当缓冲区的数据大于58字节时接收数据
						save_data = save_data + self.u4.read().decode('utf-8')
						recv_size = recv_size + size
						curr_size = size = self.u4.any()
						wait_time = 0
						continue
					if size == curr_size:#如果没有接到新数据，则等待次数加一
						wait_time = wait_time + 1
					pyb.delay(100)
					size = self.u4.any()
					if size != curr_size:#如果有新收到的数据，就更新等待次数
						curr_size = size
						wait_time = 0
			pyb.delay(cycle)#如果没有收到数据就再等待一个周期
			
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
