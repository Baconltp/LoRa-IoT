from lorapi2 import Lora
import time
import threading
import paho.mqtt.client as mqtt
import json
import queue
#!/usr/bin/python
'''
作用：
连接服务器和终端，转发服务器及终端的数据和指令
依赖：
paho-mqtt lorapi2
'''


lora = Lora()
msgque = queue.Queue()
dev_list = ''
check_delay = 600

#温度0 湿度1 光照强度2 人体红外3 雨滴4 板a电量5 土壤湿度6 水位7 盐碱性8 水泵状态9 板b电量10
#{'target':'gateway', 'msg':'getinfo', 'data':'12345'}  


def proc_data():
	#处理任务的主函数
	#此函数会从任务队列中取出一个任务。同时只会执行一个任务。
	while True:
		data = msgque.get()
		print('p-',data)
		#获取终端信息
		if data['msg'] == 'getinfo':
			#获取终端传感器信息
			#板a和板b都有传感器，先获取板a再获取板b
			msg = {'t':'a', 'msg':'getinfo'}#板a 土壤湿度0 水位1 水滴2 人体红外3 
			lora.send('{"t": "a", "msg": "getinfo"}')
			time.sleep(0.5)
			recv = lora.recv(ctimeout=20)
			#发送请求后等待20秒，若20秒后仍未收到数据，判断接收失败。
			print(recv)
			#=====================================================
			try:
				recv = json.loads(recv)
				#若json解析失败，也判断接收失败
			except:
				msg = {'target':'server', 'msg':'error_a', 'data':recv}
				msg = json.dumps(msg)
				client1.publish("iot", payload=msg.encode('utf-8'), qos=2)
				print("err_a", recv)
				continue
			data = recv['msg']
			time.sleep(2)
			#土壤湿度0 水位1 水滴2 人体红外3 温度4 湿度5 光照强度6  遮光帘状态7  水泵状态8
			print("getb")

			msg = {'t':'b', 'msg':'getinfo'}#板b  温度4 湿度5 光照强度6  遮光帘状态7  水泵状态8
			lora.send('{"t": "b", "msg": "getinfo"}')
			time.sleep(0.5)
			recv = lora.recv(ctimeout=20)
			print(recv)
			#=====================================================
			try:
				recv = json.loads(recv)
			except:
				msg = {'target':'server', 'msg':'error_b', 'data':recv}
				msg = json.dumps(msg)
				client1.publish("iot", payload=msg.encode('utf-8'), qos=2)
				print("err_b", recv)
				continue
			data = data + recv['msg']
			#温度0 光照1 土壤湿度2 湿度3 水位4 雨滴5 人体红外6 
			msg = {'target':'server', 'msg':'devinfo', 'data':[data[4], data[6], data[0], data[5], data[1], data[2], data[3], 0, 0, 0]}
			msg = json.dumps(msg)
			client1.publish("iot", payload=msg.encode('utf-8'), qos=2)
			time.sleep(0.5)
			#data = {'t':'gw', 'msg':[20, 80, 10, 0, 0]}
		#更改自动检查终端时间间隔
		#关闭灯
		elif data['msg'] == 'offlight':
			msgb = {'t':'b', 'msg':'closel'}
			lora.send(json.dumps(msgb))

			recv = lora.recv(ctimeout=20)
			#=====================================================
			try:
				recv = json.loads(recv)
			except:
				msg = {'target':'server', 'msg':'error_b', 'data':recv}
				msg = json.dumps(msg)
				client1.publish("iot", payload=msg.encode('utf-8'), qos=2)
				continue
			msg = json.dumps({'target':'server', 'msg':recv['msg']})
			client1.publish("iot", payload=msg.encode('utf-8'), qos=2)
			time.sleep(1)
		#打开灯
		elif data['msg'] == 'onlight':
			msgb = {'t':'b', 'msg':'openl'}
			lora.send(json.dumps(msgb))
			recv = lora.recv(ctimeout=20)
			try:
				recv = json.loads(recv)
			except:
				msg = {'target':'server', 'msg':'error_b', 'data':recv}
				msg = json.dumps(msg)
				client1.publish("iot", payload=msg.encode('utf-8'), qos=2)
				continue
			msg = json.dumps({'target':'server', 'msg':recv['msg']})
			client1.publish("iot", payload=msg.encode('utf-8'), qos=2)
			time.sleep(1)
		#关闭水泵
		elif data['msg'] == 'closepump':
			msgb = {'t':'b', 'msg':'closep'}
			lora.send(json.dumps(msgb))
			lora.recv()
			recv = lora.recv(ctimeout=20)
			#=====================================================
			try:
				recv = json.loads(recv)
			except:
				msg = {'target':'server', 'msg':'error_b', 'data':recv}
				msg = json.dumps(msg)
				client1.publish("iot", payload=msg.encode('utf-8'), qos=2)
				continue
			msg = json.dumps({'target':'server', 'msg':recv['msg']})
			client1.publish("iot", payload=msg.encode('utf-8'), qos=2)
			time.sleep(1)
		#打开关闭帘子
		elif data['msg'] == 'openm1':
			lora.send('{"t": "b", "msg": "openmotor"}')
		elif data['msg'] == 'closem1':
			lora.send('{"t": "b", "msg": "closemotor"}')


		elif data['msg'] == 'openm2':
			lora.send('{"t": "b", "msg": "shelterdown"}')
		elif data['msg'] == 'closem2':
			lora.send('{"t": "b", "msg": "shelterup"}')


		#打开水泵
		elif data['msg'] == 'openpump':
			msgb = {'t':'b', 'msg':'openp'}
			lora.send(json.dumps(msgb))
			lora.recv()
			recv = lora.recv(ctimeout=20)
			try:
				recv = json.loads(recv)
			except:
				msg = {'target':'server', 'msg':'error_b', 'data':recv}
				msg = json.dumps(msg)
				client1.publish("iot", payload=msg.encode('utf-8'), qos=2)
				continue
			msg = json.dumps({'target':'server', 'msg':recv['msg']})
			client1.publish("iot", payload=msg.encode('utf-8'), qos=2)
			time.sleep(1)
