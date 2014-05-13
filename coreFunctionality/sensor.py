import socket   #for sockets
import sys  #for exit
import GlobalResources as gR
import threading
from copy import deepcopy

class SensorData(threading.Thread):
	def __init__(self):
		super(SensorData, self).__init__()
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		remote_ip='128.30.79.98'
		port = 7000
		self.s.connect((remote_ip , port))
		print 'Connected'
		self._stopFlag = threading.Event()

	def run(self):
		while not self._stopFlag.isSet():
			#if gR.newTargetsFlag.isSet():
			#   gR.newTargetsFlag.clear()
			#   self.update_targets(gR.myTargets)
			newTargets = self.receive_targets()
			if not gR.newTargetsFlag.isSet():
				gR.lockMyTargets.acquire()
				gR.myTargets = deepcopy(newTargets)
				gR.lockMyTargets.release()
				gR.newTargetsFlag.set()
				
		
	def stop (self):
		self._stopFlag.set()

	def receive_targets(self):
		reply = self.s.recv(19)
		return reply
