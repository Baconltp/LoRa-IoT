#!/usr/bin/env python
#    LoRa.py
#Communication module: LoRa.
#Communication method with device via LoRa.
#Uart port drive LoRa module.
#Parse JSON between device and gateway via LoRa channel.
#LoRa module: E32-TTL-100
#Pin specification:
#M0    <--> GPIO(OUT)     #mode setting
#M1    <--> GPIO(OUT)     #mode setting
#RXD   <--> 8(TXD)        #ttyS0
#TXD   <--> 10(RXD)       #ttyS0
#AUX
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
		GPIO.setup(17,GPIO.OUT)#M0
		GPIO.setup(27,GPIO.OUT)#M1
		GPIO.output(17,GPIO.LOW)
		GPIO.output(27,GPIO.LOW)
		self.pyserial_test = serial.Serial("/dev/ttyS0", baudrate)
	def __del__(self):
		self.pyserial_test.close()
		GPIO.cleanup()
		
	def getSetting(self):
		v0 = GPIO.input(17)
		v1 = GPIO.input(27)
		GPIO.output(17,GPIO.HIGH)
		GPIO.output(27,GPIO.HIGH)
		self.pyserial_test.write(b'\xC1\xC1\xC1')
		time.sleep(0.1)
		data = self.pyserial_test.read(self.pyserial_test.inWaiting())
		if v0 == 0:
			GPIO.output(17,GPIO.LOW)
		if v1 == 0:
			GPIO.output(27,GPIO.LOW)
		return data
		
	def updateSetting(self, data):
		v0 = GPIO.input(17)
		v1 = GPIO.input(27)
		GPIO.output(17,GPIO.HIGH)
		GPIO.output(27,GPIO.HIGH)
		time.sleep(0.1)
		self.pyserial_test.write(data)
		time.sleep(0.1)
		data = self.pyserial_test.read(self.pyserial_test.inWaiting())
		if v0 == 0:
			GPIO.output(17,GPIO.LOW)
		if v1 == 0:
			GPIO.output(27,GPIO.LOW)
		return data
	
	def sleep(self):#休眠模式 3, M0 = 1, M1 = 1 
		GPIO.output(17,GPIO.HIGH)
		GPIO.output(27,GPIO.HIGH)
	def powerSave(self):#省电模式 2, M0 = 0, M1 = 1 
		GPIO.output(17,GPIO.LOW)
		GPIO.output(27,GPIO.HIGH)
	def awake(self):#唤醒模式 1, M0 = 1, M1 = 0 
		GPIO.output(17,GPIO.HIGH)
		GPIO.output(27,GPIO.LOW)
	def normal(self):#一般模式 0, M0 = 0, M1 = 0 
		GPIO.output(17,GPIO.LOW)
		GPIO.output(27,GPIO.LOW)
	def getStat(slef):
		return GPIO.input(17), GPIO.input(27)
	
	def getb(self):
		count = self.pyserial_test.inWaiting()#获取缓冲区中数据大小
		if count != 0:  
			recv = self.pyserial_test.read(count)#读取缓冲区
		else:
			return -1
		self.pyserial_test.flushInput()
		return recv
		
	def get(self):
		count = self.pyserial_test.inWaiting()#获取缓冲区中数据大小
		if count != 0:  
			recv = self.pyserial_test.read(count)#读取缓冲区
		else:
			return -1
		self.pyserial_test.flushInput()
		return recv.decode('utf-8')
		
	def recv(self, cycle=0.1, timeout=0.5, ctimeout=0):
		wait_time = 0#等待次数
		curr_size = 0#当前数据大小
		save_data = ''#收到的数据
		wait_max = timeout*10#最多等待次数
		cwait= ctimeout*(1/cycle)
		while True:
			if ctimeout !=0 and cwait==0:
				return -1
			elif ctimeout !=0:
				cwait = cwait - 1
			size = self.pyserial_test.inWaiting()
			if size != 0:
				curr_size = size#当前数据大小
				while True:
					if wait_time >= wait_max :#如果等待次数超过最多等待次数就返回数据
						if size != 0:#返回数据前将缓冲区的数据接收
							save_data = save_data + self.pyserial_test.read(size).decode('utf-8')
						return save_data
					if size >= 58:#当缓冲区的数据大于58字节时接收数据
						save_data = save_data + self.pyserial_test.read(size).decode('utf-8')
						curr_size = size = self.pyserial_test.inWaiting()
						wait_time = 0
						continue
					if size == curr_size:#如果没有接到新数据，则等待次数加一
						wait_time = wait_time + 1
					#print('wt%d wm%d s%d cs%d rs%d'%(wait_time, wait_max, size, curr_size, recv_size))
					time.sleep(0.05)
					size = self.pyserial_test.inWaiting()
					if size != curr_size:#如果有新收到的数据，就更新等待次数
						curr_size = size
						wait_time = 0
			time.sleep(cycle)#如果没有收到数据就再等待一个周期
	def send(self, data):
		return self.pyserial_test.write(data.encode('utf-8'))
	def sendb(self, data):
		return self.pyserial_test.write(data)