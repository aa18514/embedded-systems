from machine import Pin, I2C, RTC
import utime
import ustruct as struct
from netwoker import network 
import json
from clock import Clock  

class i2c():
	def __init__(self, Pin1, Pin2, frequency):
		self.__ic =  I2C(scl = Pin(Pin1), sda = Pin(Pin2), freq = frequency)
		self.__slave_address = self.__ic.scan()
		self.__continious_measurement_mode = 0
		self.__single_measurement_mode = 1
		self.__idle_mode1 = 2
		self.__idle_mode2 = 3

	def read_continious_measurement_mode(self):
		return self.__continious_measurement_mode

	def read_single_measurement_mode(self):
		return self.__single_measurement_mode

	def read_idle_mode(self):
		"""can be self.__idle_mode2 as well"""
		return self.__idle_mode1

	def set_mode(self, num):
		self.__mode = bytes(num)

	def write_mode(self, regAddress):
		self.__ic.writeto_mem(self.__slave_address[0], regAddress, b"\x00")

	def set_gain(self):
		cmd = self.__gain
		self.__ic.writeto_mem(self.__slave_address[0], 1, self.__gain)

	def positive_self_test_measurement(self):
		self.__ic.writeto_mem(self.__slave_address[0], 0, b"\x71")

	def enable_test_mode(self):
		"""8-average, 15 default, positive self - test measurement
		Gain = 5, Continious measurement mode"""
		self.positive_self_test_measurement()
		self.set_gain()
		self.write_mode(2)
		utime.sleep_ms(6)

	def update_gain(self, num):
		"""defining boundaries for x, y and z coordinates respectively"""
		self.__upper_limit = 1.474 * (930 - num*100)
		self.__lower_limit = 0.623 * (930 - num*100)
		self.__gain = bytes([num << 5])

	def update_x(self, data):
		self.__x = struct.unpack('>h', data)[0]

	def update_z(self, data):
		self.__z = struct.unpack('>h', data)[0]

	def update_y(self, data):
		self.__y = struct.unpack('>h', data)[0]

	def update_magnitude(self):
		self.__magnitude = (self.__x**2 + self.__y**2 + self.__z**2)**0.5

	def start_recieving_data(self, net):
		while True:	#should change this later
			data = [0]*6
			data = self.__ic.readfrom_mem(self.__slave_address[0], 3, 6)
			self.update_x(data[0:2])
			self.update_z(data[2:4])
			self.update_y(data[4:6])
			self.update_magnitude()
			#print(self.__x)
			#print(self.__y)
			#print(self.__z)
			#print("lower limit: " + str(self.__lower_limit))
			#print("upper limits: " + str(self.__upper_limit))
			net.publish(self.__x)
			utime.sleep_ms(67)

if __name__ == "main":
	"""get data from sensor and prepare
	packet for transmission and publish it"""
	IC = i2c(5, 4, 50000)
	net = Network('192.168.0.10', 'asdid')
	net.init_wlan_and_client()
	net.recieve_message() #recieve message from broker which contains the time 
	clk = Clock(net.retrieve_message())
	IC.update_gain(2)
	mode = IC.read_continious_measurement_mode()
	client = networker.connect()
	if(mode < 0 or mode > 4):
		print("invalid mode, please try again")
	else:
		IC.set_mode(mode)
		IC.enable_test_mode()
		IC.start_recieving_data(net)
