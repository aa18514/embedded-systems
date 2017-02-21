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
		self.__mqttc = mqttc
		self.__turned_on = False

	def run(self): 
		self.__mqttc.on_message = self.recieve_payload 
		self.__mqttc.loop_forever()

	def recieve_payload(self, topic, userdata, msg):  
		json_formatted_msg = msg.payload.decode("utf-8")
		print(json_formatted_msg)
		if("device turned on" in json_formatted_msg): 
			self.__turned_on = True 
		elif(self.__turned_on is True):
			if( "Sensor" in json_formatted_msg): 
				logging.warning(json_formatted_msg)
			else: 
				logging.info(json_formatted_msg)


if __name__ == "__main__":
	desc = ("detects if the device is functioning correctly,\n"
	"and stores the when each device was turned on and off\n"
	"along with the timestamp\n")
	parser = argparse.ArgumentParser(formatter_class = argparse.RawDescriptionHelpFormatter, description = desc)
	parser.add_argument('-v', '--verbose', action='count', help = "varying output verbosity")
	args = parser.parse_args()
	loglevel = logging.WARNING
	if args.verbose == None: 
		loglevel = logging.WARNING
	else:
		loglevel = logging.INFO 
	logging.basicConfig(filename = 'device.log',  format = '%(message)s', filemode = 'w', level=loglevel)
	channels = [mqtt.Client(), mqtt.Client()]
	channels[0].connect('192.168.0.10', 1883, 60) 
	channels[0].subscribe('esys/SenSa/status')
	channels[1].connect('192.168.0.10', 1883, 60)
	channels[1].subscribe('esys/SenSa/reading')
	mf_1 = magnetic_flux(channels[0])
	mf_2 = magnetic_flux(channels[1])
	mf_1.start()
	mf_2.start() 
	mf_1.join()
	mf_2.join()