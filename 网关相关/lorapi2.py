#!/usr/bin/env python
#    LoRa.py
#Communication module: LoRa.
#Communication method with device via LoRa.
#Uart port drive LoRa module.
#Pin specification:
#MD0    <--> GPIO(OUT)17    #mode setting
#AUX    <--> GPIO(OUT)27    #mode setting
#RXD   <--> 8(TXD)        #ttyS0
#TXD   <--> 10(RXD)       #ttyS0
#VCC   <--> 5V            #5V power
#GND   <--> GND           #GND

#Install pyserial:
#pip install pyserial    #Python2
#pip3 install pyserial   #Python3
#sudo apt-get install python-rpi.gpio
#python 3：sudo apt-get install python3-rpi.gpio
#Config UART port in raspberryPi:
#$ raspi-config
#Would you like a login shell to be accessible over serial? Choose No.
#Would you like the serial port hardware to be enabled?     Choose Yes.
#ttyS0 appear in /dev
#from lorapi import Lora
#lora = Lora()
#recv = lora.recv()
import serial  
import time
import RPi.GPIO as GPIO
#pyserial_test = serial.Serial("/dev/ttyS0", 115200)
class Lora():
	def __init__(self, baudrate=9600):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(17,GPIO.OUT)#MD0
		GPIO.setup(27,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)#AUX
		GPIO.output(17,GPIO.LOW)
		GPIO.add_event_detect(27, GPIO.FALLING, callback=self.__save_data)
		self.count=0
		self.pyserial_test = serial.Serial("/dev/ttyS0", baudrate)
	def __del__(self):
		self.pyserial_test.close()
		GPIO.cleanup()
	def __save_data(self, k):
		#time.sleep(0.4)
		#GPIO 27电平下降时执行此函数。
		# #此函数执行时代表发送或接收已经完成。
		print(k)
		self.count=self.count+1
	def getb(self):#读取缓冲区，返回二进制
		count = self.pyserial_test.inWaiting()#获取缓冲区中数据大小
		if count != 0:  
			recv = self.pyserial_test.read(count)
		else:
			return -1
		self.pyserial_test.flushInput()
		return recv
		
	def get(self):#读取缓冲区，返回字符串
		count = self.pyserial_test.inWaiting()#获取缓冲区中数据大小
		if count != 0:  
			recv = self.pyserial_test.read(count)
		else:
			return -1
		self.pyserial_test.flushInput()
		return recv.decode('utf-8')
		
	def recv(self, cycle=0.1, timeout=0.5, ctimeout=0):
		#等待数据，接收数据后返回数据。
		#ctimeout为最长等待时间，超时会返回-1 其他参数不用管。
		wait_time = 0#等待次数
		curr_size = 0#当前数据大小
		save_data = b''#收到的数据
		wait_max = timeout*10#最多等待次数
		cwait= ctimeout*(1/cycle)
		self.count = 0
		while True:
			if ctimeout!=0:
				cwait = cwait - 1
				if cwait == 0:
					return -1
			if self.count==1:
				#此函数开始执行时count为0,为1时代表__save_data函数执行了,数据接收完毕,可以返回.
				#time.sleep(0.5)
				if self.pyserial_test.inWaiting() > 0:
					save_data = save_data + self.pyserial_test.read(self.pyserial_test.inWaiting())
				self.count = 0
				return save_data.decode('utf-8')

			if self.pyserial_test.inWaiting() > 10:
				save_data = save_data + self.pyserial_test.read(self.pyserial_test.inWaiting())
			time.sleep(0.1)

	def send(self, data):#发送字符串
		return self.pyserial_test.write(data.encode('utf-8'))
	def sendb(self, data):#发送二进制
		return self.pyserial_test.write(data)