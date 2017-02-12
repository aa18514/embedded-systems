import network
import machine
import utime
from umqtt.simple import MQTTClient

class Network(): 
	def __init__(self, ip_address, id): 
		self.__ip_address = ip_address
		self.__network_id = id

<<<<<<< HEAD
def sub_cb(topic, msg):
    print((topic, msg))

def publish(client, message):
	payload = json.dumps(message)
	print(payload)
	client.publish(host_address, bytes(message, 'utf-8'))

def connect_client(client, host_address, message):
	client.publish(host_address ,bytes(message,'utf-8'))

def connect():
	client = init_wlan_and_client('192.168.0.10','asdid')
	client.set_callback(sub_cb)
	client.connect()
	cline.subsribe(b"time")
	huzzah = True
	while huzzah: 
		if True: 
			c.wait_msg()
		else: 
			c.check_msg() 
			huzzah = False
	return client
=======
	def sub_cb(self, topic, msg):
		print(msg)
		self.__msg = msg 

	def retrieve_message(self): 
		return self.__msg

	def init_wlan_and_client(self): 
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
		self.__client = MQTTClient(self.__network_id, self.__ip_address)
		self.__client.connect()

	def publish(self, message):
		self.__client.publish('esys/asd/', bytes("AALOO", 'utf-8'))

	def recieve_message(self, topic): 
		self.__client.set_callback(self.sub_cb) 
		self.__client.subscribe(topic)
		self.__client.wait_msg() 
		self.__client.check_msg()
>>>>>>> d23b3f7ccdc62be1c5c2a7e4dd484871f0be4740
