from machine import Pin, I2C
import utime
import ubinascii import hexlify

if __name__ == "main":
	i2c = I2C(scl = Pin(5), sda = Pin(4), freq = 500000)
	slave_address = i2c.scan(); 
	number_of_bytes = 4; 
	while True:
		for i in range(0, 13):
			data[i] = hexlify(i2c.readfrom_mem(slave_address[0], i, number_of_bytes)) #read the values of all the available registers and store them
		print(str(data))
		utime.sleep(5)
		
