'''
Created on Apr 30, 2014

@author: Matthias Danzmayr
'''

import Emitter
import threading
import GlobalResources as gR
import math
from copy import deepcopy

class Installation(threading.Thread):
    '''
    Installation Class
    
    is the highest unit of organization of the installation
    it supervises the operation of the installation:
        - assigns targets to the right emitters
        - makes sure that power constraints are not exceeded
    
    an installation-object holds 
    - registry for arrays and emitters
    - methods to initiate arrays
    - methods to return operation metrics
    - Targets
    '''
    
    def __init__(self, configuration):
        '''
        initiate installation object
        '''
        super(Installation, self).__init__()
        self.configuration = configuration
        self.eSpacing = self.configuration.getESpacing()
        self.rSpacing = self.configuration.getRSpacing()
        self.masters = []
        self.slaves = []
        #self.comModule = comModule
        self.emitters = list()
        self.initiateEmitters()
        self.initiateEmittersPhase2()
        self.trackedTargets = None #{"ID1":(1000, 650, 1000)}
        self.operating = False
        self._stop = threading.Event()
        #self.operate()

    #def getComModule(self):
    #    return self.comModule
    
    def run(self):
        self.operate()
    
    def stop(self):
        self._stop.set()
    
    def initiateEmitters(self):
        for i in self.configuration.getEmitterConfig():
            self.emitters.append(list())
            for j in i:
                self.emitters[-1].append( Emitter.Emitter( self, ( j[0], j[1], j[2] ), ( j[3], j[4] ), j[5], j[6], j[7], j[8], j[9], j[10], j[11] ) )
    
    def initiateEmittersPhase2(self):
        for emitterRow in self.emitters:
            for emitter in emitterRow:
                emitter.determineRange()
                emitter.determineExtRangeX()
    
    def updateEmitters(self):
            self.updateEmitterStates()     #masters are determined, states are communicated back to installation and respective unit
            self.distributeSlaves()         #invoke getSlaves in Masters
            self.invokeMasters()           #masters determine their angles and command slaves, all communicate angles back to installation and respective unit
            self.invokeSlaves()
            self.updateUnits()             #units are told to communicate new angles to arduino
    
    def updateEmitterStates(self):
        for emitterRow in self.emitters:
            for emitter in emitterRow:
                emitter.determineStatus()
        
    def updateUnits(self):
        for emitterRow in self.emitters:
            for emitter in emitterRow:
                emitter.communicateAngle()
    
    def invokeMasters(self):
        for emitterRow in self.emitters:
            for emitter in emitterRow:
                emitter.updateAngle(True)
                emitter.commandSlaves()
    
    def invokeSlaves(self):
        for emitterRow in self.emitters:
            for emitter in emitterRow:
                emitter.updateAngle(False)
    
    def distributeSlaves(self):
        for master in self.masters:
            master.getSlaves()
        
    def getEmitter(self, x, y):
        if x<0 or y<0: return False
        try: return self.emitters[x][y]
        except: return False
        
    def registerMaster(self, emitter):
        '''
        register an Emitter as a MasterEmitter by putting it into the masters list
        
        if Emitter was previously registered as Slave remove from Slave list
        '''
        #print "registering master"
        self.masters.append(emitter)
        try:
            self.slaves.remove(emitter)
        except:
            return

    def registerSlave(self, emitter):
        '''
        register an Emitter as a SlaveEmitter by putting it into the slave list
        
        if Emitter was previously registered as Slave remove from Masters list
        '''
        #print "registering slave"
        self.slaves.append(emitter)
        try:
            self.masters.remove(emitter)
        except:
            return

    def actuateEmitters(self):
        """
        Makes all registered Emitter-objects (in masters and slaves lists) execute their actuate method
        no returns
        """
        for item in self.masters:
            item.actuate()
        for item in self.slaves:
            item.actuate()

    def getEmitterPhyLocation(self, x, y):
        if not x < 0 and not y < 0:
            try:
                return self.getEmitter(x, y).getLocation()
            except IndexError:
                return False
            except:
                print "Unexpected Error while looking up emitter-location"
                return False
        else:
            return False
    
    def operate (self):
        while not self._stop.isSet():
            if self.obtainTargets():
                self.updateEmitters()
                gR.emitterUpdatedFlag.set()
            if gR.newCommandFlag.isSet():
                self.followCommand()
                self.updateEmitters()
                gR.emitterUpdatedFlag.set()
            if gR.saveConfigFlag.isSet():
                gR.saveConfigFlag.clear()
                self.saveConfig()
                
    def saveConfig(self):
        for row in self.emitters:
            for emitter in row:
                newDefAng = emitter.getDefaultAngle()
                arrLoc = emitter.getArrLoc()
                self.configuration.updateDefaultAngle(arrLoc, newDefAng)
        
        gR.lockSaveConfigFilename.acquire(1)
        filename = deepcopy(gR.saveConfigFilename)
        gR.lockSaveConfigFilename.release()
        self.configuration.writeConfig(filename)
        self.configuration.loadConfig(filename)
    
    def followCommand(self):
        gR.lockDirectCommand.acquire(1)
        command = deepcopy(gR.directCommand)
        gR.lockDirectCommand.release()
        gR.newCommandFlag.clear()
        self.getEmitter(int(command[0][0]), int(command [0][1])).changeDefAngle(int(command[1]))
        #except: print "command failed in Installation.followCommand"
        
    def obtainTargets(self):
        if gR.newTargetsFlag.isSet():
            gR.newTargetsFlag.clear()
            gR.lockMyTargets.acquire(1)
            try: self.trackedTargets = deepcopy(gR.myTargets)
            finally: 
                gR.lockMyTargets.release()
            return True
        else:
            return False

    def targetsInRange(self, eRange):
        targets = {}
        try:
            for key, target in self.trackedTargets.iteritems():
                if eRange[0] < target[0] and target[0] < eRange[1] and eRange[2] < target[1] and target[1] < eRange[3]:
                    targets[key] = target
        except:
            pass
            #print "Error in Installation.targetsInRange(). Probable Cause: No targets are being tracked"
        return targets            
    
    def getTarget(self, targetID):
        return self.trackedTargets[targetID]
        
    def getESpacing(self):
        return self.eSpacing
        
    def getRSpacing(self):
        return self.rSpacing
    
    def getEmitterList(self):
        return self.emitters

