import GlobalResources as gR
import ddpclient
import json
import threading
import time
from copy import deepcopy

class VisulaizationGateway(threading.Thread):

	def __init__(self, host):
		super(VisulaizationGateway, self).__init__()
		self._stop = threading.Event()
		self.app = ddpclient.App(host, False)

	def run(self):
		#send data every second
		theTime = 0
		while not self._stop.isSet():
			if not time.time() - theTime < 1:
				self.sendData()
				theTime = time.time()

	def stop(self):
		self._stop.set()

	def sendData(self):
		data = self.createData()
		self.app.do_call("gateway [\"khu8dqMtLeuUxkZUu9sPHtqVxTCxyr\","+json.dumps(data)+"]")
		print json.dumps(data)

	def createData(self):
		targetData = self.retrieveTargetData()
		timestamp = time.time()
		data = [{'timestamp':timestamp,'balls':targetData}]
		return data

	def retrieveTargetData(self):
		return gR.myInstallationThread.targetData()