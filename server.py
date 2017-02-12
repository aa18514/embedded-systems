import paho.mqtt.client as mqtt 
import time

if __name__ == "__main__":
	mqttc = mqtt.Client() 
	mqttc.connect('192.168.0.10', 1883, 4)
	mqttc.publish('esys/asd/', bytes("P", 'utf-8'))