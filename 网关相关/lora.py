#    LoRa.py
#Communication module: LoRa.
#Communication method with gateway via LoRa.
#Uart port drive LoRa module.
#Parse JSON between device and gateway via LoRa channel.
#LoRa module: E32-TTL-100
#Pin specification:
#Module         MCU
#M0(IN)    <--> Y3     #mode setting, can not hang
#M1(IN)    <--> Y4     #mode setting, can not hang
#RXD(IN)   <--> Y1     #UART4
#TXD(OUT)  <--> Y2     #UART4
#AUX(OUT)  <--> 
#VCC       <--> 3.3V
#GND       <--> GND

#Communication mode is 0, need to set M0 and M1 to 0.
#默认设置:b'\xc0\x00\x00\x1a\x17D'
#定点通信发送端设置:b'\xc0\xd0\x00\x1a\x04\xc4',接收端设置b'\xc0\x10\x00\x1a\x04\xc4'
#其中第2,3字节是地址\xd0\x00,
#第5字节\x04是信道,最后一字节\xc4打开定点发送使能.更多帮助可以查看模块手册.
#发送lora.send(b'\x10\x00\x04aacc'),前2字节为接收端地址,第三字节为信道
#from lora import Lora
from pyb import UART 
from pyb import Pin
import pyb
class Lora():
	def __init__(self, M0Pin='Y3', M1Pin='Y4', baudrate=9600):
		self.M0 = Pin(M0Pin, Pin.OUT_PP)
		self.M1 = Pin(M1Pin, Pin.OUT_PP)
		self.M0.low()
		self.M1.low()
		self.u4 = UART(6,baudrate)
		self.u4.init(baudrate, bits=8, parity=None, stop=1)
	def getSetting(self):#获取当前工作参数
		v0 = self.M0.value()
		v1 = self.M1.value()
		self.M0.high()
		self.M1.high()
		self.send(b'\xC1\xC1\xC1')
		pyb.delay(100)
		data = self.u4.read()
		if v0 == 0:
			self.M0.low()
		if v1 == 0:
			self.M1.low()
		return data
		
	def updateSetting(self, data):#更新工作参数,详细工作参数设置请查阅模块手册
		v0 = self.M0.value()
		v1 = self.M1.value()
		self.M0.high()
		self.M1.high()
		pyb.delay(100)
		i = self.send(data)
		if v0 == 0:
			self.M0.low()
		if v1 == 0:
			self.M1.low()
		return i
	
	def getStat(self):#
		return self.M0.value(), self.M1.value()
		
	def sleep(self):#休眠模式 3, M0 = 1, M1 = 1 
		#此模式不能收也不能发
		self.M0.high()
		self.M1.high()
	def powerSave(self):#省电模式 2, M0 = 0, M1 = 1 
		#此模式只能收唤醒模式发送的数据,不能发送数据
		self.M0.low()
		self.M1.high()
	def awake(self):#唤醒模式 1, M0 = 1, M1 = 0 
		#参考上面,能收能发
		self.M0.high()
		self.M1.low()
	def normal(self):#一般模式 0, M0 = 0, M1 = 0 
		#能收能发
		self.M0.low()
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
