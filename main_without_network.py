from machine import Pin, I2C, RTC
import utime
from mqtt import *
import json
from clock import Clock  
import ustruct as struct

class i2c():
	def __init__(self, Pin1, Pin2, frequency):
		self.__ic =  I2C(scl = Pin(Pin1), sda = Pin(Pin2), freq = frequency)
		self.__slave_address = self.__ic.scan()[0]
		self.__data = [0]*6
		self.__magnitude = 0 

	def set_mode(self, num):
		self.__mode = bytes(num)

	def positive_self_test_measurement(self):
		self.__ic.writeto_mem(self.__slave_address, 0, b"\x70")

	def set_gain(self):
		self.__ic.writeto_mem(self.__slave_address, 1, b"\x20")
	
	def write_mode(self):
		self.__ic.writeto_mem(self.__slave_address, 2, b"\x00")

	def enable_test_mode(self):
		"""8-average, 15 default, 
		positive self - test measurement
		Gain = 5, Continious measurement 
		mode"""
		self.positive_self_test_measurement()
		self.set_gain()
		self.write_mode()
		utime.sleep_ms(6)

	def update_gain(self, num):
		"""defining boundaries for x, 
		y and z coordinates respectively"""
		self.__upper_limit = 1370.82 - 147.4*num
		self.__lower_limit = 579.39  - 062.3*num
		self.__gain = bytes([num << 5]) 

	
	def update_magnitude(self):
		self.__magnitude = (self.__x**2 + self.__y**2 + self.__z**2)**0.5

	def update_x(self, data):
		self.__x = struct.unpack('>h', data)[0]

	def update_z(self, data):
		self.__z = struct.unpack('>h', data)[0]

	def update_y(self, data):
		self.__y = struct.unpack('>h', data)[0]


	def start_recieving_data(self):
		while True:	
			self.__data = self.__ic.readfrom_mem(self.__slave_address, 3, 6) 
			self.update_x(self.__data[0:2])
			self.update_y(self.__data[2:4])
			self.update_z(self.__data[4:6])
			m = (self.__x**2 + self.__y**2 + self.__z**2)**0.5
			print(str(self.__x) + " " + str(self.__y) + " " + str(self.__z))
			print("magnitude: " + str(m))
			if(self.__magnitude is not 0):
				if(abs(m - self.__magnitude) > 100): 
					msg = "device connected: "
					print(msg)
			self.__magnitude = m 
			utime.sleep_ms(2000)
	
IC = i2c(5, 4, 50000)
IC.update_gain(2)
IC.set_mode(0)
IC.enable_test_mode()
IC.start_recieving_data()
