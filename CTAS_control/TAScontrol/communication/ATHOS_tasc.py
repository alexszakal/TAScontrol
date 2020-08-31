import socket
import numpy
import sys
import _thread
import math
from time import sleep

from .tascAxisDefs import *
from TAScontrol.properties.spectrometer import *
from TAScontrol.others.filePath import *

import pickle

def position(axis):
    #Get the position of a motor 
    #motname is string
    #returns the position as floating point

    statusSocket.sendall('getPos -a '+axis)
    data = statusSocket.recv(4096)
    return float(data)

def isMoving(axis):
    #Determine if an axis is moving
    #returns 0->not moving
    #        1-> moving
    statusSocket.sendall('isMoving -a '+axis)
    data = statusSocket.recv(4096)
    var = 0
    if data: var = 1
    return var
    
def axisStatus(axis):
    """Reads the status of an axis"""

    msg='getStatus -a' + axis
    print('Message:\n' + msg + '\r\n')
    statusSocket.sendall(msg)
    data = statusSocket.recv(4096)
    print('Reply:\n'+data)
    # depending on the data tipe
    # data = data.replace(',',';')
    # data = data.replace('=',';')
    # dataParts = data.split(';')
    # return dataParts[4]
    return data
    
def startMove(axis, targetPos):
    msg = 'move -a ' + axis + ' -t ' + targetPos
    
    commandSocket.setblocking(0)
    try:
        commandSocket.recv(4096)   ##Az eddigi beragadt valaszok kiszurese
    except:
        pass
    commandSocket.setblocking(1)
    
    commandSocket.sendall(msg)
    data=""
    while data == '':
        data = data + commandSocket.recv(4096)
    if data == 'ACK':
        return "moveStarted"
    else:
        print("Motor move error on "+axis+" axis: "+data)
        return "Error" 
        
    
def startCounting(mode, value):
    #Start counting
    #mode='time' or mode='monitor'
    #value is counting time[ms] or the monitor value
    
    if mode == 'time':
        commandSocket.sendall('timeLimit '+str(value))
        print('StartDAQ,timelimit='+str(value)+';&\r\n')
    elif mode == 'monitor':
        commandSocket.sendall('monitorLimit'+str(value))
    else:
        print('startCounting error. Give correct mode! Mode given: ' + mode)
         
    data = commandSocket.recv(4096)
    print("startCount Reply:"+data)
    #print "DAQStart reply:"
    #print data
    
    if data == '0':
        #print 'DAQ started'
        return 1
    else:
        print('DAQ start error! Message: '+data)
        return 0
    

def read2Ddata():
    detector=pickle.load(open(emulatorPath+"detectorData.bin", "rb"))
    
    return detector

def readDetectorStats():
    #returns the [monitor, time, counts, seq#] in an array
    
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.connect((statusHOST, statusPORT))
    statusSocket.sendall('GetResult;\r\n')
    print('GetResult;')
    data = statusSocket.recv(4096)
    print("DetStat reply: " + data)
    if data.find(';') == -1:
        statusSocket.recv(4096)
        
    dataVals=data.replace(',',';').replace('=',';').split(';')
    
    retval=numpy.zeros(4)
    retval[0]=dataVals[4]
    retval[1]=dataVals[6]
    retval[2]=dataVals[8]
    retval[3]=0
    
    return retval
    
def sumCountsInROI(data, xmin, xmax, ymin, ymax):
    sumCounts=0
    
    for i in range(xmin-1, xmax):
        for j in range(ymin-1, ymax):
            sumCounts=sumCounts + data[i,j]
    return sumCounts
    
def readDetectorStatus():
    #returns the status code of the DAQ system
    # if measurement is running  code=0 000 000
    # if measurement is finished code=1 000 000
    
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.connect((statusHOST, statusPORT))
    statusSocket.sendall('GetDAQStatus;\r\n')
    print('GetDAQStatus;')
    data = statusSocket.recv(4096)
    print('GetDAQStatus Reply:'+data)
    if data.find(";")==-1:
        statusSocket.recv(4096)
    
    data=data.replace(',',';')
    data=data.replace('=',';')
    dataVals=data.split(';')
    
    #print data
    return dataVals[4]

