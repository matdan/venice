'''
Created on May 8, 2014

@author: Matthias
'''

import threading

remote_ip='128.30.79.98'
port = 7000
saveConfigFilename = 'config.csv'
eSpacing = 235
rSpacing = 1829

myEStats = None
lockMyEstates = threading.Lock()
myTargets = {}
lockMyTargets = threading.Lock()
newTargetsFlag = threading.Event()
emitterUpdatedFlag = threading.Event()

directCommand = {}
lockDirectCommand = threading.Lock()
newCommandFlag = threading.Event()

saveConfigFlag = threading.Event()
lockSaveConfigFilename = threading.Lock()