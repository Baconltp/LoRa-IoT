import pyb
from pyb import Pin
from pyb import Timer
from pyb import UART
from pyb import I2C  
import micropython
#import showdata
from lora import Lora
lora = Lora()
import moisture
import WaterLevel
import time
import json
from DHT12 import DHT12
import security
import LightIntensity
dht = DHT12('X1')


p_in = Pin('X12',Pin.IN,Pin.PULL_UP)

adc = pyb.ADC(Pin('X11'))
adc = pyb.ADC(pyb.Pin.board.X11)

def rainfallAo():
	return adc.read()

def getRainDO():
	return p_in.value


while True:
	data = lora.recv()
	print(data)
	if data == 'dect':#响应心跳包，收到'dect'时延迟550毫秒回复'a'
		pyb.delay(550)
		lora.send('a')
		print('a')
		continue
	elif data == 'a' or data == 'b':#收到别的设备发出的心跳包时不回复
		continue
	elif data == 'awake':#暂时废弃
		#lora.normal()
		print('b awake')
		continue
	elif data == 'powerSave':#暂时废弃
		#lora.powerSave()
		print('b powerSave')
		continue
	try:
		data = json.loads(data)
		#收到正常的指令，指令应是json格式的
		#{"t":"a","msg":"getinfo"}
		#其中t代表目标，上面示例中，目标是a，板a会接收，若b板收到，会直接丢弃
		#但是这种方法不好。连续接到两个指令时，数据会像这样
		#{"t":"a","msg":"getinfo"}{"t":"b","msg":"getinfo"}
		#导致json解析错误
	except:
		print('error', data)
		continue
	print(data['t'] == 'a')
	if data['t'] == 'a' :
		#data = {'t':'gw', 'msg':[20, 80, 10, 1]}
		#板a 土壤湿度0 水位1 水滴2 人体红外3 空气温度4 空气湿度5 光照强度6
		wet = moisture.getMoisAo()
		waterlev = WaterLevel.getWaterLevel()
		waterdrop = rainfallAo()
		security = security.detectMotion()
		#temp,hum = dht.read_temp_hum()
		temp,hum = error,error
		#lightintensity = LightIntensity.readLight()
		lightintensity=error
		#上面两个传感器有时不能及时返回数据，导致网关认为板a已经挂了
		msggw = {'t':'gw', 'msg':[wet, waterlev , waterdrop, security, temp, hum, lightintensity]}
		print(msggw)
		lora.send(json.dumps(msggw))
		#将数据发回网关
    
