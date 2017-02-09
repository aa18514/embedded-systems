from machine import Pin, I2C
import utime
import ustruct as struct
import networks
import json

class i2c(): 
	def __init__(self, Pin1, Pin2, frequency): 
		self.__ic =  I2C(scl = Pin(Pin1), sda = Pin(Pin2), freq = frequency)
		self.__slave_address = self.__ic.scan()

	def enable_test_mode(self): 
		self.__ic.writeto_mem(self.__slave_address[0], 2, b"\x00")
	
	def update_x(self, x_msb, x_lsb):
		self.__x = struct.unpack('>h', x_msb + x_lsb)[0]

	def update_z(self, z_msb, z_lsb):
		self.__z = struct.unpack('>h', z_msb + z_lsb)[0]
	
	def update_y(self, y_msb, y_lsb):
		self.__y = struct.unpack('>h', y_msb + y_lsb)[0]
	
	def update_magnitude(self): 
		self.__magnitude = (self.__x**2 + self.__y**2 + self.__z**2)**0.5

	def start_recieving_data(self): 
		data = [0]*13
		while True:	#should change this later 
			for i in range(0, 13):
				data[i] = self.__ic.readfrom_mem(self.__slave_address[0], i, 1) #second byte is the register address, third byte is the number of bytes read
			self.update_x(data[3], data[4])
			self.update_z(data[5], data[6])
			self.update_y(data[7], data[8])
			self.update_magnitude()
			message = self.__magnitude
			print(message)
			utime.sleep(1)

if __name__ == "main":
	"""get data from sensor and prepare 
	packet for transmission and publish it"""
	IC = i2c(5, 4, 50000)  
	IC.enable_test_mode()
	IC.start_recieving_data()