def detectorEmulator(mode, value):
    #Load detStats
    succ=0
    while succ == 0:
        try:
            detStats=pickle.load(open(emulatorPath+"detStats.bin", "rb"))
            succ=1
        except:
            pass
    
    detStats=[0, 0, 0, detStats[3]+1, 1]  #[ido count monitor fajlnev running]
    pickle.dump(detStats, open(emulatorPath+"detStats.bin", "wb"))

    #Zero detectorData, save it
    detectorData=numpy.zeros((128,128))
    pickle.dump(detectorData, open(emulatorPath+"detectorData.bin", "wb"))
    
    mean=[64,64]
    cov=[[15,0],[0,20]]
            
    #Emulate with random distribution in the center (write detStats, detectorData)
    if mode == 'time':
        while detStats[0] < value:
            #Sorsolunk random beuteseke1
            x,y=numpy.random.multivariate_normal(mean,cov,200).T
            for i in range(0,200):
                xcoord=math.floor(x[i])
                ycoord=math.floor(y[i])
                if xcoord<0:
                    xcoord=0
                if xcoord>127:
                    xcoord=127
                if ycoord<0:
                    ycoord=0
                if ycoord>127:
                    ycoord=127
                detectorData[xcoord, ycoord] = detectorData[xcoord, ycoord] + 1
            detStats[0]=detStats[0]+500     #time
            detStats[1]=detStats[1]+200   #count
            detStats[2]=detStats[2]+1000  #monitor
            pickle.dump(detStats, open(emulatorPath+"detStats.bin", "wb"))
            pickle.dump(detectorData, open(emulatorPath+"detectorData.bin", "wb"))
            sleep(0.4)
        detStats[4]=0
        pickle.dump(detStats, open(emulatorPath+"detStats.bin", "wb"))
        
    elif mode == 'monitor':
        while detstats[2] < value:
            #Sorsolunk random beuteseke1
            x,y=numpy.random.multivariate_normal(mean,cov,200).T
            for i in range(0,200):
                xcoord=math.floor(x[i])
                ycoord=math.floor(y[i])
                if xcoord<0:
                    xcoord=0
                if xcoord>127:
                    xcoord=127
                if ycoord<0:
                    ycoord=0
                if ycoord>127:
                    ycoord=127
                detectorData[xcoord, ycoord] = detectorData[xcoord, ycoord] + 1
            detStats[0]=detStats[0]+500     #time
            detStats[1]=detStats[1]+200   #count
            detStats[2]=detStats[2]+1000  #monitor
            pickle.dump(detStats, open(emulatorPath+"detStats.bin", "wb"))
            pickle.dump(detectorData, open(emulatorPath+"detectorData.bin", "wb"))
            sleep(0.4)
        detStats[4]=0
        pickle.dump(detStats, open(emulatorPath+"detStats.bin", "wb"))
    else:
        print('Wrong MODE argument given to detectorEmulator')
    
    return

def RSNDcount(mode, count, echoing='on', writeEnd='off'):
    #Start measurement
    _thread.start_new_thread(detectorEmulator, (mode, count*1000) )
    sleep(0.5)   
    succ=0
    while succ==0:
        try:
            detStats=pickle.load(open(emulatorPath+'detStats.bin', 'rb'))
            succ=1
        except:
            pass
    
    while detStats[4]==1: 
        
        if echoing == 'on':
            print("{0:10.2f} {1:10d} {2:10d}\r".format(int(detStats[0])/1000, int(detStats[1]), int(detStats[2])), end=' ')
            sys.stdout.flush()
        
        succ=0
        while succ==0:
            try:
                detStats=pickle.load(open(emulatorPath+'detStats.bin', 'rb'))
                succ=1
            except:
                pass
        sleep(0.5)
    
    if (writeEnd == 'off') & (echoing == 'on'):
        print("                                      \r", end=' ')
            
    
    #retVals=[Time(ms) Detector Monitor Seq.Number]
    succ=0
    while succ==0:
        try:
            detStats=pickle.load(open(emulatorPath+'detStats.bin', 'rb'))
            succ=1
        except:
            pass
    
    data=read2Ddata()
    ROIcounts=sumCountsInROI(data, actSpect.ROI[0], actSpect.ROI[1], actSpect.ROI[2], actSpect.ROI[3]) 
    retVals=[float(detStats[0]), int(detStats[1]), int(detStats[2]), int(detStats[3]), int(ROIcounts) ]
    
    #print "vege"
    return retVals
    
def stopMove(axis):
    # the all function is not implemented jet
    if axis == 'all': commandSocket.sendall('stop')
    else: commandSocket.sendall('stop -a '+ axis)
    
    
    
    
    
    
    
    
