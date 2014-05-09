'''
Created on May 1, 2014

@author: Matthias
'''

import csv

class Configuration(object):
    '''
    classdocs
    '''


    def __init__(self, filename):
        '''
        Constructor
        '''
        self.eSpacing = 235
        self.rSpacing = 1829
        self.config = self.readConfig(filename)
        self.emitterParams = 12
        
        """
        self.emitterConfig = [ [ [ row[i] for row in self.config[ j*self.emitterParams:j*self.emitterParams+self.emitterParams ] ] for i in range( len( self.config[ j * self.emitterParams ] ) ) ] for j in range( len( self.config ) / self.emitterParams ) ]
        #cleanConfig
        #print
        for row in self.emitterConfig:
            print row
        #print self.emitterConfig
        for i in range(len(self.emitterConfig)):
            #print filter(None, self.emitterConfig[i])
            for j in range(len(self.emitterConfig[i])):
                self.emitterConfig[i][j] = filter(None, self.emitterConfig[i][j])
        for i in range(len(self.emitterConfig)):
            #print filter(None, self.emitterConfig[i])
            self.emitterConfig[i] = filter(None, self.emitterConfig[i])
            
        #print
        for row in self.emitterConfig:
            print row
        """
        ml = [self.config[i:i+self.emitterParams] for i in range(0, len(self.config), self.emitterParams)] 
        ml = [map(list, zip(*row)) for row in ml]
        ml2 = []
        for row in ml:
            newRow = []
            for emi in row:
                if not '' in emi:
                    newRow.append(emi)
            if len(newRow) > 0:
                ml2.append(newRow)
        
        self.emitterConfig = ml2
        
        
    def readConfig(self, filename):
        #print "start to read file: " + filename
        configFile = open(filename)
        configReader = csv.reader(configFile)
        configArray = list()
        for row in configReader:
            configArray.append(row)
        #print configArray
        return configArray
        
    def getEmitterConfig (self):
        return self.emitterConfig
    
    def getDefaultAngle(self, x, y):
        return self.emitterConfig[x][y][5]
    
    def getESpacing(self):
        return self.eSpacing
    
    def getRSpacing(self):
        return self.rSpacing