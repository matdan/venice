'''
Created on May 9, 2014

@author: Matthias
'''
import cmd
import GlobalResources as gR
import time
import math

class ManualControl(cmd.Cmd):
    '''
    Class to achieve manual control over an Installation
    '''
    
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.selectedEmitter = None
    
    def do_sel(self, arrLoc):
        try:
            self.selectedEmitter = (int(arrLoc[0]),int(arrLoc[1:]))
        except: print "selection failed"
        else: print "selection of emitter ", self.selectedEmitter, " successful"
      
    def do_w(self, angle):
        if angle:
            self.issueCommand('a', abs(float(angle))) 
        else:
            self.issueCommand('a', 1.0) 
        
    def do_s(self, angle):
        if angle:
            self.issueCommand('a', -1 * abs(float(angle))) 
        else:
            self.issueCommand('a', -1) 
    
    def do_b(self, x):
        self.issueCommand('b', None)
        
    def do_dR1(self, x):
        eALocList = gR.myInstallationThread.getEmitterALocs()
        print eALocList
        for loc in eALocList:
            self.do_sel(loc)
            self.do_b(1)
            time.sleep(1)
            for i in range(45):
                self.do_w(1)
                time.sleep(0.02)
            time.sleep(1)
            for i in range(90):
                self.do_s(1)
                time.sleep(0.02)
            time.sleep(2)
            for i in range(45):
                self.do_w(1)
                time.sleep(0.02)
            time.sleep(1)
            self.do_b(1)
            time.sleep(1)

    def do_dR2(self, x):
        eALocList = gR.myInstallationThread.getEmitterALocs()
        print eALocList
        for loc in eALocList:
            self.do_sel(loc)
            self.do_b(1)
            time.sleep(1)
            self.do_b(1)
            time.sleep(0.2)

    def do_dR3(self, x):
        eALocList = gR.myInstallationThread.getEmitterALocs()
        print eALocList
        for i in range(11):
            for loc in eALocList:
                self.do_sel(loc)
                self.do_w(4)
            #time.sleep(0.01)
        for i in range(22):
            for loc in eALocList:
                self.do_sel(loc)
                self.do_s(4)
            #time.sleep(0.01)
        for i in range(11):
            for loc in eALocList:
                self.do_sel(loc)
                self.do_w(4)
            #time.sleep(0.01)
        
    def do_EOF(self, line):
        return True
    
    def do_saveConfig(self, filename):
        gR.saveConfigFlag.set()
        if filename:
            gR.lockSaveConfigFilename.acquire(1)
            gR.saveConfigFilename = 'filename'
            gR.lockSaveConfigFilename.release()
            
    
    def issueCommand(self, cType, payload):
        '''
        issues a command to rotate the selected emitter by angle
        '''
        if self.selectedEmitter:
            if not gR.newCommandFlag.isSet():
                gR.lockDirectCommand.acquire(1)
                gR.directCommand = (self.selectedEmitter, cType, payload)
                gR.lockDirectCommand.release()
                gR.newCommandFlag.set()
                time.sleep(0.01)
                print "command issued to emitter ", self.selectedEmitter, "cType: ", cType, "payload: ", payload
            else:
                print "command failed, flag set, try again"
        else:
            print "command failed, no emitter selected"