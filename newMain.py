from machine import Pin, I2C 
import utime 
import json 
from clock import *
import ustruct as struct
from ubinascii import hexlify
from newMqtt import * 

ENTER = b'13' 
class i2c():
	def __init__(self, Pin1, Pin2, frequency):
		self.__ic =  I2C(scl = Pin(Pin1), sda = Pin(Pin2), freq = frequency)
		self.__slave_address = self.__ic.scan()[0]

	def set_mode(self, value):
		self.__ic.writeto_mem(self.__slave_address, 2, value)

	def set_gain(self, value):
		self.__ic.writeto_mem(self.__slave_address, 1, value)

	"""Need to
		set frequency of register updates
		set average number of samples
		set neasurement mode """

	def set_measurement_mode(self, value):
		self.__ic.writeto_mem(self.__slave_address, 0, value)

	def read_data (self):
		self.__data = self.__ic.readfrom_mem(self.__slave_address,3,6)
		self.__x = struct.unpack('>h', self.__data[0:2])[0]
		self.__y = struct.unpack('>h', self.__data[2:4])[0]
		self.__z = struct.unpack('>h', self.__data[4:6])[0]


IC = i2c(5, 4, 50000)
net = Network('192.168.0.10', 'asdid')
net.init_wlan_and_client()	
net.recieve_message(b"esys/time")
CLK = Clock(json.loads(net.__msg)['date'])
net.publish(json.dumps("device turned on"))
print("device turned on")
utime.sleep_ms(6)


while True: 
	net.recieve_message(b"esys/asad/")
	if(net.__msg == ENTER): #test mode
		IC.set_measurement_mode(b"\x71") # positive test mode
		IC.set_gain(b"\xA0") #gain = 5
		IC.set_mode(b"\x00") #continious mode 
		n = 0
		while n < 20: 
			IC.read_data()
			net.publish(json.dumps(hexlify(IC.__data)))
			time = CLK.get_time()
			print(time) 
			n += 1
			print(str(IC.__x) + " " + str(IC.__y) + " " +  str(IC.__z))
			utime.sleep_ms(70)
		
	if(net.__msg == T): 
		IC.set_measurement_mode(b"\x70") #normal mode at 15 Hz 
		IC.set_gain(b"\xA0")
		IC.set_mode(b"\x00")
		while True: 
			IC.read_data() 
			net.publish(json.dumps(hexlify(IC.__data)))
			time = CLK.get_time() 
			print(time)
			print(str(IC.__x) + " " + str(IC.__y) + " " + str(IC.__z))
			utime.sleep_ms(70)