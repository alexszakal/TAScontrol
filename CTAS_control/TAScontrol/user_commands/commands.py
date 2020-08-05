import sys
from time import sleep
from time import asctime
from numpy import *
from cmath import sqrt
import pickle
from TAScontrol.others.filePath import *

''' IMPORTS for EMULATOR mode '''
HWtype=pickle.load(open(configDataPath+"HWtype.bin", 'rb'))

if HWtype == 'emulator':
    from ..communication.emulator import startCounting
    from ..communication.emulator import readDetectorStats
    from ..communication.emulator import readDetectorStatus
    from ..communication.emulator import position
    from ..communication.emulator import startMove
    from ..communication.emulator import axisStatus
    from ..communication.emulator import isMoving
    from ..communication.emulator import RSNDcount
    from ..communication.emulator import stopMove
    from ..communication.emulator import read2Ddata
    from ..communication.emulator import sumCountsInROI
elif HWtype == 'ctas':
    from ..communication.tasc import startCounting
    from ..communication.tasc import readDetectorStats
    from ..communication.tasc import readDetectorStatus
    from ..communication.tasc import position
    from ..communication.tasc import startMove
    from ..communication.tasc import axisStatus
    from ..communication.tasc import isMoving
    from ..communication.tasc import RSNDcount
    from ..communication.tasc import stopMove
    from ..communication.tasc import read2Ddata
    from ..communication.tasc import sumCountsInROI

from TAScontrol.properties.sample import *
from TAScontrol.properties.spectrometer import *
from TAScontrol.properties.experiment import *

# Common imports
from ..others.dataFiles import initScanFile
from ..others.dataFiles import writeToLogFile
from ..others.dataFiles import writeToLogFullFile
from ..communication.tascAxisDefs import *

def count(cTime, echoing='on', mode='time'):
    #Counts for a given time value
    #returns the detStat list [monitor, time, counts, sequenceNo, ROIcount].
    detStat=RSNDcount(mode, cTime, echoing='on', writeEnd='off')

    return detStat
    
def count_old(cTime, echoing='on'):
    #Counts for a given time value
    #returns the detStat list [monitor, time, counts, sequenceNo] .
    startCounting('time', cTime*1000)
    sleep(0.5)
    
    if echoing=='on':
        while readDetectorStatus() == 1000000:
            print('Starting!')
    
    detstats=readDetectorStats()    
    while detstats[1]<cTime*1000:
        sleep(0.5)
        detstats=readDetectorStats()
        if echoing=='on':
            print("\r{0} {1} {2} {3}".format(detstats[0], detstats[1], detstats[2], detstats[3]), end=' ')
            sys.stdout.flush()
    return detstats

def readang(axis, echoing='on'):
    #If it is a simple motor
    if axisDictRev.__contains__(axis) == 1:
        posi=position(axis)
        
        if axis==ath:
            if actSpect.scattSign[0,2] == 1:    #Analyzer scatters to positive direction
                posi=posi-actSpect.axisOffsetDict[ axisDictRev[axis]]
                posi=90-posi
            if actSpect.scattSign[0,2] == -1:    #Analyzer scatters to the negative direction
                posi=posi-actSpect.axisOffsetDict[ axisDictRev[axis]]
                posi=-90-posi  
        else:
            posi=posi-actSpect.axisOffsetDict[ axisDictRev[axis]]
        if echoing=='on':
            print(axis+'  '+str(posi))
            return
        return posi
    else:       #It is a complex motor
        if axis=='kf':
            lf=2*actSpect.d_ana*sin( deg2rad(abs(readang(ath, echoing='off'))) )
            kf=2*pi/lf
            return kf
        elif axis=='ki':
            li=2*actSpect.d_monok*sin( deg2rad(readang(monok, echoing='off')))
            ki=2*pi/li
            return ki
        elif axis=='Ef':
            lf=2*actSpect.d_ana*sin( deg2rad(abs(readang(ath, echoing='off'))) )
            Ef=81.808/pow(lf,2)
            return Ef
        elif axis=='Ei':
            li=2*actSpect.d_monok*sin( deg2rad(readang(monok, echoing='off')))
            Ei=81.808/pow(li,2)
            return Ei
        elif axis=='lf':
            lf=2*actSpect.d_ana*sin( deg2rad(abs(readang(ath, echoing='off'))) )
            return lf
        elif axis=='li':
            li=2*actSpect.d_monok*sin( deg2rad(readang(monok, echoing='off')))
            return li
        
    

def readangAll(axis):
    """Read the status and angle of the axis"""
    #TODO: Megirni a readangAll fuggvenyt ha mar megvan a teljes protokoll
    
