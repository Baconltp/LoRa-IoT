import LightIntensity
import pyb
from pyb import Pin
from pyb import Timer
from pyb import UART  
import micropython
import Pump
from lora2 import Lora
import json
lora = Lora()
import DHT12
from DHT12 import DHT12
dht = DHT12('X1')

while True:
    data = lora.recv()
    if data == 'dect':
        pyb.delay(550)
        lora.send('b')
        print('b')
        continue
    elif data == 'awake':
        lora.normal()
        print('b awake')
        continue
    elif data == 'powerSave':
        lora.powerSave()
        print('b powerSave')
        continue
    try:
        data = json.loads(data)
    except:
        print('error', data)
        continue
    print(data)
    
    if data['t'] == 'b' and data['msg'] == 'openp':#打开水泵
        Pump.Pump_on()
        stat = Pump.getState()
        msggw = {'t':'gw', 'msg':[stat]}
        lora.send(json.dumps(msggw))
    elif data['t'] == 'b' and data['msg'] == 'closep':#关闭水泵
        Pump.Pump_off()
        stat = Pump.getState()
        msggw = {'t':'gw', 'msg':[stat]}
        lora.send(json.dumps(msggw))
		#将水泵状态返回给网关
    elif data['t'] == 'b' and data['msg'] == 'getinfo':#获取传感器数据 
        temp,hum = dht.read_temp_hum()
        lightintensity = LightIntensity.readlight()
        msggw = {'t':'gw', 'msg':[temp,hum,lightintensity]}
        print(msggw)
        lora.send(json.dumps(msggw))