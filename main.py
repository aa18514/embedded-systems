from machine import Pin, I2C
import time

if __name__ == "main":
	i2c = I2C(scl = Pin(5), sda = Pin(4), freq = 500000)
	available_address = i2c.scan(); 
	number_of_bytes = 4; 
	while True:
		print(i2c.readfrom(available_address[0], number_of_bytes))
		time.sleep(5)