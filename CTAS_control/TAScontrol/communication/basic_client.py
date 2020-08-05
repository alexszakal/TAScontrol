# Echo client program
#EZ ITT A JATSZOTER

import socket
from .tasc import position
from .tasc import read2Ddata
from .tasc import startCounting
from .tasc import readDetectorStats
from .tasc import sumCountsInROI
from .tasc import readDetectorStatus

#data=readDetectorStatus()
#print data

posi=position(str(7))
print('Position of '+str(7)+' motor: '+str(posi))

#counts=read2Ddata()
#sumCounts=sumCountsInROI(counts, 1,128, 1,128)
#print 'SummedCounts '+str(sumCounts)

#startCounting('time', 20000)

#for i in range(0, 5):
#    detstats=readDetectorStats()
#    print 
    
#for i in range(0,4):
#    print detstats[i]