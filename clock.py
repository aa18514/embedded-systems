"""further decording to be done here"""

class Clock(): 
	def __init__(self, message): 
		self.__val = message 
		#self.__hour = ? 
		#self.__minutes = ? 
		#self.__seconds = ? 
		
	def update_time(self, Value): 
		self.__val = Value

	def increment(self): 
		self.__val += 1