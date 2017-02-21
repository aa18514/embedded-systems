A smart homes solution that presents the power comsumption of the appliance in home

The files main.py mqtt.py and clock.py are run on the huzzah feather.
	The code takes raw data from the sensor, detects if appliance is turned on or off
	and publishes it on the mqtt broker

The file server.py subcribers to the mqtt broker and store the relevent published data.
	The stored data includes the time when an appliance was turned on and off.
	The data can be used to visual the usage of the appliance over some period of time

The code shows a proof of concept that the provided sensor can detect if an appliance is turned on or off.

Future works include
	further calculations on the threshold used in main.py
	using the readings to approximate the value of current
	adding a gui for server.py 