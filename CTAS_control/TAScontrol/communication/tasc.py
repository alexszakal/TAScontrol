import socket
import numpy
import sys
import pickle
import time

from time import sleep
from .tascCommSockets import statusSocket
from .tascCommSockets import commandSocket
from .tascAxisDefs import *

global detConnected
detCouple = 'couple'    # 'couple' or 'release' A6 angle

from TAScontrol.properties.spectrometer import *

statusHOST = '148.6.120.29'    # The address of the status host
statusPORT = 4973
commandHOST = '148.6.120.29'   # The address of the command host
commandPORT = 4975

def position(axis):
    #Get the position of a motor 
    #motname is string
    #returns the position as floating point


    statusSocket.sendall('GetPosition,motor='+axis+';\r\n')
    data = statusSocket.recv(4096)
    #print 'Reply:'
    #print data
    vals=data.split(',')
    angle=vals[2].split('=')
    #if axis == 'STP25':
    #    angleret=float(angle[1])+90
    #    return angleret
    return float(angle[1])

def isMoving(axis):
    #Determine if an axis is moving
    #returns 0->not moving
    #        1-> moving
    if(axis.find('SRQV')==0):
        statusSocket.sendall('GetPosition,motor='+axis+';\r\n')
        data = statusSocket.recv(4096)
        vals=data.replace(',',' ').replace('=',' ').split()
        return int(vals[8][0])     #Ez az enabled bitet adja vissza mert a szervoknal az jelenti hogy megallt
    else:
        statusSocket.sendall('GetPosition,motor='+axis+';\r\n')
        data = statusSocket.recv(4096)
        #print data;
        
        vals=data.replace(',',' ').replace('=',' ').split()
        #print "Moving: {0}".format(vals[8][3])
        return int(vals[8][3])    #Ez a moving bitet adja vissza.
    
    
def axisStatus(axis):
    """Reads the status of an axis"""

    msg='GetStatus,motor='+axis+';\r\n'
    print('Message:\n'+msg)
    statusSocket.sendall(msg)
    data = statusSocket.recv(4096)
    print('Reply:\n'+data)
    data = data.replace(',',';')
    data = data.replace('=',';')
    dataParts = data.split(';')
    return dataParts[4]
    
def startMove(axis, targetPos):
    """Start to move a motor to a given position"""
    if bool(axis == detang) & bool(detCouple == 'couple'):
        msg='TASMoveTo,motor='+axis+',position='+str(targetPos)+',unit='+unitDict[axisDictRev[axis]]+';&\r\n'
    else:
        msg='MoveTo,motor='+axis+',position='+str(targetPos)+',unit='+unitDict[axisDictRev[axis]]+';&\r\n'
    #print 'startMove message: '+msg
    commandSocket.setblocking(0)
    try:
        commandSocket.recv(4096)   ##Az eddigi beragadt valaszok kiszurese
    except:
        pass
    commandSocket.setblocking(1)
    commandSocket.sendall(msg)
    data=""
    while data.find(";\r\n") == -1:
        data = data + commandSocket.recv(4096)
    #print 'Reply:\n'+data
    if data == '0,message=OK;\r\n':
        return "moveStarted"
    else:
        print("Motor move error on "+axis+" axis: "+data)
        return "Error: "+data     

def startCounting(mode, value):
    #Start counting
    #mode='time' or mode='monitor'
    #value is counting time[ms] or the monitor value
    
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.connect((commandHOST, commandPORT))
    
    if mode == 'time':
        commandSocket.sendall('StartDAQ,timelimit='+str(value)+';&\r\n')
        print('StartDAQ,timelimit='+str(value)+';&\r\n')
    elif mode == 'monitor':
        commandSocket.sendall('StartDAQ,monitorlimit='+str(value)+';&\r\n')
    else:
        print('startCounting error. Give correct mode! Mode given: ' + mode)

    data = commandSocket.recv(4096)
    print("startCount Reply:"+data)
    #print "DAQStart reply:"
    #print data
    
    if data == '0,message=OK;\r\n':
        #print 'DAQ started'
        return 1
    else:
        print('DAQ start error! Message: '+data)
        return 0
    

