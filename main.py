from machine import Pin, I2C, RTC
import utime
import ustruct as struct
import networks
import json

class i2c(): 
	def __init__(self, Pin1, Pin2, frequency): 
		self.__ic =  I2C(scl = Pin(Pin1), sda = Pin(Pin2), freq = frequency)
		self.__slave_address = self.__ic.scan()
	
	def set_mode(self, num):
		self.__mode = bytes(num) 
	
	def write_mode(self): 
		self.__ic.writeto_mem(self.__slave_address[0], 2, self.__mode)
	
	def set_gain(self):
		cmd = bytes(self.__gain << 5)
		self.__ic.writeto_mem(self.__slave_address[0], 1, cmd)
	
	def positive_self_test_measurement(self): 
		self.__ic.writeto_mem(self.__slave_address[0], 0, b"\x71")
	
	def enable_test_mode(self): 
		"""8-average, 15 default, positive self - test measurement
		Gain = 5, Continious measurement mode"""
		self.positive_self_test_measurement() 
		self.set_gain()
		self.continious_measurement_mode()
		utime.sleep_ms(6)
		
	def update_gain(self, num):
		self.__gain = num
	
	def update_x(self, data):
		self.__x = struct.unpack('>h', data)[0]

	def update_z(self, data):
		self.__z = struct.unpack('>h', data)[0]
	
	def update_y(self, data):
		self.__y = struct.unpack('>h', data)[0]
	
	def update_magnitude(self): 
		self.__magnitude = (self.__x**2 + self.__y**2 + self.__z**2)**0.5

	def start_recieving_data(self): 
		while True:	#should change this later 
			data = [0]*6
			data = self.__ic.readfrom_mem(self.__slave_address[0], 3, 6)
			self.update_x(data[0:2])
			self.update_z(data[2:4])
			self.update_y(data[4:6])
			self.update_magnitude()
			print(self.__x)
			print(self.__y)
			print(self.__z)
			self.update_magnitude()
			utime.sleep_ms(67)

if __name__ == "main":
	"""get data from sensor and prepare 
	packet for transmission and publish it"""
	IC = i2c(5, 4, 50000)  
	IC.update_gain(5)
	IC.set_mode(0) 
	IC.enable_test_mode()
	IC.start_recieving_data()
	
