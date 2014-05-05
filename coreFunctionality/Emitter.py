'''
Created on May 1, 2014

@author: Matthias
'''

import VectorMath as vm
import math
from output import Logger as log

class Emitter(object):
    
    def __init__(self, installation, phyLocation, arrLocation, defaultAngle, maxTilt, servoArduinoID, servoPin, relayArduinoID, relayPin ):
        self.phyLocation = phyLocation          #coorinates of physical location
        #print "initiating emitter at: " + str(self.phyLocation)
        self.arrLocation = arrLocation          #coordinates in emitterArray
        self.angle = 0 
        self.defaulAngle = defaultAngle         #pre-configured default servo-position
        self.installation = installation        #parent installation-object
        self.relayArduinoID = relayArduinoID
        self.servoArduinoID = servoArduinoID
        self.relayPin = relayPin
        self.servoPin = servoPin
        self.state = False                             #TRUE for master, FALSE for slave
        #self.range = self.determineRange()       #list of (xMin, xMax, yMin, yMax)
        self.target = None                      #key of tracked target in installation's target dictionary
        self.influence = 2
        self.slaves = None
        self.commands = list()
        
    """
    checks for targets in range
    sets state
    communicates state to installation
    """
    def determineStatus(self):
        #retrieve targets in emitter-range from installation as dictionary
        trackedTargetsInRange = self.installation.targetsInRange(self.range)
        
        if trackedTargetsInRange:
            #emitter has targets in range
            
            if self.target != None and trackedTargetsInRange.has_key(self.target):
                #emitter was already tracking a target and that target is still in its range
                return
                
            else:
                #emitter was not tracking before but has targets in Range
                
                self.target = self.determineClosestTarget(trackedTargetsInRange)
                self.beMaster()
                
        else:
            #no targets in range
            
            self.beSlave()
                
        self.communicateState()
    
    """
    determine which slaves are influenced by master-emitter
    """
    def getSlaves(self):
        self.slaves = list()
        #path 1 
        i=0
        x=self.arrLocation[0]        
        y=self.arrLocation[1]
        while i < self.influence:
            i += 1
            
            try: 
                slaveCandidate = self.installation.getEmitter(x,y-i)
            except:
                break
            
            if not slaveCandidate.isMaster():
                self.slaves.append(slaveCandidate)
                
        #path 2
        i=0
        while i < self.influence:
            i += 1
            
            try: 
                slaveCandidate = self.installation.getEmitter(x,y+i)
            except:
                break
            
            if not slaveCandidate.isMaster():
                self.slaves.append(slaveCandidate)
        
        #path 3
        j = False
        i = 0 
        while i < self.influence:
            
            try: 
                slaveCandidate = self.installation.getEmitter(x-1,y-i)
            except:
                break
            
            if not slaveCandidate.isMaster():
                j = True
                self.slaves.append(slaveCandidate)
                
            i += 1
            
        #path 4
        if j:
            i = 1 
            while i < self.influence:
                
                try: 
                    slaveCandidate = self.installation.getEmitter(x-1,y+i)
                except:
                    break
                
                if not slaveCandidate.isMaster():
                    self.slaves.append(slaveCandidate)
                    
                i += 1
        
        #path 5
        j = False
        i=0 
        while i < self.influence:
            
            try: 
                slaveCandidate = self.installation.getEmitter(x+1,y-i)
            except:
                break
            
            if not slaveCandidate.isMaster():
                j = True
                self.slaves.append(slaveCandidate)
                
            i += 1
            
        #path 6
        if j:
            i=1 
            while i < self.influence:
                
                try: 
                    slaveCandidate = self.installation.getEmitter(x+1,y+i)
                except:
                    break
                
                if not slaveCandidate.isMaster():
                    self.slaves.append(slaveCandidate)
    
                    
                i += 1
                
    """
    targetList is a dictionary of targets k = targetID v = point
    returns ID/key of closest Point
    """
    def determineClosestTarget(self, targetList):
        distances = {}
        for key in targetList.keys():
            distances[key] = vm.getPointDistance(self.phyLocation, targetList[key])
        
        return min(distances, key=distances.get)
        
    def isMaster(self):
        return self.state
        
    def determineRange(self):
        #print "determining range of " + str(self.arrLocation)
        myArrX = int(self.arrLocation[0])
        myArrY = int(self.arrLocation[1])
        myPhyX = int(self.phyLocation[0])
        myPhyY = int(self.phyLocation[1])
        
        minXLoc = self.installation.getEmitterPhyLocation( myArrX - 1, myArrY )
        if not minXLoc:
            minX = myPhyX - self.installation.getRSpacing()
        else:
            minX = minXLoc[0]
            
        maxXLoc = self.installation.getEmitterPhyLocation( myArrX + 1, myArrY )
        if not maxXLoc:
            maxX = myPhyX + self.installation.getRSpacing()
        else:
            maxX = maxXLoc[0]
            
        minYLoc = self.installation.getEmitterPhyLocation( myArrX, myArrY - 1 )
        if not minYLoc:
            minY = myPhyX - self.installation.getESpacing()
        else:
            minY = minYLoc[1]
        
        maxYLoc = self.installation.getEmitterPhyLocation( myArrX, myArrY + 1 )
        if not maxYLoc:
            maxY = myPhyX + self.installation.getESpacing()
        else:
            maxY = maxYLoc[1]
        
        self.range = (minX, maxX, minY, maxY)
        #print "self.range = " + str(self.range)
        
    def updateAngle(self, masterOrSlave):
        if not masterOrSlave == self.state:
            return
        
        if self.state:
            self.angle = self.angleToTarget()
            
        elif not self.state:
            i = 0
            comComb = 0
            for command in self.commands:
                comComb += command
                i += 1
            if i == 0:
                self.angle = 0
            else:
                self.angle = comComb/i
                                            
    def commandSlaves(self):
        if self.state:
            for slave in self.slaves:
                slave.receiveCommand(self.angle, self.arrLocation)
    
    def receiveCommand(self, angle, origin):
        distance = abs(self.arrLocation[0] - origin[0]) + abs(self.arrLocation[1] - origin[1])
        self.commands.append(angle * self.commandEffect(distance))
    
    def commandEffect(self, distance):
        effect = (math.sin((self.influence/2+distance)*math.pi/self.influence)/2+0.5)
        if effect < 0.03:
            effect = 0
        return effect
    
    #def communicateStatus(self):
    
    def angleToTarget(self):
        target2D = (self.target[0], self.target[2])
        location2D = (self.phyLocation[0], self.phyLocation[2])
        
        targetVector = vm.createVector(location2D, target2D)
        
        targetAngle = vm.angle_between((0,-1), targetVector)
        
        return targetAngle
        
    def beSlave(self):
        if self.state:
            self.state = False
            self.commands = None
            
    def beMaster(self):
        if not self.state:
            self.state = True
    
    def getLocation(self):
        return self.phyLocation
    
    def getArrLocation(self):
        return self.arrLocation
    
    def communicateState(self):
        if self.state:
            self.installation.registerMaster(self)
        else:
            self.installation.registerSlave(self)

    def communicateAngle(self):
        self.installation.logger.receiveState(self)
    
    def getState(self):
        return self.state
    
    def getAngle(self):
        return self.angle