def rallh():

    #for i in range(0,len(axisDictList)):
    #    if (i%3==0) & (i!=0):     #Start new line
    #        print
    #    print axisDictList[i][0].rjust(10)+'{0:9.2f}'.format(readang(axisDictList[i][1],echoing='off')),
        
    #print "\n\n"
    
    print("\n---------------   Main TAS Angles   ---------------")
    for i in range(8):     #Triple axis angles
        if (i%4==0) & (i!=0):
            print()
        print(axisDictList[i][0].rjust(8)+'{0:7.3f}'.format(readang(axisDictList[i][1],echoing='off')), end=' ')
    print() 
    
    print("\n--------------- Monochromator stage ---------------")
    for i in range(8,11):  
        print(axisDictList[i][0].rjust(8)+'{0:7.3f}'.format(readang(axisDictList[i][1],echoing='off')), end=' ')
    print()
    for i in range(11,13):
        print(axisDictList[i][0].rjust(8)+'{0:7.3f}'.format(readang(axisDictList[i][1],echoing='off')), end=' ')
    print()
   
    print("\n---------------       Slit 1        ---------------")    
    for i in range(13,17): 
        print(axisDictList[i][0].rjust(8)+'{0:7.3f}'.format(readang(axisDictList[i][1],echoing='off')), end=' ')
    print()
    
    print("\n---------------       Slit 2        ---------------") 
    for i in range(17,21): 
        print(axisDictList[i][0].rjust(8)+'{0:7.3f}'.format(readang(axisDictList[i][1],echoing='off')), end=' ')
    print()
        
    print("\n---------------   Sample Translate  ---------------") 
    for i in range(21,23): 
        print(axisDictList[i][0].rjust(8)+'{0:7.3f}'.format(readang(axisDictList[i][1],echoing='off')), end=' ')
    print()
    
    print("\n---------------    Analyzer Stage   ---------------") 
    for i in range(23,27):  
        print(axisDictList[i][0].rjust(8)+'{0:7.3f}'.format(readang(axisDictList[i][1],echoing='off')), end=' ')
    print()

    print("\n---------------      Distances      ---------------") 
    for i in range(27,30):  
        print(axisDictList[i][0].rjust(8)+'{0:7.3f}'.format(readang(axisDictList[i][1],echoing='off')), end=' ')
    print()
    
    print("\n--------------- Analyzer Shielding  ---------------") 
    for i in range(30,32): 
        print(axisDictList[i][0].rjust(8)+'{0:7.3f}'.format(readang(axisDictList[i][1],echoing='off')), end=' ')
    print()

        
    return



