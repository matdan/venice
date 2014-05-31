'''
Created on May 9, 2014

@author: Matthias
'''
import cmd
import GlobalResources as gR
import time
import math
import Logger as log
import TargetAcquisition as tA
import threading
import DataGateway as dG
import cascade

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
        """
        test emitters one by one
        bulb on. 45+ 90- 45+ bulb off.
        """
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

    def do_startPreview(self, args):

        if not gR.myPreviewThread.isAlive():
            gR.myPreviewThread =  log.Logger()
            gR.myPreviewThread.start()
            print "communication to rhino preview started"
        else:
            print "communication to rhino preview already running"

    def do_stopPreview(self, args):
        if gR.myPreviewThread.isAlive():
            gR.myPreviewThread.stop()
            gR.myPreviewThread.join()
            print "preview stopped"
        else:
            print "preview not active"

    def do_startArduinos(self, args):
        try:
            if not gR.myCommunicationThread.isALive():
                gR.myCommunicationThread = cascade.ArduinoDriver(gR.myEStats, gR.path)
                gR.myCommunicationThread.start()
                print "arduino communication started"
            else:
                print "arduino communication already active"
        except:
            gR.myCommunicationThread = cascade.ArduinoDriver(gR.myEStats, gR.path)
            gR.myCommunicationThread.start()
            print "arduino communication started"

    def do_stopArduinos(self, args):
        if gR.myCommunicationThread.isAlive():
            gR.myCommunicationThread.stop()
            gR.myCommunicationThread.join()
            print "arduinos stopped"
        else:
            print "preview not active"
        
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


class InstallationControl(cmd.Cmd):
    '''
    Class to achieve manual control over an Installation
    '''
    
    def __init__(self):
        cmd.Cmd.__init__(self)


    def do_EOF(self, line):
        return True

    def do_getTargets(self, args):
        try: 
            if not gR.myTargetAcquisitionThread.isAlive():
                
                #gR.myTargetAcquisitionThread = tA.SensorData()
                #gR.myTargetAcquisitionThread = tA.DataTest()
                gR.myTargetAcquisitionThread = tA.FakeData()

                gR.myTargetAcquisitionThread.start()

                print "target acquisition thread started"

            else:
                print "target acquisition thread already running"
        except:
            #gR.myTargetAcquisitionThread = tA.SensorData()
            #gR.myTargetAcquisitionThread = tA.DataTest()
            gR.myTargetAcquisitionThread = tA.FakeData()

            gR.myTargetAcquisitionThread.start()

            print "target acquisition thread started"



    def do_stopTargetAcquisition(self, args):
        if gR.myTargetAcquisitionThread.isAlive():
            gR.myTargetAcquisitionThread.stop()
            gR.myTargetAcquisitionThread.join()
            print "targetAcquisition stopped"
        else:
            print "targetAcquisition not active"

    def do_connectVis(self, args):
        try:
            if not gR.myVisualizationDG.isAlive():
                gR.myVisualizationDG.start()
                print "communication to visualisation thread started"
            else:
                print "communication to visualisation thread already running"
        except:
            gR.myVisualizationDG = dG.VisulaizationGateway("localwarmingdev.meteor.com")
            gR.myVisualizationDG.start()
            print "communication to visualisation thread started"

    def do_stopVisThread(self, args):
        if gR.myVisualizationDG.isAlive():
            gR.myVisualizationDG.stop()
            gR.myVisualizationDG.join()
            print "visThread stopped"
        else:
            print "visThread not active"

    def do_startPreview(self, args):

        if not gR.myPreviewThread.isAlive():
            gR.myPreviewThread =  log.Logger()
            gR.myPreviewThread.start()
            print "communication to rhino preview started"
        else:
            print "communication to rhino preview already running"

    def do_stopPreview(self, args):
        if gR.myPreviewThread.isAlive():
            gR.myPreviewThread.stop()
            gR.myPreviewThread.join()
            print "preview stopped"
        else:
            print "preview not active"

    def do_startArduinos(self, args):
        try:
            if not gR.myCommunicationThread.isALive():
                gR.myCommunicationThread = cascade.ArduinoDriver(gR.myEStats, gR.path)
                gR.myCommunicationThread.start()
                print "arduino communication started"
            else:
                print "arduino communication already active"
        except:
            gR.myCommunicationThread = cascade.ArduinoDriver(gR.myEStats, gR.path)
            gR.myCommunicationThread.start()
            print "arduino communication started"

    def do_stopArduinos(self, args):
        if gR.myCommunicationThread.isAlive():
            gR.myCommunicationThread.stop()
            gR.myCommunicationThread.join()
            print "arduinos stopped"
        else:
            print "preview not active"

    def do_getItOverWith(self, args):
        gR.myInstallationThread.stop()
        gR.myInstallationThread.join()

        threads = [gR.myCommunicationThread, gR.myTargetAcquisitionThread, gR.myPreviewThread]
        for thread in threads:
            try:
                if thread.isAlive():
                    thread.stop()
                    thread.join()
            except: pass
        self.do_EOF(None)