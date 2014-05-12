'''
Created on May 8, 2014

@author: Matthias
'''
import threading
import GlobalResources as gR
import time
import socket
import csv

class FakeData(threading.Thread):



    def __init__(self):

        super(FakeData, self).__init__()
        
    def run(self):
        """
        #fakeData1
        gR.lockMyTargets.acquire(1)
        gR.myTargets = {1:[500,500,1200]}
        gR.lockMyTargets.release()
        gR.newTargetsFlag.set()
        
        time.sleep(2)
        gR.lockMyTargets.acquire(1)
        gR.myTargets = {1:[500,1500,1200]}
        gR.lockMyTargets.release()
        gR.newTargetsFlag.set()
        
        time.sleep(2)
        gR.lockMyTargets.acquire(1)
        gR.myTargets = {1:[500,2500,1200]}
        gR.lockMyTargets.release()
        gR.newTargetsFlag.set()
        """
        
        #fakeData2
        for i in range(800):
            gR.lockMyTargets.acquire(1)
            gR.myTargets = { 1:[-1500+i*10,1000,1200], 2:[900,0+i*10,1200], 3:[3600-i*5,3000-i*4,1200] }
            gR.lockMyTargets.release()
            gR.newTargetsFlag.set()
            
            time.sleep(0.01)

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
            gR.lockMyTargets.acquire(1)
            try:
                gR.newTargetsFlag.set()
                self.update_targets(gR.myTargets)
            finally:
                gR.lockMyTargets.release()

    def stop(self):
        self._stop.set()

    def update_targets(self, targets):
        reply = self.s.recv(19)
        x = reply.split(',')
        out = {}
        out[int(x[0])] = [int(float(x[1])), int(float(x[2]))]
        gR.myTargets = out


class DataTest(threading.Thread):
    def __init__(self):
        super(DataTest, self).__init__()
        self._stopFlag = threading.Event()
        self.data = self.parse_data('coordinates.csv')

    def run(self):
        while not self._stopFlag.isSet():
            gR.lockMyTargets.acquire(1)
            #try:
            self.update_targets()
            gR.newTargetsFlag.set()
            #except: 
            #    print "nooooo!"
                
            #finally:
            gR.lockMyTargets.release()
            time.sleep(0.001)

    def stop(self):
        self._stopFlag.set()

    def parse_data(self, coord_file):
        """
        with open(coord_file, 'r') as f:
            content = f.readlines()
            print content
        return content
        """
        file = open(coord_file)
        fileReader = csv.reader(file)
        fileArray = list()
        for row in fileReader:
            fileArray.append(row)
        #print configArray.
        print len(fileArray)
        return fileArray

    def update_targets(self):
        if len(self.data) > 0:
            datum = self.data[0]
            out = {}
            out[1] = [float(datum[1]) * 1000+1000, float(datum[0]) * 1000,  1200]
            del self.data[0]
        else: self.stop()
        gR.myTargets = out
        print gR.myTargets
            