def move(axis, targetPos, echoing="on", logging="on", wrend="on"):
    """Move the axis and return when the movement finished"""
    
    ##Check out of bound condition and 'ath' rotation 
    if (bool(axis !='ki') & bool(axis !='kf') & bool(axis !='Ei') & bool(axis !='Ef') & bool(axis !='li') & bool(axis !='lf') ):
        
        if axis==ath:    ### SPECIAL TRANSFORMATION OF ATH
            if actSpect.scattSign[0,2]==1:
                if targetPos >=0:
                    targetPos = 90-targetPos
                else:
                    print('Analyzer scattering sign is positive! Give posivive ath value!')
                    return
            elif actSpect.scattSign[0,2]==-1:
                if targetPos <=0:
                    targetPos = -90-targetPos
                else:
                    print('Analyzer scattering sign is negative! Give negative ath value!')
                    return
            else:
                print('Incorrect scattering Sign value on analyzer!')
                return 

        if axis==detang:    ##Detang SIGN check
            if targetPos<0:
                if actSpect.scattSign[0,2]==1:
                    print('Analyzer scattering sign is positive! Give posivive detang value!')
                    return
            if targetPos>0:
                if actSpect.scattSign[0,2] == -1:
                    print('Analyzer scattering sign is negative! Give negative detang value!')
                    return
        
        if axis==s2th:    ##Detang SIGN check
            if targetPos<0:
                if actSpect.scattSign[0,1]==1:
                    print('Sample scattering sign is positive! Give posivive s2th value!')
                    return
            if targetPos>0:
                if actSpect.scattSign[0,1]==-1:
                    print('Sample scattering sign is negative! Give negative s2th value!')
                    return
                
        if axis==monho:    ##Monho SIGN check
            if targetPos<0:
                if actSpect.scattSign[0,0]==1:
                    print('Monochromator scattering sign is positive! Give posivive monho value!')
                    return
            if targetPos>0:
                if actSpect.scattSign[0,0]==-1:
                    print('Monochromator scattering sign is negative! Give negative monho value!')
                    return
        
        if axis==monok:    ##Monho SIGN check
            if targetPos<0:
                if actSpect.scattSign[0,0]==1:
                    print('Monochromator scattering sign is positive! Give posivive monok value!')
                    return
            if targetPos>0:
                if actSpect.scattSign[0,0]==-1:
                    print('Monochromator scattering sign is negative! Give negative monok value!')
                    return
             
        if  bool(targetPos<actSpect.axisLimitsDict[axisDictRev[axis]][0]) | bool(targetPos > actSpect.axisLimitsDict[axisDictRev[axis]][1]):
            print(axisDictRev[axis] + " targetposition out of bounds ({0}, {1})!".format(actSpect.axisLimitsDict[axisDictRev[axis]][0], actSpect.axisLimitsDict[axisDictRev[axis]][1]))
            return 'outOfBounds' 
    
    ##Write to LogFiles
    if logging == "on":
        commandString=asctime()+": move(axis={0}, targetPos={1}".format(axis,targetPos)
        writeToLogFile(commandString)
        writeToLogFullFile(commandString)
    
    if axis == 'ki':
        qMonok=2*pi/actSpect.d_monok
        if targetPos>2*qMonok:
            print('Target is too high!')
            return
        targThetaMonok=rad2deg(arcsin(qMonok/2/targetPos))*actSpect.scattSign[0,0]
        moveret=move(monok,targThetaMonok, echoing="on", logging="off", wrend="off")
        if moveret == 'outOfBounds':
            return
        moveret=move(monho,2*targThetaMonok, echoing="on", logging="off", wrend="off")
        if moveret == 'outOfBounds':
            return
        return
    if axis=='kf':
        qAnalyzer=2*pi/actSpect.d_ana
        if targetPos>2*qAnalyzer:
            print('Target is too high!')
            return
        targThetaAna=rad2deg(arcsin(qAnalyzer/2/targetPos))*actSpect.scattSign[0,2]
        moveret=move(ath,targThetaAna, echoing="on", logging="off", wrend="off")
        if moveret == 'outOfBounds':
            return
        moveret=move(detang,2*targThetaAna, echoing="on", logging="off", wrend="off")
        if moveret == 'outOfBounds':
            return
        return
    if axis=='Ei':
        lami=sqrt(81.808/targetPos)
        ki=2*pi/lami
        move('ki', ki, echoing="off", logging="off", wrend="off")
        return
    if axis=='Ef':
        lamf=sqrt(81.808/targetPos)
        kf=2*pi/lamf
        move('kf', kf, echoing="off", logging="off", wrend="off")
        return
    if axis=='li':
        move('ki', 2*pi/targetPos, echoing="off", logging="off", wrend="off")
        return
    if axis=='lf':
        move('kf', 2*pi/targetPos, echoing="off", logging="off", wrend="off")
        return
        
    
    if bool(axis == ath):
        if bool(actSpect.scattSign[0,2]==1):
            targetPos=targetPos+actSpect.axisOffsetDict[ axisDictRev[axis]]
        if bool(actSpect.scattSign[0,2]==-1):
            targetPos=targetPos+actSpect.axisOffsetDict[ axisDictRev[axis]]
    else:
        targetPos=targetPos+actSpect.axisOffsetDict[ axisDictRev[axis]]
    
    ##Start moving
    startMove(axis, targetPos)
    #print 'targetPos {0}'.format(targetPos)
    ##Wait until the motor arrives
    currPos=position(axis)
    diff=targetPos-currPos
    sleep(3)         #TODO: Erre a sleep-re nincs szukseg ha a CTL jol valaszo
    while isMoving(axis)==1:
        if echoing == "on":
            print(axisDictRev[axis]+': {0:9.2f}'.format(readang(axis, echoing='off'))+'\r', end=' ')
            sys.stdout.flush()
        sleep(0.5)
    if (echoing == "on"):
        if (wrend=="on"):
            print(axisDictRev[axis]+': {0:9.2f}'.format(readang(axis, echoing='off')))
        if wrend=="off" :
            print('                                                  \r', end=' ')
   # stopMove(axis)  #Stop the movement of the axis
    
    return readang(axis, echoing='off')
    #return  position(axis)


