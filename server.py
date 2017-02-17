import paho.mqtt.client as mqtt
import time
import struct
import json  
import logging
import argparse
from msvcrt import getch
from threading import Thread 

class magnetic_flux(Thread): 
	def __init__(self, mqttc):
		super(magnetic_flux, self).__init__()
		self.__count = 0 
		self.__mqttc = mqttc
		self.__turned_on = False
		self.__publish_id = 'esys/unnamed1/'
		
	def run(self): 
		while True:
			if(self.__turned_on == True):
				key = ord(getch()) #wait for a key press 
				if key == 13 or (key == 116 and self.__count == 0): #if key press is enter
					self.__mqttc.publish(self.__publish_id, str(key))		
				else: 
					logging.warning('entered incorrect key')

	def recieve_payload(self, topic, userdata, msg):  
		self.__turned_on = True
		print(msg.payload)
		if(msg.payload == "Device turned on"):
			self.__count += 1
		if(msg.payload == "Device turned off"):
			self.__count -= 1
		logging.info('device turned on: %s' % str(self.__count))


if __name__ == "__main__":
	desc = ("utiltiy to detect active number of devices"
	"currently there are two modes, the user should press"
	"the character T if he wants to enter the test mode"
	"and the Enter key if he wants to enter into continious" 
	"mode test mode can be performed multiple times only"
	 "at device start-up")
	parser = argparse.ArgumentParser(formatter_class = argparse.RawDescriptionHelpFormatter, description = desc)
	parser.add_argument('-v', '--verbose', action='count', help = "varying output verbosity")
	args = parser.parse_args()
	if args.verbose == None: 
		loglevel = logging.WARNING
	elif args.verbose == 1:
		loglevel = logging.INFO 
	else:
		loglevel = logging.DEBUG 
	logging.basicConfig(filename = 'device.log',  format = '%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filemode = 'w', level=loglevel)
	mqttc = mqtt.Client()
	mqttc.connect('192.168.0.10', 1883, 60) 
	mqttc.subscribe('esys/asd/')
	mf = magnetic_flux(mqttc)
	mf.start()
	mqttc.on_message = mf.sub_cb 
	mqttc.loop_forever() 
	mf.join()