def read2Ddata():
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.connect((statusHOST, statusPORT))
    indexNum=1
    retval=numpy.zeros((129,129))
    
    statusSocket.sendall('Get2DHistogram,sequence=0;\r\n')
    detector=''
    getData=statusSocket.recv(4096)
    while getData.find(';') < 0:
        detector=detector+getData
        getData=statusSocket.recv(4096)
    detector=detector+getData
    
    #print detector.split('Histogram=')[0]
    data=detector.split('Histogram=')[1]
    data=data.split(';')[0]
    data=data.split(' ')
    
    for i in range(129):
        for j in range(129):
            retval[j][i]=float(data[i*129+j])
        
    
    """
    for indexNum in range(0,32):
        #print 'Getting index='+str(indexNum+1)
        statusSocket.sendall('Get2DHistogram,sequence=0,index='+str(indexNum+1)+';\r\n')
        data = statusSocket.recv(4096)
        #print data
        dataSplit=data.split('=')
        dataCounts=dataSplit[2].split(';')  #clear the ';' sign from the end
        dataPixels=dataCounts[0].split(' ')
        numRead=len(dataPixels)
        #print numRead
        for i in range(0,4):   # go through the lines of the 2D images
            for j in range(0,128):
                detector[indexNum+i, j] = float(dataPixels[i*128+j])        
    """
    
    return retval

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
    #The maximal value is inclusive.
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

def RSNDcount(mode, count, echoing='on', writeEnd='off'):
    #Start RSND Counting mode
    if(mode == 'time'):
        commandSocket.sendall('RSND-DAQ,timelimit={0};\r\n'.format(count*1000))
    else:
        commandSocket.sendall('RSND-DAQ,monitorlimit={0};\r\n'.format(count))
    #print 'RSND-DAQ started;'
    data = commandSocket.recv(4096)
    while data.find(";\r\n") == -1:
        data = data + commandSocket.recv(4096)
    #print 'RSND_DAQstart reply:'+data
    
    lastTim=-1
    sameTim=0
    #Measurement started.
    data=""
    dataSplit=['0','0','0','0','0','0','0','0'] 
    while data != "0,message=OK;\r\n":
        data=""
        sleep(1)
        while data.find(';\r\n') == -1:
            data=data + commandSocket.recv(4096)
        #print data
        if data.find("902,message=\"Monitor counts")!=-1:
            dataSplit=data.split('\t')
            if echoing == 'on':
                print("{0:10.2f} {1:10d} {2:10d}\r".format(int(dataSplit[3])/1000.0, int(dataSplit[5]), int(dataSplit[1])), end=' ')
                sys.stdout.flush()
            if int(dataSplit[3]) == lastTim:
                sameTim=sameTim+1
            else:
                sameTim=0
                lastTim=int(dataSplit[3])
                
            if sameTim>4:
                commandSocket.sendall('StopDAQ;\r\n')
                reply=commandSocket.recv(4096)
                #print 'stopReply:'
                sleep(3)
                #print reply
                retVals=RSNDcount(mode, count, echoing, writeEnd)
                return retVals
    
    if (writeEnd == 'off') & (echoing == 'on'):
        print("                                      \r", end=' ')
            
    statusSocket.sendall('GetDAQStatus;\r\n'.format(count*1000))
    reply = statusSocket.recv(4096)
    #print 'StatusReply' + reply
    reply=reply.split(',')[2]
    reply=reply.split('=')[1]
    
    if bool(reply[1]=='1') | bool(reply[2]=='1'):
        retVals=RSNDcount(mode, count, echoing, writeEnd)
    
    data=read2Ddata()
    ROIsum=sumCountsInROI(data, actSpect.ROI[0], actSpect.ROI[1], actSpect.ROI[2], actSpect.ROI[3])
    
    statusSocket.sendall('GetResult;\r\n')
    reply=statusSocket.recv(4096)

    reply=reply.split(',')
        
    
    retVals=[float(reply[2].split('=')[1]), float(reply[3].split('=')[1])/1000, int(reply[4].split('=')[1]), int(reply[5].split('=')[1]), int(ROIsum) ] #Time

    return retVals
    
def stopMove(axis):
    if axisDict.get(axis) != 'None':
        commandSocket.sendall('Stop,motor='+axis+';\r\n')
        msg=''
        while msg.find('0,message=OK;') == -1:
            #print msg.find('0,message=OK;')
            #print msg
            msg=msg+commandSocket.recv(4096)
        return
    else:
        return
    
    
    
    
    
    
    
    