def scan(axis, start, step, end, time, cscanLog='off'):
    """ Scans the axis from start to end with step stepSize. Counts for time """
    #Command Logging
    if cscanLog == 'off':
        if axisDictRev.__contains__(axis):
            commandStringLog='\n'+asctime()+": scan(axis={0}, start={1}, step={2}, end={3}, time={4})".format(axisDictRev[axis], start, step, end, time)
            commandString="scan(axis={0}, start={1}, step={2}, end={3}, time={4})".format(axisDictRev[axis], start, step, end, time)
            angleType='simple'
            axisPrintName=axisDictRev[axis]
        else:
            commandStringLog='\n'+asctime()+": scan(axis={0}, start={1}, step={2}, end={3}, time={4})".format(axis, start, step, end, time)
            commandString="scan(axis={0}, start={1}, step={2}, end={3}, time={4})".format(axis, start, step, end, time)
            angleType='complex'
            axisPrintName=axis
    else:
        commandStringLog=asctime()+": "+cscanLog
        commandString=cscanLog
        axisPrintName=axisDictRev[axis]
        angleType='simple'
    scanFile=initScanFile(commandString)
    writeToLogFile(commandStringLog)
    writeToLogFullFile(commandStringLog)
    
    currpos=start
    #Scan in forward direction
    if start < end:
        scanFor=1
        if step < 0:
            step=step*(-1)
    else:  #Scan backwards
        scanFor=0
        if step > 0:
            step=step*(-1) 
    
    print(" {0}        CNT      CNTROI        MON       TIME     2DFNUM    CNT/MON   Err(CNT/MON)".format(axisPrintName.rjust(9)))
    nextStep=start
    while ((round(nextStep*100)<=round(end*100)) & (scanFor==1)) | ((round(nextStep*100)>=round(end*100)) & (scanFor==0)):
        #print "Moving {0} to {1}".format(axis, nextStep)
        movret=move(axis, nextStep, echoing="off", logging="off")
        if movret == 'outOfBounds':
            return
        detstat=count(time,echoing="off")
        #print 'Detstat in scan:'
        #print detstat
        #Write results to the scanFile and logFullFile
        if angleType=='simple':
            if (detstat [0] == 0) | (detstat[4]==0):
                scanLogLine="{0:10.2f} {1:10} {2:10} {3:10} {4:10} {5:10} {6:10.3f} {7:10.3f}\n".format(readang(axis,echoing='off'),  
                detstat[2], detstat[4], detstat[0], detstat[1], detstat[3], 0.0, 0.0 )
                printLine=scanLogLine
            else:
                scanLogLine="{0:10.2f} {1:10} {2:10} {3:10} {4:10} {5:10} {6:10.3f} {7:10.3f}\n".format(readang(axis,echoing='off'),  
                detstat[2], detstat[4], detstat[0], detstat[1], detstat[3], float(detstat[4])/float(detstat[0]), 
                float(detstat[4])/float(detstat[0])*sqrt(1/float(detstat[4])+1/float(detstat[0])).real  )
                printLine=scanLogLine
        elif angleType=='complex':
            if (detstat [0] == 0) | (detstat[4] == 0):
                scanLogLine="{0:10.2f} {1:10} {2:10} {3:10} {4:10} {5:10} {6:10.3f} {7:10.3f} {8:10.2f} {9:10.2f} {10:10.2f} {11:10.2f} {12:10.2f} {13:10.2f} {14:10.2f} {15:10.2f}\n".format(readang(axis,echoing='off'),  
                detstat[2], detstat[4], detstat[0], detstat[1], detstat[3], 0.0, 0.0,
                readang(monok,'off'), readang(monho,'off'), readang(om,'off'), readang(s2th,'off'),
                readang(ath,'off'), readang(detang,'off'), readang(sgL,'off'), readang(sgU,'off') )
                
                printLine="{0:10.2f} {1:10} {2:10} {3:10} {4:10} {5:10} {6:10.3f} {7:10.3f}\n".format(readang(axis,echoing='off'),  
                detstat[2], detstat[4], detstat[0], detstat[1], detstat[3], 0.0, 0.0)
            else:
                scanLogLine="{0:10.2f} {1:10} {2:10} {3:10} {4:10} {5:10} {6:10.3f} {7:10.3f} {8:10.2f} {9:10.2f} {10:10.2f} {11:10.2f} {12:10.2f} {13:10.2f} {14:10.2f} {15:10.2f}\n".format(readang(axis,echoing='off'),  
                detstat[2], detstat[4], detstat[0], detstat[1], detstat[3], float(detstat[4])/float(detstat[0]), 
                float(detstat[4])/float(detstat[0])*sqrt(1/float(detstat[4])+1/float(detstat[0])).real,
                readang(monok,'off'), readang(monho,'off'), readang(om,'off'), readang(s2th,'off'),
                readang(ath,'off'), readang(detang,'off'), readang(sgL,'off'), readang(sgU,'off')  )
                
                printLine="{0:10.2f} {1:10} {2:10} {3:10} {4:10} {5:10} {6:10.3f} {7:10.3f}\n".format(readang(axis,echoing='off'),  
                detstat[2], detstat[4], detstat[0], detstat[1], detstat[3], float(detstat[4])/float(detstat[0]), 
                float(detstat[4])/float(detstat[0])*sqrt(1/float(detstat[4])+1/float(detstat[0])).real)
        
        print(printLine, end=' ')     
        scanFile[0].write(scanLogLine)
        scanFile[0].flush()
        scanFile[1].write(scanLogLine)
        scanFile[1].flush()
        writeToLogFullFile(scanLogLine)
        
        nextStep=nextStep+step
    
    scanFile[0].close()
    scanFile[1].close()
    print("Scan finished")
      
