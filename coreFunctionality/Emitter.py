'''
Created on May 1, 2014

@author: Matthias
'''

import VectorMath as vm
import math
import GlobalResources as gR

class Emitter(object):
    
    def __init__(self, installation, phyLocation, arrLocation, defaultAngle, maxTilt, servoArduinoID, servoPin, relayArduinoID, relayPin, rotationMod ):
        self.phyLocation = phyLocation          #coorinates of physical location
        #print "initiating emitter at: " + str(self.phyLocation)
        self.arrLocation = arrLocation          #coordinates in emitterArray
        self.defaultAngle = math.radians(float(defaultAngle)) 
        self.angle = math.radians(float(defaultAngle))
        self.installation = installation        #parent installation-object
        self.relayArduinoID = relayArduinoID
        self.servoArduinoID = servoArduinoID
        self.relayPin = relayPin
        self.servoPin = servoPin
        self.state = 0             
        self.rotationMod = rotationMod              #TRUE for master, FALSE for slave
        #self.range = self.determineRange()       #list of (xMin, xMax, yMin, yMax)
        self.target = None                      #key of tracked target in installation's target dictionary
        self.influence = 1
        self.slaves = None
        self.commands = []
        self.bulbActive = False
        self.tertiaryTarget = None
        self.rangeExtensionX = self.installation.getRSpacing()/2
        
    def determineStatus(self):
        """
        checks for targets in range
        sets state
        communicates state to installation
        """
        trackedTargetsInRange = self.installation.targetsInRange(self.range)
        
        if trackedTargetsInRange:
            #emitter has targets in range
            if self.target != None and trackedTargetsInRange.has_key(self.target):
                #emitter was already tracking a target and that target is still in its range
                self.beMaster()
                return
                
            else:
                #emitter was not tracking before but has targets in Range
                self.target = self.determineClosestTarget(trackedTargetsInRange)
                self.beMaster()
            
            self.tertiaryTarget = None
                
        else:
            self.target = None
            trackedTargetsInExtRangeX = self.installation.targetsInRange(self.extRangeX)

            if trackedTargetsInExtRangeX:
                self.tertiaryTarget = self.determineClosestTarget(trackedTargetsInExtRangeX)
                self.beMaster()
            else:
                #no targets in range
                self.tertiaryTarget = None
                self.beSlave()
                
        self.registerEmitter()
    
    def changeDefAngle(self, angle):
        '''
        changes emitter's self.defaultAngle by angle
        '''
        self.defaultAngle += angle
        self.updateAngle(self.state)
        self.communicateAngle()
        gR.emitterUpdatedFlag.set()
    
    def targetXDistance(self, targetID):
        return float(self.installation.getTarget(targetID)[0]) - float(self.phyLocation[0])
    
    def targetYDistance(self, targetID):
        return float(self.installation.getTarget(targetID)[1]) - float(self.phyLocation[1])    
    
    def getSlaves(self):
        """
        determine which slaves are influenced by master-emitter
        """
        self.slaves = list()
        x=int(self.arrLocation[0])
        y=int(self.arrLocation[1])
        
        #path 1 
        i=0
        while i < self.influence:
            i += 1
            
            slaveCandidate = self.installation.getEmitter(x,y-i)
            if not slaveCandidate: break
            if not slaveCandidate.isMaster():
                self.slaves.append(slaveCandidate)
            else:
                break
                
        #path 2
        i=0
        while i < self.influence:
            i += 1
            
            slaveCandidate = self.installation.getEmitter(x,y+i)
            if not slaveCandidate: break
            if not slaveCandidate.isMaster():
                self.slaves.append(slaveCandidate)
            else:
                break      

    def determineClosestTarget(self, targetList):
        """
        targetList is a dictionary of targets k = targetID v = point
        returns ID/key of closest Point
        """
        distances = {}
        for key in targetList.keys():
            distances[key] = vm.getPointDistance(self.phyLocation, targetList[key])
        
        return min(distances, key=distances.get)
        
    def isMaster(self):
        return self.state
        
    def determineRange(self):
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
            minY = myPhyY - self.installation.getESpacing()
        else:
            minY = minYLoc[1]
        
        maxYLoc = self.installation.getEmitterPhyLocation( myArrX, myArrY + 1 )
        if not maxYLoc:
            maxY = myPhyY + self.installation.getESpacing()
        else:
            maxY = maxYLoc[1]
        
        self.range = (int(minX), int(maxX), int(minY), int(maxY))
        
    def determineExtRangeX(self):
        self.extRangeX = [ self.range[0] - self.rangeExtensionX, self.range[1] + self.rangeExtensionX, self.range[2], self.range[3] ]
    
    def updateAngle(self, masterOrSlave):
        if not masterOrSlave == self.state:
            return
        
        if self.state:
            if self.target:
                self.setAngle(self.angleToTarget(self.installation.getTarget(self.target)))
            elif self.tertiaryTarget:
                distance = self.targetXDistance(self.tertiaryTarget)
                maxAngle = abs(self.angleToTarget( [ float(self.range[1]),0, 1200 ] ))
                if distance > 0:
                    relevantRange = self.range[1]
                    outOfRange = distance - (int(relevantRange) - int(self.phyLocation[0]))
                    self.setAngle(vm.mapToDomain(outOfRange, 0, float(abs(relevantRange-float(self.extRangeX[1]))), maxAngle, 0))
                elif distance < 0:
                    relevantRange = self.range[0]
                    outOfRange = int(self.phyLocation[0]) - int(relevantRange) + distance
                    self.setAngle( vm.mapToDomain(outOfRange, 0, -1 * float(abs(relevantRange-float(self.extRangeX[0]))), -1 * float(maxAngle), 0) )
                else:
                    raise Exception("Evil's afoot!")
                
                
        elif not self.state:
            i = 0
            comComb = 0
            for command in self.commands:
                comComb += command
                i += 1
            if i == 0:
                self.setAngle(0)
            else:
                print i
                self.setAngle(comComb/i)
        
    def setAngle(self, angle):
        """
        takes in angle in RAD
        sets angle in degrees
        """
        self.angle = angle
    """
    def commandSlaves(self):
        if self.state:
            for slave in self.slaves:
                slave.receiveCommand( float(self.angle), self.arrLocation )
    
    def receiveCommand(self, angle, origin):
        self.commands = []
        distance = abs(int(self.arrLocation[0]) - int(origin[0])) + abs(int(self.arrLocation[1]) - int(origin[1]))
        self.commands.append((angle) * self.commandEffect(distance))        
    
    def commandEffect(self, distance):
        effect = (math.sin((self.influence/2+distance)*math.pi/self.influence)/2+0.5)
        if effect < 0.03:
            effect = 0
        return effect
    """
    def commandSlaves(self):
        if self.state:
            for slave in self.slaves:
                if self.target:
                    slave.receiveCommand( float(self.angle), self.target )
                elif self.tertiaryTarget:
                    slave.receiveCommand( float(self.angle), self.tertiaryTarget )
    
    def receiveCommand(self, angle, target):
        self.commands = []
        distance = abs(self.targetYDistance(target))-gR.eSpacing
        self.commands.append((angle) * self.commandEffect(distance))        
    
    def commandEffect(self, distance):
        #if distance > (gR.eSpacing*(self.influence+1)):
        #    return 0
        effect = (math.sin(((gR.eSpacing*(self.influence)/2+distance)*math.pi/(gR.eSpacing*(self.influence))))/2+0.5)
        return effect
    
    def angleToTarget(self, target):
        target3D = target
        target2D = (int(target3D[0]), int(target3D[2]))
        location2D = (int(self.phyLocation[0]), int(self.phyLocation[2]))
        
        targetVector = vm.createVector(location2D, target2D)
        
        targetAngle = vm.angleBetween2D([0,-1], targetVector)
        
        return targetAngle
        
    def beSlave(self):
        self.commands = []
        self.bulbActive = False
        if self.state:
            self.state = False
            
    def beMaster(self):
        self.commands = []
        if not self.state:
            self.state = True
        
        if self.target:
            if not self.bulbActive:
                self.bulbActive = True
        else:
            self.bulbActive = False
    
    def getBulbState(self):
        return self.bulbActive
    
    def getLocation(self):
        return self.phyLocation
    
    def getArrLocation(self):
        return self.arrLocation
    
    def registerEmitter(self):
        if self.state:
            self.installation.registerMaster(self)
        else:
            self.installation.registerSlave(self)

    def communicateAngle(self):
        gR.myEStats.updateEmitter(self)
        
    def getState(self):
        return self.state
    
    def getAngle(self):
        return float(self.angle)
    
    def getRotationMod(self):
        '''
        returns emitter's rotation modulator
        '''
        return float(self.rotationMod)
    
    def getDefaultAngle(self):
        '''
        returns emitter's default angle
        '''
        return self.defaultAngle
    
    def getArrLoc(self):
        return self.arrLocation