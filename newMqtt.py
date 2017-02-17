import network
import utime
from umqtt.simple import MQTTClient

class Network(): 
	def __init__(self, ip_address, ids): 
		self.__ip_address = ip_address
		self.__network_id = ids
		self.__secure_connection = False

	def sub_cb(self, topic, msg):
		print(msg) 
		self.__msg = msg

	def init_wlan_and_client(self): 
		"""initialize the wireless network
		and set up the client with the appropiate 
		ip_address and id"""
		u = utime.time()
		ap_if = network.WLAN(network.AP_IF)
		ap_if.active(False)
		sta_if =network.WLAN(network.STA_IF)
		sta_if.active(True)
		sta_if.connect('EEERover', 'exhibition')
		while(utime.time() - u < 60 and not sta_if.isconnected()): #block until the we are connected to the internet
			pass
		if sta_if.isconnected(): 
			self.__client = MQTTClient(self.__network_id, self.__ip_address)
			self.__client.connect()
			self.__secure_connection = True
		else: 
			print("unable to connect to the wireless network")

	def publish(self, message):
		if self.__secure_connection == True: 
			self.__client.publish('esys/asd/', message)

	def recieve_message(self, topic): 
		self.__client.set_callback(self.sub_cb) 
		self.__client.subscribe(topic)
		self.__client.wait_msg() #blocking call 
		self.__client.check_msg()