"""
from  coreFunctionality import Configuration

configuration = Configuration('config.csv')
print configuration.getEmitterConfig()
"""
"""
from coreFunctionality import Configuration as cF

myConfig = cF.Configuration('../config.csv')

print myConfig.getEmitterConfig()
"""
"""
def testFunction (x):
    y = ( 1, 2, 3)
    return y[x]


try:
    print testFunction(3)
except:
    print 'exception'
"""
"""
import math
from coreFunctionality import VectorMath as vm

print vm.angleBetween2D((1,0),(2,-0.1))
print math.pi * 1.5 + math.atan(2/0.1)
print vm.angle2DVector((2,-0.0001))
print math.pi
"""
"""
num = 123341
print num
num = "{0:.2f}".format(num)
print num
"""

"""
def printArray(emitterStates):
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

myList = ( ( (0, 14.2324), (0, -12), (1, 12.1), (0, -12), (1, 12.1), (0, -12), (1, 12.1) ), ( (0, 14.2324), (0, 12), (1, 12.1), (0, 12), (0, 12), (0, 12), (0, 12), (0, 12), (0, 12), (0, 12), (0, 12) ) )

printArray(myList)
"""

from Tkinter import *

class App:

    def __init__(self, master):

        frame = Frame(master)
        frame.pack()

        self.button = Button(
            frame, text="QUIT", fg="red", command=frame.quit
            )
        self.button.pack(side=LEFT)

        self.hi_there = Button(frame, text="Hello", command=self.say_hi)
        self.hi_there.pack(side=LEFT)

    def say_hi(self):
        print "hi there, everyone!"

root = Tk()

app = App(root)

root.mainloop()
root.destroy() # optional; see description below



"""MAIN
from coreFunctionality import Configuration
from coreFunctionality import Installation
import threading
import time

myConfig = Configuration.Configuration("../config.csv")
#myInstallation = Installation.Installation(myConfig)
myThread = Installation.Installation(myConfig)
print "thread defined"
myThread.start()
print "thread started"
#myInstallation.stopOperation()
time.sleep(5)
myThread.stop()
print "stop issued"
myThread.join()
print "done"
"""