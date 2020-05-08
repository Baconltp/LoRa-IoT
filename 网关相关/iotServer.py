#!/usr/bin/env python
#coding:utf-8

import tornado.ioloop
import tornado.web
import paho.mqtt.client as mqtt
import threading
import json
import time

'''
本代码的作用：
创建API供外部调用，调用后，可以在mqtt里发送特定信息给网关。
目前实现的功能：
打开水泵，关闭水泵，开灯，关灯，开上帘子，关上帘子，
开侧帘子，关侧帘子，获取终端传感器信息。
使用方法：
运行本代码后，程序会监听6001端口，假设服务器ip为10.0.1.1，
访问http://10.0.1.1:6001/openpump ，会发送一个mqtt消息给网关，执行打开水泵操作。
http://10.0.1.1:6001/openpump
http://10.0.1.1:6001/closepump
http://10.0.1.1:6001/onlight
http://10.0.1.1:6001/offlight
http://10.0.1.1:6001/openm1
http://10.0.1.1:6001/openm2
http://10.0.1.1:6001/closem1
http://10.0.1.1:6001/closem2
http://10.0.1.1:6001/getinfo
依赖：
tornado  paho-mqtt
'''
mqtthost = "192.168.1.1"#mqtt服务器地址
mqttport = 31313#mqtt服务器端口
client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
mqtt_username = "admin"#用户名
mqtt_pw = "password"#密码

class nullHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("hello world")
	
class setyzHander(tornado.web.RequestHandler):
	def get(self):
		self.set_header("Access-Control-Allow-Origin", "*")
		airtem = self.get_argument("airtem")
		light = self.get_argument("light")
		soilhum = self.get_argument("soilhum")
		water = self.get_argument("water")
		airhum = self.get_argument("airhum")
		raindrop = self.get_argument("raindrop")
		body = self.get_argument("body")
		self.write(airhum+light+soilhum+water+airhum+raindrop+body)
class openm1Handler(tornado.web.RequestHandler):
	def get(self):
		client.publish("iot", payload='{"target": "gateway", "msg": "openm1"}', qos=0)
		self.set_header("Access-Control-Allow-Origin", "*")
		self.write("done.")
class closem1Handler(tornado.web.RequestHandler):
	def get(self):
		client.publish("iot", payload='{"target": "gateway", "msg": "closem1"}', qos=0)
		self.set_header("Access-Control-Allow-Origin", "*")
		self.write("done.")
class openm2Handler(tornado.web.RequestHandler):
	def get(self):
		client.publish("iot", payload='{"target": "gateway", "msg": "openm2"}', qos=0)
		self.set_header("Access-Control-Allow-Origin", "*")
		self.write("done.")
class closem2Handler(tornado.web.RequestHandler):
	def get(self):
		client.publish("iot", payload='{"target": "gateway", "msg": "closem2"}', qos=0)
		self.set_header("Access-Control-Allow-Origin", "*")
		self.write("done.")
class openpumpHandler(tornado.web.RequestHandler):
	def get(self):
		client.publish("iot", payload='{"target": "gateway", "msg": "openpump"}', qos=0)
		self.set_header("Access-Control-Allow-Origin", "*")
		self.write("done.")
class closepumpHandler(tornado.web.RequestHandler):
	def get(self):
		client.publish("iot", payload='{"target": "gateway", "msg": "closepump"}', qos=0)
		self.set_header("Access-Control-Allow-Origin", "*")
		self.write("done.")
class onlightHandler(tornado.web.RequestHandler):
	def get(self):
		client.publish("iot", payload='{"target": "gateway", "msg": "onlight"}', qos=0)
		self.set_header("Access-Control-Allow-Origin", "*")
		self.write("done.")

class offlightHandler(tornado.web.RequestHandler):
	def get(self):
		client.publish("iot", payload='{"target": "gateway", "msg": "offlight"}', qos=0)
		self.set_header("Access-Control-Allow-Origin", "*")
		self.write("done.")
class getinfoHander(tornado.web.RequestHandler):
	def get(self):
		client.publish("iot", payload='{"target": "gateway", "msg": "getinfo"}', qos=0)
		time.sleep(3)
		self.set_header("Access-Control-Allow-Origin", "*")
		self.write("done.")



settings = {#html文件归类配置，设置一个字典
	"template_path":"views",#键为template_path固定的，值为要存放HTML的文件夹名称
	"static_path":"statics",#键为static_path固定的，值为要存放js和css的文件夹名称
}

#路由映射
application = tornado.web.Application([#创建一个变量等于tornado.web下的Application方法
    (r"/", nullHandler),
	(r"/openpump", openpumpHandler),
	(r"/closepump", closepumpHandler),
	(r"/onlight", onlightHandler),
	(r"/offlight", offlightHandler),
	(r"/openm1", openm1Handler),
	(r"/openm2", openm2Handler),
	(r"/closem1", closem1Handler),
	(r"/closem2", closem2Handler),
	(r"/getinfo", getinfoHander)

],**settings)#将html文件归类配置字典，写在路由映射的第二个参数里

def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))

def on_message(client, userdata, msg):
	data = msg.payload.decode()
	print(client,userdata, data)

client = mqtt.Client(client_id)
client.username_pw_set(username=mqtt_username,password=mqtt_pw)
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtthost, mqttport, 60)
time.sleep(1)#这1s一定要加
client.subscribe("iot")
def getinfo_thread():
	time.sleep(30)
	client.publish("iot", payload='{"target": "gateway", "msg": "getinfo"}', qos=0)
	time.sleep(300)

def mqtt_thread(mqtt_client):
	mqtt_client.loop_forever()

if __name__ == "__main__":
	application.listen(port=6001,address="0.0.0.0")#设置端口
	th1  = threading.Thread(target=mqtt_thread, args=(client, ))
	th1.start()
	th2 = threading.Thread(target=getinfo_thread)
	th2.start()
	tornado.ioloop.IOLoop.instance().start()