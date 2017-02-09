from machine import Pin, I2C
import utime
import ustruct as struct
import networks
import json

class i2c(): 
	def __init__(self, Pin1, Pin2, frequency): 
		self.__ic =  I2C(scl = Pin(Pin1), sda = Pin(Pin2), freq = frequency)
		self.__slave_address = self.__ic.scan()

	def construct(self, data_1, data_2):
		"""concatanate MSB and LSB"""
		print(data_1)
		print(data_2)
		print(data_1 + data_2)
		return bytearray(data_1 + data_2)

	def write_data(self, x, y, z):
		return self.prepare_message(x, "x-coordinate: ") + self.prepare_message(y, "z-coordinate: ") + self.prepare_message(z, "y-coordinate: ")
		return message

	def prepare_message(self, data, label):
		"""interpret data as an 
		signed integer"""
		message = label + "{}\n".format(struct.unpack('>h', data)[0])
		print(message)
		return message 

	def enable_test_mode(self): 
		self.__ic.writeto_mem(self.__slave_address[0], 2, b"\x00")
	
	def start_recieving_data(self): 
		data = [0]*13
		while True:	#should change this later 
			for i in range(0, 13):
				data[i] = self.__ic.readfrom_mem(self.__slave_address[0], i, 1) #second byte is the register address, third byte is the number of bytes read
			x_msb = data[3] 
			x_lsb = data[4] 
			z_msb = data[5] 
			z_lsb = data[6]
			y_msb = data[7] 
			y_lsb = data[8] 
			message = self.write_data(self.construct(x_msb, x_lsb), self.construct(z_msb, z_lsb), self.construct(y_msb, y_lsb))
			print(json.dumps(message))
			utime.sleep(1)

if __name__ == "main":
	"""get data from sensor and prepare 
	packet for transmission and publish it"""
	IC = i2c(5, 4, 50000)  
	IC.enable_test_mode()
	IC.start_recieving_data()