def cscan(axis, amplitude, step, time):
    #Scans around a central position
    start=readang(axis, echoing='off')-amplitude
    end=start+2*amplitude
    cscLog="cscan(axis={0}, amplitude={1}, step={2}, time={3})".format(axisDictRev[axis],amplitude,step,time)
    scan(axis,start,step,end,time, cscanLog=cscLog)
    return

def setORef(order, h, k, l, E, omega, phi, mu, nu):
    #Set the primary reflection of the sample
    #params: order:(0,1) h k l E omega 2Theta, mu nu
    actSample.ORef[order]=[h,k,l,E, omega, phi, mu, nu]
    actSample.pVec[order,0:3]=matrix('{0} {1} {2}'.format(h,k,l))
    actSample.save()

def setCell(a,b,c, alpha, beta, gamma):
    #Set the cell parameters of the Sample,
    actSample.a=a
    actSample.b=b
    actSample.c=c
    
    actSample.alpha=alpha
    actSample.beta=beta
    actSample.gamma=gamma
    
    actSample.save()
    
def setPlane(vec1, vec2):
    print('matrix vec1:')
    print(matrix(vec1))
    print('matrix vec2:')
    print(matrix(vec2))
    
    actSample.pVec[0]=matrix(vec1)
    actSample.pVec[1]=matrix(vec2)
    print()
    print('New plane set:')
    print('    H        K       L')
    print(' {0:7.2f} {1:7.2f} {2:7.2f}'.format(actSample.pVec[0,0], actSample.pVec[0,1], actSample.pVec[0,2] ))
    print(' {0:7.2f} {1:7.2f} {2:7.2f}'.format(actSample.pVec[1,0], actSample.pVec[1,1], actSample.pVec[1,2] ))
    print()
    actSample.save()

def printSample():
    #Print the actual Sample properties
    print() 
    print('NAME: ' +actSample.name)
    print('a={0} b={1} c={2}'.format(actSample.a, actSample.b, actSample.c))
    print('alpha={0} beta={1} gamma={2}\n'.format(actSample.alpha, actSample.beta, actSample.gamma))
    print('Orienting Reflections:')
    print('    h      k      l       E       om       Th2     SGL     SGU')
    print('{0:7.2f} {1:6.2f} {2:6.2f} {3:7.2f} {4:8.2f} {5:8.2f} {6:7.2f} {7:7.2f}'.format(actSample.ORef[0][0], 
    actSample.ORef[0][1], actSample.ORef[0][2], actSample.ORef[0][3], actSample.ORef[0][4], actSample.ORef[0][5],
    actSample.ORef[0][6], actSample.ORef[0][7] ))
    print('{0:7.2f} {1:6.2f} {2:6.2f} {3:7.2f} {4:8.2f} {5:8.2f} {6:7.2f} {7:7.2f}'.format(actSample.ORef[1][0], 
    actSample.ORef[1][1], actSample.ORef[1][2], actSample.ORef[1][3], actSample.ORef[1][4], actSample.ORef[1][5],
    actSample.ORef[1][6], actSample.ORef[1][7] ))
    print('\n In-plane vectors:')
    print('    H        K       L')
    print(' {0:7.2f} {1:7.2f} {2:7.2f}'.format(actSample.pVec[0,0], actSample.pVec[0,1], actSample.pVec[0,2] ))
    print(' {0:7.2f} {1:7.2f} {2:7.2f}'.format(actSample.pVec[1,0], actSample.pVec[1,1], actSample.pVec[1,2] ))
    print('\n UB matrix:')
    print(actSample.UB) 
    print()

def printSpect():
    #Print the actual Spectrometer configuration
    print()
    print('Monochromator d-spacing:  {0}'.format(actSpect.d_monok))
    print('Analyzer d-spacing:       {0}'.format(actSpect.d_ana))
    print()
    print('Collimators:   {0}   {1}   {2}   {3}'.format(actSpect.colli[0], actSpect.colli[1], actSpect.colli[2], actSpect.colli[3]))
    print() 
    print('ROI settings:   Xmin: {0}   Xmax: {1}   Ymin:{2}   Ymax:{3}'.format(actSpect.ROI[0], actSpect.ROI[1], actSpect.ROI[2], actSpect.ROI[3]))
    print()
    print('Locked:      {0} @ {1} A^-1'.format(actSpect.lock[0], actSpect.lock[1]))
    print() 
    print('Scattaring signs:   Monok: {0}   Sample: {1}   Analyzer: {2}'.format(actSpect.scattSign[0,0], actSpect.scattSign[0,1], actSpect.scattSign[0,2]))
    
def setMonok(dval):
    if bool(type(dval) != float) & bool(type(dval) != int):
        print('Error: Wrong type of input argument')
        return
    
    actSpect.d_monok=dval
    actSpect.save()