'''
        #终端lora模块 省电模式
        elif data['msg'] == 'powerSave':
            lora.send('powerSave')
            time.sleep(1)
        elif data['msg'] == 'check_dev':
            dect_device()
            time.sleep(1)
        #唤醒终端lora模块
        elif data['msg'] == 'awake':
			lora.awake()
			time.sleep(0.1)
			lora.send('awake')
			time.sleep(1)
			lora.normal()
'''
def on_message(client, userdata, msg):
	#当收到mqtt消息时，此函数执行。
	global check_delay
	data = msg.payload.decode()
	try:
		data = json.loads(data)
	except:
		print('%s msg load err:%s'%(time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time())), data))
	if data['target'] == 'gateway':
		#当target为gateway时处理，否则丢弃
		if data['msg'] == 'check_interval':
			check_delay = data['data']
			print('check_interval', check_delay)
		elif data['msg'] == 'getque':
			msgs = {'target':'server', 'msg':'quesize', 'data':msgque._qsize()}
			client1.publish("iot", payload=json.dumps(msgs).encode('utf-8'), qos=2)
		else:
			msgque.put(data)
			#将耗时请求扔进队列

def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))
init_time = time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time()))

client1 = mqtt.Client('rspi_gateway'+init_time)
client1.username_pw_set(username="admin",password="password")#mqtt账号密码
client1.on_connect = on_connect
client1.connect("47.103.128.205", 31313, 60)#mqtt服务器地址及端口
time.sleep(1)
client1.subscribe("iot")
client1.on_message = on_message

def dect_device(report=1):
	global dev_list
	lora.send('dect')
	dev_list = lora.recv()
	dev_list = lora.recv(ctimeout=40, timeout=10)
	print(dev_list)
	if dev_list == -1:
		dev_list = ''
	if report==1:
		msg = {'target':'server', 'msg':'device_dect', 'data':dev_list}
		msg = json.dumps(msg)
		client1.publish("iot", payload=msg.encode('utf-8'), qos=2)
	return dev_list

def auto_check():
	while True:
		time.sleep(check_delay)
		msg = {'msg':'check_dev'}
		msgque.put(msg)
        


dect_device()
print(dev_list)
th1 = threading.Thread(target=proc_data)
th1.start()
th_autocheck = threading.Thread(target=auto_check)
th_autocheck.start()
client1.loop_forever()
