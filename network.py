import network
import machine
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)

sta_if =network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('EEERover','exhibition')
while not sta_if.isconnected():
	pass
print('true')
#else: print('false')

from umqtt.simple import MQTTClient
client = MQTTClient('asdid','192.168.0.10')
client.connect()
client.publish('esys/asd/',bytes('hellooooo','utf-8'))