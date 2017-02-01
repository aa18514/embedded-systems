from machine import Pin, I2C
import utime
import ustruct as struct

def construct(data_1, data_2):
	return bytearray(data_1 + data_2)

def write_data(x, y, z):
	write(x, "x-coordinate: ")
	write(y, "y-coordinate: ")
	write(z, "z-coordinate: ")

def write(data, label): 
	print(label + "{}\n".format(struct.unpack('>h', data)[0]))

if __name__ == "main":
	i2c = I2C(scl = Pin(5), sda = Pin(4), freq = 500000)
	slave_address = i2c.scan() 
	number_of_bytes = 1 
	data = [0]*13
	i2c.writeto_mem(slave_address[0], 2, b"\x00") #enable test mode
	while True:
		for i in range(0, 13):
			data[i] = i2c.readfrom_mem(slave_address[0], i, number_of_bytes) #second byte is the register address, third byte is the number of bytes read
		write_data(x = construct(data[3], data[4]), y = construct(data[5], data[6]), z = construct(data[7], data[8]))
		utime.sleep(1)
