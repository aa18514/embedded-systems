from machine import Pin, I2C 
import utime 
import json 
from clock import *
import ustruct as struct
from mqtt import * 

ENTER = b'13' 
T = b'116'
class i2c():
	def __init__(self, Pin1, Pin2, frequency):
		self.__ic =  I2C(scl = Pin(Pin1), sda = Pin(Pin2), freq = frequency)
		self.__slave_address = self.__ic.scan()[0]

	def set_measurement_mode(self, value):
		self.__ic.writeto_mem(self.__slave_address, 0, value)

	def set_gain(self, value):
		self.__ic.writeto_mem(self.__slave_address, 1, value)

	def set_mode(self, value):
		self.__ic.writeto_mem(self.__slave_address, 2, value)
		
	def read_data (self):
		self.__data = self.__ic.readfrom_mem(self.__slave_address,3,6)
		self.__x = struct.unpack('>h', self.__data[0:2])[0]
		self.__y = struct.unpack('>h', self.__data[2:4])[0]
		self.__z = struct.unpack('>h', self.__data[4:6])[0]
		self.__magMilliGauss = (((self.__x)**2 + (self.__z)**2 + (self.__y)**2)**0.5)*0.92  #for gain = 1

IC = i2c(5, 4, 50000)
net = Network('192.168.0.10', 'asdid', 60)
net.init_wlan_and_client()	
net.recieve_message(b"esys/time")
CLK = Clock(json.loads(net.__msg)['date'])
net.publish("device turned on")
print("device turned on")

while True:
	printCmd = "Print 'Enter' to start getting data, 't' to run test sensor"
	net.publish(printCmd)
	net.recieve_message(b"esys/unnamed1/")
	if(net.__msg == T): #test mode
		IC.set_measurement_mode(b"\x71") # positive test mode
		IC.set_gain(b"\xA0") #gain = 5
		IC.set_mode(b"\x00") #continious mode
		upperLimit = 243	#from data sheet for gain 5
		lowerLimit = 575
		testStatus = "Pass, sensor is working properly" 	
		for n in range(0,20): 
			IC.read_data()
			if (243 < IC.__x < 575 and 243 < IC.__z < 575 and 243 < IC.__y < 575):
				pass
			else:
				testStatus = "Fail, sensor is faulty"	
		utime.sleep_ms(67)

		print(testStatus)
		print(printCmd)
		net.publish(testStatus)
		net.publish(printCmd)
			
	elif(net.__msg == ENTER):
		print("getting data")
		net.publish("getting data") 
		IC.set_measurement_mode(b"\x70") #normal mode at 15 Hz 
		IC.set_gain(b"\x20")
		IC.set_mode(b"\x00")
		utime.sleep_ms(6)
		turnedOff = True
		oldMag = 0
		#midMag1 = 0
		midMag2 = 0
		while True: 	
			magnitudeSum = 0 
			for n in range(0,3):
				IC.read_data() 
				magnitudeSum += IC.__magMilliGauss
				utime.sleep_ms(1500)

			magAvg = magnitudeSum/3
			time = CLK.get_time()			

			if(oldMag is not 0):
				if (turnedOff == True and magAvg - oldMag > 60):
					turnedOff = False
					net.publish("Device turned on")
					net.publish(time)
				elif (turnedOff == False and magAvg - oldMag < -60):
					turnedOff = True
					net.publish("Device turned off")
					net.publish(time)
			oldMag = midMag2
			#midMag2 = midMag1
			midMag2 = magAvg
			
			outputstream = "{}".format("magAvg: " + str(magAvg) + " milli gauss")
			print(outputstream)
			print(str(IC.__x) + " " + str(IC.__z) + " " + str(IC.__y) + "\n" )
			#net.publish(outputstream)
