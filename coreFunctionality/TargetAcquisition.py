'''
Created on May 8, 2014

@author: Matthias
'''
import threading
import GlobalResources as gR
import time
import socket
import csv
from copy import deepcopy

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
        for i in range(200):
            gR.lockMyTargets.acquire(1)
            gR.myTargets = { 1:[600,0+i*12,1200]}#,  2:[8000-i*10,1900,1200], 3:[3600-i*5,3000-i*4,1200] }#{ 2:[-500+i*8,2585-i*4,1200]}
            #gR.myTargets = { 1:[-4000+i*10,600,1200]}
            #gR.myTargets = { 2:[-500+i*8,2585-i*4,1200]}
            gR.lockMyTargets.release()
            gR.newTargetsFlag.set()
            
            time.sleep(0.02)

        """{2:[900,0+i*5,1200]}
        for i in range(800):
            gR.lockMyTargets.acquire(1)
            #gR.myTargets ={2:[900,0+i*5,1200]}#{ 1:[-4000+i*10,600,1200]}#,  2:[8000-i*10,1900,1200]}#, 2:[900,0+i*10,1200]}#, 3:[3600-i*5,3000-i*4,1200] }{ 2:[-500+i*8,2585-i*4,1200]}
            gR.myTargets = { 1:[-4000+i*10,600,1200]}
            #gR.myTargets = { 2:[-500+i*8,2585-i*4,1200]}
            gR.lockMyTargets.release()
            gR.newTargetsFlag.set()
            
            time.sleep(0.02)


        for i in range(800):
            gR.lockMyTargets.acquire(1)
            #gR.myTargets ={2:[900,0+i*5,1200]}#{ 1:[-4000+i*10,600,1200]}#,  2:[8000-i*10,1900,1200]}#, 2:[900,0+i*10,1200]}#, 3:[3600-i*5,3000-i*4,1200] }{ 2:[-500+i*8,2585-i*4,1200]}
            #gR.myTargets = { 1:[-4000+i*10,600,1200]}
            gR.myTargets = { 2:[-500+i*8,2585-i*4,1200]}
            gR.lockMyTargets.release()
            gR.newTargetsFlag.set()
            
            time.sleep(0.02)
        """
class SensorData(threading.Thread):
    def __init__(self):
        super(SensorData, self).__init__()
        self._stopFlag = threading.Event()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_ip = gR.remote_ip
        port = gR.port
        self.s.connect((remote_ip , port))
        print 'Connected'

    def run(self):
        while not self._stopFlag.isSet():
            try: newTarget = self.receive_targets()
            #if not gR.newTargetsFlag.isSet():
            except: print "Error in SensorData"
            else:
                self.forwardNewTargets(newTarget)
                gR.newTargetsFlag.set()

    def stop(self):
        self._stopFlag.set()
        
    def forwardNewTargets(self, newTarget):
        gR.lockMyTargets.acquire(1)
        
        for key, target in newTarget.iteritems():
            gR.myTargets[key] = target
        
        gR.lockMyTargets.release()
        print "myTargets: ", gR.myTargets
    
    def receive_targets(self):
        reply = self.s.recv(19)
        x = reply.split(',')
        out = {}
        out[int(x[0])] = [int(float(x[1])*1000), int(float(x[2])*1000),1200]
        print "out: ", out
        return out


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
            time.sleep(0.004)

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
            gR.myTargets = out
        else: self.stop()
            