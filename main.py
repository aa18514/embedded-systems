from machine import Pin, I2C

i2c = I2C(scl = Pin(5), sda = Pin(4), freq = 100000)
available_address = i2c.scan(); 
number_of_bytes = 1; 
while(True):
	print("i2c.readfrom(available_address, number_of_bytes)")