def setAnal(dval):
    if bool(type(dval) != float) & bool(type(dval) != int):
        print('Error: Wrong type of input argument')
        return
    actSpect.d_ana=dval
    actSpect.save()
    
def setCollimators(cvals):
    if (type(cvals) != list):
        print('Error: list argument expected')
        return
    if cvals.__len__() != 4 :
        print('Error: argument length is not 4 !')
        return
    actSpect.colli=cvals
    actSpect.save()
    
def setROI(ROI):
    if (type(ROI) != list):
        print('Error: list argument expected')
        return
    if ROI.__len__() != 4 :
        print('Error: argument length is not 4 !')
        return
    actSpect.ROI=ROI
    actSpect.save()
    
def setLock(lock):
    if (type(lock) != list):
        print("Error: list argument expected: ['ki' or 'kf', value]")
        return
    if lock.__len__() != 2 :
        print('Error: argument length is not 2 !')
        return
    if bool(lock[0] != 'ki') & bool(lock[0] != 'kf'):
        print("Error: 'ki' or 'kf' can be locked only!")
        return
    if bool(type(lock[1]) != float) & bool(type(lock[1]) != int):
        print('Error: value must be float or int type!')
        return
    
    actSpect.lock=lock
    actSpect.save()
    
def setScattSigns(sign):
    if type(sign) != list:
        print("Error: list argument expected!")
        return
    for i in range(3):
        if bool(sign[i]!=1) & bool(sign[i]!=-1) :
            print('Sign must be 1 or -1!')
            return
    
    actSpect.scattSign=matrix(sign)
    actSpect.save()
    
def printOffsets():
    print("\n---------------   Main TAS Angle OFFSETS   ---------------")
    for i in range(8):     #Triple axis angles
        if (i%4==0) & (i!=0):
            print()
        print(axisDictList[i][0].rjust(8)+'{0:7.3f}'.format(actSpect.axisOffsetDict[ axisDictList[i][0] ] ), end=' ')
    print() 
    
    print("\n--------------- Monochromator stage OFFSETS---------------")
    for i in range(8,11):  
        print(axisDictList[i][0].rjust(8)+'{0:7.3f}'.format(actSpect.axisOffsetDict[ axisDictList[i][0] ]), end=' ')
    print()
    for i in range(11,13):
        print(axisDictList[i][0].rjust(8)+'{0:7.3f}'.format( actSpect.axisOffsetDict[ axisDictList[i][0] ] ), end=' ')
    print()
   
    print("\n---------------       Slit 1 OFFSETS       ---------------")    
    for i in range(13,17): 
        print(axisDictList[i][0].rjust(8)+'{0:7.3f}'.format( actSpect.axisOffsetDict[ axisDictList[i][0] ] ), end=' ')
    print()
    
    print("\n---------------       Slit 2 OFFSETS       ---------------") 
    for i in range(17,21): 
        print(axisDictList[i][0].rjust(8)+'{0:7.3f}'.format( actSpect.axisOffsetDict[ axisDictList[i][0] ] ), end=' ')
    print()
        
    print("\n---------------   Sample Translate OFFSETS  ---------------") 
    for i in range(21,23): 
        print(axisDictList[i][0].rjust(8)+'{0:7.3f}'.format( actSpect.axisOffsetDict[ axisDictList[i][0] ] ), end=' ')
    print()
    
    print("\n---------------    Analyzer Stage  OFFSETS   ---------------") 
    for i in range(23,27):  
        print(axisDictList[i][0].rjust(8)+'{0:7.3f}'.format( actSpect.axisOffsetDict[ axisDictList[i][0] ] ), end=' ')
    print()

    print("\n---------------      Distances  OFFSETS    ---------------") 
    for i in range(27,30):  
        print(axisDictList[i][0].rjust(8)+'{0:7.3f}'.format( actSpect.axisOffsetDict[ axisDictList[i][0] ] ), end=' ')
    print()
    
    print("\n--------------- Analyzer Shielding OFFSETS  ---------------") 
    for i in range(30,32): 
        print(axisDictList[i][0].rjust(8)+'{0:7.3f}'.format( actSpect.axisOffsetDict[ axisDictList[i][0] ] ), end=' ')
    print()
        
    return    

