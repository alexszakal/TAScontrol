from time import sleep
import sys
from collections import OrderedDict
import pickle
import numpy

global HWtype
HWtype='emulator'
pickle.dump(HWtype, open('/home/szakal/Dropbox/mainPy/HWtype.bin','wb') )

from TAScontrol.user_commands.commands import count
from TAScontrol.user_commands.commands import readang
from TAScontrol.user_commands.commands import rallh
from TAScontrol.user_commands.commands import scan
from TAScontrol.user_commands.commands import move
from TAScontrol.user_commands.commands import cscan

#Commands for sample and orientation definition
from TAScontrol.user_commands.commands import setORef
from TAScontrol.user_commands.commands import setCell
from TAScontrol.user_commands.commands import printSample
from TAScontrol.user_commands.commands import setSampleName
from TAScontrol.user_commands.commands import refreshUB

#Commands for movement in 4D (h,k,l,E) space
from TAScontrol.user_commands.commands import lockK
from TAScontrol.user_commands.commands import calcHKLE
from TAScontrol.user_commands.commands import mvhkl
from TAScontrol.user_commands.commands import schkl


print "\n\n *** TAS Control Software Started ***"
print "Initializing the connection to Servers..."
from TAScontrol.communication.tascAxisDefs import *            #Axis names
from TAScontrol.properties.sample import *                     #Sample class and sctSample instanc
from TAScontrol.properties.spectrometer import *               #Spectrometer class and actSpect instance
from TAScontrol.properties.experiment import *

#from TAScontrol.communication.tascCommSockets import *    #Connects to the server
print "Connected to servers\n"
print "Initializing spectrometer"

#Wrappers of spectrometer commands:
print "Sample name:"
print actSample.name

print "Current motor positions:"
rallh()
print "\n\n"

#   EZEKET A VEGLEGESBE IS AT KELL TENNI!!!!!!!





#   EZEKET NEM KELL ATTENNI A VEGLEGES FAJLBA !!!!
if HWtype == 'emulator':
#Initialize motor movement register
    movingAxes=OrderedDict([ ('mvfoc',0), ('monok',0), ('monho',0),\
    ('s2th',0),('om',0),('ath',0),('sadist',0),('detang',0),\
    ('mtrX',0), ('mtrY',0), ('mgL',0), ('mgU',0), ('s1X', 0),\
    ('s1Y',0), ('s1L',0), ('s1U',0), ('s2X',0), ('s2Y',0),\
    ('s2L',0), ('s2U',0), ('strX',0), ('strY',0), ('agU',0),\
    ('agL',0), ('antrX', 0), ('antrY',0), ('angU',0), ('angL',0),\
    ('detdist',0), ('msdist',0), ('anShRot', 0), ('anShLift', 0),\
    ('sgL', 0), ('sgU', 0)])
    pickle.dump(movingAxes, open("/home/szakal/Dropbox/mainPy/movingAxes.bin", "wb"))

#Initialize detector registers

    detectorData=numpy.zeros((128,128))
    pickle.dump(detectorData, open("/home/szakal/Dropbox/mainPy/detectorData.bin", "wb"))

    detStats=[0, 0, 0, 10000, 0]
    pickle.dump(detStats, open('/home/szakal/Dropbox/mainPy/detStats.bin', 'wb'))


#TMP Imports
#from TAScontrol.communication.tasc import readDetectorStats
#from TAScontrol.communication.tasc import startCounting  
#from TAScontrol.communication.tasc import axisStatus
#from TAScontrol.communication.tasc import startMove
#from TAScontrol.communication.tasc import position
#from TAScontrol.communication.tasc import stopMove