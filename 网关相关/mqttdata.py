import paho.mqtt.client as mqtt
import threading
import json
import pymysql
import time
mqtthost = "127.0.0.1"
mqttport = 31313
client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
mqtt_username = "admin"
mqtt_pw = "password"

def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))
	#{'target':'server', 'msg':'devinfo', 'data':[]}



def on_message(client, userdata, msg):
	data = msg.payload.decode()
	print(client,userdata, data)
	data = json.loads(data)
	if data['target'] == 'server':
		if(data['msg'] == 'devinfo'):
			airtem = data['data'][0]
			light = data['data'][1]
			soilhum = data['data'][2]
			airhum = data['data'][3]
			water = data['data'][4]
			raindrop = data['data'][5]
			body = data['data'][6]
			print(1)
			db = pymysql.connect(host="127.0.0.1",user="yoursql",password="123456",database="kc_db",port=3306)
			print(2)
			cursor = db.cursor()
			print("INSERT INTO `kc_inf` VALUES (NOW());",airtem, light, soilhum, airhum, water, raindrop, body)
			cursor.execute('INSERT INTO `kc_inf` VALUES (NOW(), %f, %f, %f, %f, %f, %f, %f);'%(airtem, light, soilhum, airhum, water, raindrop, body))
			print(cursor.fetchall())
			db.commit()
			db.close()
			print(12)



client = mqtt.Client(client_id)
client.username_pw_set(username=mqtt_username,password=mqtt_pw)
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtthost, mqttport, 60)
time.sleep(1)#这1s一定要加
client.subscribe("iot")
client.loop_forever()