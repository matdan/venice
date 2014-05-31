"""
#Version1
import Configuration
import Installation
#import comModule...
from output import GUInterface
from output import Logger
import threading
import time

myConfig = Configuration.Configuration("../config.csv")
myLogger = Logger.Logger()
#myComModule = #fill in the blanks
myInstallationThread = Installation.Installation(myConfig, myLogger)#, myComModule)
myLogger.obtainEmitterList(myInstallationThread.getEmitterList())
myInstallationThread.start()
time.sleep(1)
myInstallationThread.stop()
print "stop issued"
myInstallationThread.join()
print "done"
"""
"""
#Version 2

import Configuration as con
import Installation as ins
import GlobalResources as gR
import Logger as log
import TargetAcquisition as tA
import time

myConfig = con.Configuration("../config.csv")
    
gR.myEStats = ins.EmitterStatuses(myConfig)

myInstallationThread = ins.Installation(myConfig)
myTargetAcquisitionThread = tA.FakeData()
myCommunicationThread = log.Logger()

myInstallationThread.start()
myCommunicationThread.start()
myTargetAcquisitionThread.start()

myTargetAcquisitionThread.join()
myInstallationThread.stop()
myCommunicationThread.stop()
myInstallationThread.join()
myCommunicationThread.join()

#gR.myEStats.printStatuses()

print "done"
"""



#Version 3

import Configuration as con
import Installation as ins
import GlobalResources as gR
import Logger as log
import TargetAcquisition as tA
import time
import commandClasses as cC
import cascade
import DataGateway as dG

if __name__ == '__main__':
    
    # mac path tends to look like this:
    #paths.append('/dev/tty.usbmodem1411')
    # windows path tends to look like this:
    gR.paths.append(10)
    gR.paths.append(6)
    gR.paths.append(7)
    gR.paths.append(8)
    gR.paths.append(9)
    
    

    myConfig = con.Configuration("configBiennale.csv")
    #myConfig = con.Configuration("configSim.csv")
    #myConfig = con.Configuration("configCube.csv")
    
    gR.myEStats = ins.EmitterStatuses(myConfig)
    
    gR.myInstallationThread = ins.Installation(myConfig)
    
    #myCommunicationThread = cascade.ArduinoDriver(gR.myEStats, paths)
    gR.myPreviewThread = log.Logger()
    
    #gR.myVisualizationDG = dG.VisulaizationGateway("localwarmingdev.meteor.com")

    
    

    #operational
    gR.myInstallationThread.start()
    #gR.myCommunicationThread.start()
    #gR.myVisualizationDG.start()
    

    #initiate cmd-control
    cC.ManualControl().cmdloop()
    cC.InstallationControl().cmdloop()
    
    """
    #operational
    gR.myTargetAcquisitionThread.start()
    gR.myTargetAcquisitionThread.join()
    gR.myInstallationThread.stop()
    gR.myCommunicationThread.stop()
    gR.myInstallationThread.join()
    gR.myCommunicationThread.join()
    #gR.myVisualizationDG.stop()
    #gR.myVisualizationDG.join()
    """
    print "done"