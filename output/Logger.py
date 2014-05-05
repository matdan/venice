'''
Created on May 4, 2014

@author: Matthias
'''

class Logger(object):
    '''
    classdocs
    '''


    def __init__(self, emitterList):
        '''
        Constructor
        '''
        
        self.emitterStates = self.createEmitterList(emitterList)
        
    def createEmitterList(self, emitterList):
        emitterStates = list()
        for i in range(len(emitterList)):
            emitterStates.append(list())
            for j in range(len(emitterList[i])):
                emitterStates[i].append( [0,0] )
        return emitterStates
        
    def receiveState(self, emitter):
        state = [ emitter.getState(), emitter.getAngle() ]
        self.emitterStates[ int( emitter.getArrLocation()[0] ) ][ int( emitter.getArrLocation()[1] ) ] = state
        
    def printArray(self, emitterStates):
        for emitterRow in emitterStates:
            print (10*len(emitterRow)+1)*"-"
            entry = ""
            for i in range(len(emitterRow)):
                entry += "|" + "{0:.2f}".format(emitterRow[i][1]).rjust(8, " ")+" "
            entry += "|\n"
            entry += (10*len(emitterRow)+1)*"-"+"\n"
            for i in range(len(emitterRow)):
                entry += "|" + "{0:.0f}".format(emitterRow[i][0]).center(9, " ")
            entry += "|"
            print entry
            print (10*len(emitterRow)+1)*"-"+"\n"
            
            
            
            
            
        
        