def printLimits():
    print("\n---------------   Main TAS Angle LIMITS   ---------------")
    for i in range(8):     #Triple axis angles
        if (i%4==0) & (i!=0):
            print()
        print(axisDictList[i][0].rjust(8)+'{0:12}'.format(actSpect.axisLimitsDict[ axisDictList[i][0] ] ), end=' ')
    print() 
    
    print("\n--------------- Monochromator stage LIMITS  ---------------")
    for i in range(8,11):  
        print(axisDictList[i][0].rjust(8)+'{0:12}'.format(actSpect.axisLimitsDict[ axisDictList[i][0] ]), end=' ')
    print()
    for i in range(11,13):
        print(axisDictList[i][0].rjust(8)+'{0:12}'.format( actSpect.axisLimitsDict[ axisDictList[i][0] ] ), end=' ')
    print()
   
    print("\n---------------       Slit 1 LIMITS       ---------------")    
    for i in range(13,17): 
        print(axisDictList[i][0].rjust(8)+'{0:12}'.format( actSpect.axisLimitsDict[ axisDictList[i][0] ] ), end=' ')
    print()
    
    print("\n---------------       Slit 2 LIMITS       ---------------") 
    for i in range(17,21): 
        print(axisDictList[i][0].rjust(8)+'{0:12}'.format( actSpect.axisLimitsDict[ axisDictList[i][0] ] ), end=' ')
    print()
        
    print("\n---------------   Sample Translate LIMITS  ---------------") 
    for i in range(21,23): 
        print(axisDictList[i][0].rjust(8)+'{0:12}'.format( actSpect.axisLimitsDict[ axisDictList[i][0] ] ), end=' ')
    print()
    
    print("\n---------------    Analyzer Stage  LIMITS   ---------------") 
    for i in range(23,27):  
        print(axisDictList[i][0].rjust(8)+'{0:12}'.format( actSpect.axisLimitsDict[ axisDictList[i][0] ] ), end=' ')
    print()

    print("\n---------------      Distances  LIMITS    ---------------") 
    for i in range(27,30):  
        print(axisDictList[i][0].rjust(8)+'{0:12}'.format( actSpect.axisLimitsDict[ axisDictList[i][0] ] ), end=' ')
    print()
    
    print("\n--------------- Analyzer Shielding LIMITS  ---------------") 
    for i in range(30,32): 
        print(axisDictList[i][0].rjust(8)+'{0:12}'.format( actSpect.axisLimitsDict[ axisDictList[i][0] ] ), end=' ')
    print()
        
    return 
    
def setOffset(axis, value):
    if axisDictRev.__contains__(axis) != 1:
        print('Give correct motor name!!!')
        return
    if bool(type(value) != float) & bool(type(value) != int):
        print('Give int or floating value offset!')
        return
        
    actSpect.axisOffsetDict[axisDictRev[axis]]=value
    actSpect.save()

def setLimits(axis, value):
    if axisDictRev.__contains__(axis) != 1:
        print('Give correct motor name!!!')
        return
    if bool( type(value) != list ):
        print('List is expected as second argument [MinVal, Maxval]')
        return
    if value.__len__() != 2:
        print('Second argument needs two elements  [MinVal, Maxval]')
        return
    
    actSpect.axisLimitsDict[axisDictRev[axis]]=value
    actSpect.save()

####################################
##    EXPERIMENT COMMANDS         ##
####################################
    
def setTitle(title):
    actExp.title=title
    actExp.save()

def setUser(user):
    actExp.user=user
    actExp.save()
    
def printExp():
    print()
    print('Experiment title: {0}'.format(actExp.title))
    print()
    print('User: {0}'.format(actExp.user))
    print()
    
def setSampleName(name):
    #Set the sample name
    actSample.name=name
    actSample.save()

def refreshUB():
    #refresh the UB matrix of the sample
    actSample.refreshUB()
    actSample.save()

def lockK(side, value='actual'):
    #Locks 'ki' or 'kf' at a given k value or at the actual value
    if side == 'ki':
        if value=='actual':
            kival=pi/actSpect.d_monok*sin(deg2rad(readang(monok,'off') ))
            print('Locking actual k_i value at {0} A^-1'.format(kival))
            actSpect.lock=['ki', kival]
        else:
            print('Locking k_i at {0} A^-1'.format(value))
            actSpect.lock=['ki', value]
    elif side == 'kf':
        if value=='actual':
            kfval=pi/actSpect.d_ana*sin(deg2rad(readang(ath,'off') ))
            print('Locking actual k_f value at {0} A^-1'.format(kfval))
            actSpect.lock=['kf', kfval]
        else:
            print('Locking k_f at {0} A^-1'.format(value))
            actSpect.lock=['kf', value]
    else:
        print("Type 'ki' or 'kf' as first argument!!")
    
    actSpect.save()
    
def calcHKLE(h, k, l, E):
    #calculate the A1, A2, A3, A4, A5, A6 and mu,nu angles for a given reflection
    #uses the actual sample
    retvals=actSpect.calcHKLE(h, k, l, E)
    return retvals

