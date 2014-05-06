'''
Created on May 5, 2014

@author: Matthias
'''

import Tkinter as tk
import threading


class GUI(threading.Thread):
    '''
    classdocs
    '''


    def __init__(self, logger):#, updateGUI, emitterStates_lock):
        '''
        Constructor
        '''
        super(GUI, self).__init__()
        self.root = tk.Tk()
        self.status = tk.Label(self.root, text= "", font="Courier")
        self.status.pack()
        
        self.logger = logger
        #self.updateGUI = updateGUI
        #self.emitterStates_lock = emitterStates_lock
        
    def run(self):
        print "gui running"
        self.update_status()
        self.root.after(1000, self.update_status())
        self.root.mainloop()
        
    
    def update_status(self):
        print "status updating"
        # If not, then just add a "." on the end
        current_status = self.generateOutput(self.logger.getEmitterList())
        
        # Update the message
        self.status.configure( text = current_status )
    
    def generateOutput(self, emitterStates):
        output = ""
        for emitterRow in emitterStates:
            output += (10*len(emitterRow)+1)*"-"+"\n"
            entry = ""
            for i in range(len(emitterRow)):
                entry += "|" + "{0:.2f}".format(emitterRow[i][1]).rjust(8, " ")+" "
            entry += "|\n"
            entry += (10*len(emitterRow)+1)*"-"+"\n"
            for i in range(len(emitterRow)):
                entry += "|" + "{0:.0f}".format(emitterRow[i][0]).center(9, " ")
            entry += "|"
            output += entry + "\n"
            output += (10*len(emitterRow)+1)*"-"+"\n"
        return output