class EmitterStatuses(object):
    
    def __init__(self, configuration):
        self.statuses = self.generateEntries(configuration)
        
    def generateEntries(self, configuration):
        statuses = {}
        emitterConfig = configuration.getEmitterConfig()
        #print emitterConfig
        i = 0
        for row in configuration.getEmitterConfig():
            j = 0
            for eConf in row:
                #print i, j
                statuses[ ( int(emitterConfig[i][j][3]), int(emitterConfig[i][j][4]) ) ] = [ emitterConfig[i][j][7], emitterConfig[i][j][9], emitterConfig[i][j][8], emitterConfig[i][j][10], 0, emitterConfig[i][j][5] ]
                #print statuses[ ( int(emitterConfig[i][j][3]), int(emitterConfig[i][j][4]) ) ]
                #dictionary layout
                #[arrayLocation] : [ servoArduinoID, relayArduinoID, servoPin, relayPin, state, angle(DEG) ]
                j += 1
            
            i += 1
        #print statuses
        return statuses
    
    def getStatuses(self):
        return self.statuses
    
    def updateEmitter(self, emitter):
        emArLoc = emitter.getArrLocation()
        self.statuses.get( ( int(emArLoc[0]), int(emArLoc[1]) ) )[-2] = int(emitter.getState()) + int(emitter.getBulbState())
        self.statuses.get( (int(emArLoc[0]), int(emArLoc[1])) )[-1] = math.degrees( emitter.getAngle() * emitter.getRotationMod() + emitter.getDefaultAngle() )
    
    def printStatuses(self):
        print self.statuses
                