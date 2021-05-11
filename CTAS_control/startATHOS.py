from time import sleep
import sys
from collections import OrderedDict
import pickle
import numpy
from TAScontrol.others.filePath import *

global HWtype
HWtype='athos'      # 'emulator' or 'ctas'
pickle.dump(HWtype, open(configDataPath+'HWtype.bin','wb') )

from TAScontrol.user_commands.commands import count
from TAScontrol.user_commands.commands import readang
from TAScontrol.user_commands.commands import rallh
from TAScontrol.user_commands.commands import scan
from TAScontrol.user_commands.commands import cscan
from TAScontrol.user_commands.commands import move

#Commands for sample and orientation definition
from TAScontrol.user_commands.commands import setORef
from TAScontrol.user_commands.commands import setPlane
from TAScontrol.user_commands.commands import setCell
from TAScontrol.user_commands.commands import printSample
from TAScontrol.user_commands.commands import setSampleName
from TAScontrol.user_commands.commands import refreshUB

#Commands connected to the spectrometer modification
from TAScontrol.user_commands.commands import printSpect
from TAScontrol.user_commands.commands import setAnal
from TAScontrol.user_commands.commands import setMonok
from TAScontrol.user_commands.commands import setCollimators
from TAScontrol.user_commands.commands import setROI
from TAScontrol.user_commands.commands import setScattSigns
from TAScontrol.user_commands.commands import setLock
from TAScontrol.user_commands.commands import setLimits
from TAScontrol.user_commands.commands import setOffset
from TAScontrol.user_commands.commands import printOffsets
from TAScontrol.user_commands.commands import printLimits
from TAScontrol.user_commands.commands import lockK

from TAScontrol.user_commands.commands import printExp
from TAScontrol.user_commands.commands import setTitle
from TAScontrol.user_commands.commands import setUser

from TAScontrol.user_commands.commands import writeLog

#Commands for movement in 4D (h,k,l,E) space
from TAScontrol.user_commands.commands import calcHKLE
from TAScontrol.user_commands.commands import mvhkl
from TAScontrol.user_commands.commands import schkl


from TAScontrol.communication.tascAxisDefs import *            #Axis names
from TAScontrol.properties.sample import *                     #Sample class and sctSample instanc
from TAScontrol.properties.spectrometer import *               #Spectrometer class and actSpect instance
from TAScontrol.properties.experiment import *

print("\n\n *** TAS Control Software Started ***")
print("Initializing the connection to Servers...")
if HWtype == 'ctas':
    from TAScontrol.communication.tascCommSockets import *    #Connects to the server
print("Connected to servers\n")
print("Current motor positions:")
rallh()
print("\n\n")
#TMP Imports
#from TAScontrol.communication.tasc import readDetectorStats
#from TAScontrol.communication.tasc import startCounting  
#from TAScontrol.communication.tasc import axisStatus
#from TAScontrol.communication.tasc import startMove
#from TAScontrol.communication.tasc import position
#from TAScontrol.communication.tasc import read2Ddata

def nightRun():
    schkl([1.95,1.95,0,-5],[0,0,0,-0.25],37,90)
    schkl([2.05,2.05,0,-5],[0,0,0,-0.25],37,90)
    
    schkl([2,2,0.1,-6],[0,0,0,0.25],49,90)
    schkl([2,2,-0.1,-6],[0,0,0,0.25],49,90)
    
    schkl([2,2,0.15,-4],[0,0,0,-0.25],25,90)
    schkl([2,2,-0.15,-4],[0,0,0,-0.25],25,90)
    

    
