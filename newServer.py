import paho.mqtt.client as mqtt 
import time
import struct 
from datetime import datetime

class magnetic_flux(): 
	def __init__(self):
		self.__x = 0 
		self.__y = 0 
		self.__z = 0 
		
	def update_magnitude(self):
		self.__magnitude = (self.__x**2 + self.__y**2 + self.__z**2)**0.5

	def update_x(self, data):
		self.__x = struct.unpack('>h', data)[0]

	def update_z(self, data):
		self.__z = struct.unpack('>h', data)[0]

	def update_y(self, data):
		self.__y = struct.unpack('>h', data)[0]

	def sub_cb(self, topic, userdata, msg): 
		self.decode(msg.payload)

	def decode(self, data):
		self.update_x(data[0:2])
		self.update_z(data[2:4])
		self.update_y(data[4:6])
		self.update_magnitude() 
		msg = "{}\n".format(str(datetime.now()) + ',' + str(self.__magnitude)) #write this to csv file  
		print(msg)

if __name__ == "__main__":
	mqttc = mqtt.Client()
	mf = magnetic_flux()  
	mqttc.on_message = mf.sub_cb 
	mqttc.connect('192.168.0.10', 1883, 4) 
	mqttc.subscribe('esys/asd/')
	mqttc.loop_forever() 