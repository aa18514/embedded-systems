import network
import machine
from umqtt.simple import MQTTClient

def init_wlan_and_client(ip_address, id): 
	"""initialize the wireless network
	and set up the client with the appropiate 
	ip_address and id"""
	ap_if = network.WLAN(network.AP_IF)
	ap_if.active(False)
	sta_if =network.WLAN(network.STA_IF)
	sta_if.active(True)
	sta_if.connect('EEERover','exhibition')
	while not sta_if.isconnected(): #block until the we are connected to the internet
		pass
	client = MQTTClient(id,ip_address)
	return client

def connect_client(client, host_address, message):
	client.publish(host_address ,bytes(message,'utf-8'))

def connect():
	client = init_wlan_and_client('192.168.0.10','asdid')
	client.connect()
	publish_data(client, "esys/asd", bytes('helloooo'), 'utf-8')