def mvhkl(hklE, simulation='off'):
    #Moves the spectrometer to the given hklE point
    targAngles=calcHKLE(hklE[0], hklE[1], hklE[2], hklE[3])
        
    angleList=(monok, monho, om, s2th, ath, detang, sgU, sgL)
    if simulation == 'off':
        for i in range(8):
            actPos=readang(angleList[i], 'off')
            if abs(targAngles[i]-actPos) > 0.01 :
                movret=move(angleList[i], targAngles[i], echoing="on", logging="off", wrend="off" )
                if movret == 'outOfBounds':
                    return
    elif simulation == 'on':
        print('Simulation mode')
        return 1
    else:
        print('Wrong simulation parameter in mvhkl(): ' + simulation)
    
    
def schkl(start, step, np, value, type='time', simulation='off'):
    #Do a scan in reciprocal space
    
    #write the command in the Logfiles
    if type=='time':
        commandStringLog='\n'+asctime()+": schkl(start={0}, step={1}, np={2}, time={3})".format(start, step, np, value)
        commandString="schkl(start={0}, step={1}, np={2}, time={3})".format(start, step, np, value)
    elif type=='mon':
        commandStringLog='\n'+asctime()+": schkl(start={0}, step={1}, np={2}, mon={3})".format(start, step, np, value)
        commandString="schkl(start={0}, step={1}, np={2}, mon={3})".format(start, step, np, value)
    else:
        print("Error in schkl(). Give 'mon' or 'time' as counting type!")
        return
    
    writeToLogFile(commandStringLog)
    writeToLogFullFile(commandStringLog)
    #Write the header of the scanfile
    scanFile=initScanFile(commandString)
    
    #go through the points and count for the given value
    print("    H      K       L      E       CNT     CNTROI    MON       TIME   2DFNUM    CNT/MON   Err(CNT/MON)")

    for i in range(0,np):
        targHKLE=(start[0]+i*step[0], start[1]+i*step[1], start[2]+i*step[2], start[3]+i*step[3])
        
        #Move spectrometer
        if simulation == 'off':
            mvhkl(targHKLE)
        elif simulation == 'on':
            mvhkl(targHKLE, simulation='on')
        else:
            print('Wrong simulation argument in schkl() function: ' + simulation)
            
        #count for the given amount of time / moonitor
        detstat=count(value,echoing="off")
    
        scanFile[0].write('{0:7.4f} {1:7.4f} {2:7.4f} {3:6.2f} {4:8} {5:7.2f} {6:8} {7:8} {8:8} {9:6.2f} {10:6.2f} {11:6.2f} {12:6.2f} {13:6.2f} {14:6.2f} {15:6.2f} {16:6.2f}\n'.format( 
        double(targHKLE[0]), double(targHKLE[1]), double(targHKLE[2]), double(targHKLE[3]), 
        detstat[0], detstat[1], detstat[2], detstat[4], detstat[3], 
        readang(monok, 'off'), readang(monho, 'off'), readang(om, 'off'), readang(s2th, 'off'),
        readang(ath, 'off'), readang(detang, 'off'), readang(sgL, 'off'), readang(sgU, 'off') ) )
        
        scanFile[1].write('{0:7.4f} {1:7.4f} {2:7.4f} {3:6.2f} {4:8} {5:7.2f} {6:8} {7:8} {8:8} {9:6.2f} {10:6.2f} {11:6.2f} {12:6.2f} {13:6.2f} {14:6.2f} {15:6.2f} {16:6.2f}\n'.format( 
        double(targHKLE[0]), double(targHKLE[1]), double(targHKLE[2]), double(targHKLE[3]), 
        detstat[0], detstat[1], detstat[2], detstat[4], detstat[3],  #monitor, time, count, ROI, seqNum
        readang(monok, 'off'), readang(monho, 'off'), readang(om, 'off'), readang(s2th, 'off'),
        readang(ath, 'off'), readang(detang, 'off'), readang(sgL, 'off'), readang(sgU, 'off') ) )
        
        scanFile[0].flush()
        scanFile[1].flush()
        #print "   H        K        L        E     CNT    CNTROI   MON  TIME  2DFNUM    CNT/MON  Err(CNT/MON)"
        print('{0:7.4f} {1:7.4f} {2:7.4f} {3:6.2f} {4:8} {5:8} {6:8} {7:8.2} {8:8}\n'.format( 
        double(targHKLE[0]), double(targHKLE[1]), double(targHKLE[2]), double(targHKLE[3]), 
        detstat[2], detstat[4], detstat[0], detstat[1], detstat[3] )) #CNT, ROICNT, monitor, time, seqnum
    #write the result to the log file
     
def writeLog(logString):
    if type(logString) != str:
        print('Give string argument!')
        return
    
    writeToLogFile('#############  USER COMMENT  #########################')
    writeToLogFullFile('#############  USER COMMENT  #########################')
    
    writeToLogFile('  '+logString)
    writeToLogFullFile('  '+logString)

    writeToLogFile('######################################################')
    writeToLogFullFile('######################################################')
















 
    
    

