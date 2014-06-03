import glob
import operator
import serial
import sys
import time
import threading
import GlobalResources as gR
from copy import deepcopy

'''
Device
id_num - id as specified in config
path - path to the device on the os, also specified in config
port - open serial port connection
'''
class Device:
	def __init__(self, id_num, path):
		self.id_num = id_num
		self.path = path
		self.values = {}

	def readState(self, pin, value):
		self.values[pin] = value

	def getSortedValues(self):
		pinList = self.values.keys()
		valueList = self.values.values()
		pinList, valueList = zip(*sorted(zip(pinList, valueList)))
		return valueList

class ArduinoDriver(threading.Thread):
	def __init__(self, emitterStats, paths):
		super(ArduinoDriver, self).__init__()
		# indexes to device paths
		self.devices = []
		self.last_update_time = time.clock()
		self.arduino_delay = 0.05

		for i,path in enumerate(paths):
			print path
			self.devices.append(Device(i, path))

		# architecture of data_store
		# list of devices (arduinos)
		# each index of list contains a dictionary
		# dictionary contains keys, which are pins
		# values of dictionary are angle/state
		# example:
		#[{pin:angle}, {pin:state}, {pin:angle}, {pin:state}, ...]

		self.readEmitterStates()
		self.open_ports()

		self._stopFlag = threading.Event()

	def run(self):
        #[arrayLocation] : [ servoArduinoID, relayArduinoID, servoPin, relayPin, state, angle(DEG) ]
		while not self._stopFlag.isSet():
			if gR.emitterUpdatedFlag.isSet():
				gR.emitterUpdatedFlag.clear()

				self.readEmitterStates()
				#try:
				self.updateArduinos()
				#except: print "arduino write error"


	def stop(self):
		self.close_ports()
		self._stopFlag.set()

	def readEmitterStates(self):
		gR.lockMyEstates.acquire(1)
		newStates = gR.myEStats.getStatuses()
		gR.lockMyEstates.release()

		for key, value in newStates.iteritems():
			self.devices[int(value[0])-1].readState(int(value[2]),int(value[5]))
			self.devices[int(value[1])-1].readState(int(value[3]),int(value[4]))

	def updateArduinos(self):
		# if enough time has elapsed since the last update, update arduinos
		elapsed = (time.clock() - self.last_update_time)
		if elapsed > self.arduino_delay:
			#print 'data_store:'
			#print self.data_store
			#print 'devices:'
			#print self.devices
			# iterate over arduinos to send data to


			for device in self.devices:
				serial_data = ""
				for data in device.getSortedValues():
					#print str(data[1])
					serial_data = serial_data + str(data).zfill(3)
				

				serial_data = serial_data + "\0"
				print "sending data to port: ", device.path,"\n", serial_data,"\n"
				# send the data to an arduino
				if device.path:
					device.port.write(serial_data)

			# update the clock if you need a delay
			self.last_update_time = time.clock()

	# opens all the arduinos as configured in __init__.py
	def open_ports(self):
		print 'opening ports'
		for device in self.devices:
			print device.path
			if device.path:
				device.port = serial.Serial(int(device.path)-1, 9600)

	# close all the arduinos
	def close_ports(self):
		print 'closing ports'
		for device in self.devices:
			if path:
				device.port.close()