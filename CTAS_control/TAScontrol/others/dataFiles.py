import time
from os import listdir
from TAScontrol.communication.tascAxisDefs import *            #Axis names
from TAScontrol.properties.sample import *
from TAScontrol.properties.spectrometer import *
from TAScontrol.properties.experiment import *

from TAScontrol.others.filePath import *

import TAScontrol.user_commands.commands

def initScanFile(command):
    #starts the data files
    #cnt-20140404_10_12_11.log type AND s100000.dat type
    #RETURNS: list of file references [fLogDate, fLogNum]

    
    #Create the filename string
    ct=time.localtime();
    filnameDate="cnt-{0:02d}{1:02d}{2:02d}_{3:02d}_{4:02d}_{5:02d}.log".format\
    (ct.tm_year-2000, ct.tm_mon, ct.tm_mday, ct.tm_hour, ct.tm_min, ct.tm_sec)
    
    #get the last index number
    files=listdir(dataPath+'numberedScans/')
    files.sort()      #Sort the names in place
    lastfile=files[len(files)-1]
    nextFileNum=int(lastfile.replace('s','').replace('.dat',''))+1
    
    filNameNum="s{0}.dat".format(nextFileNum)
    print filnameDate+"      "+"s"+str(nextFileNum)
    #Open the file
    fLogDate=open(dataPath+filnameDate, 'w')
    fLogNum=open(dataPath+"numberedScans/"+filNameNum,'w')
    
    #Write the HEADER of the file
    fLogDate.write("#CNTAS {0} {1} \n".format(actExp.user, time.asctime()))
    fLogNum.write( "#CNTAS {0} {1} \n".format(actExp.user, time.asctime()))
    
    fLogDate.write("#USER: {0} \n".format(actExp.user))
    fLogNum.write( "#USER: {0} \n".format(actExp.user))
    
    fLogDate.write("#DATE: {0} \n".format(time.asctime()))
    fLogNum.write( "#DATE: {0} \n".format(time.asctime()))
    
    fLogDate.write("#TITLE: {0} \n".format(actExp.title))
    fLogNum.write( "#TITLE: {0} \n".format(actExp.title))
    
    fLogDate.write("#CMD: " + command+ "\n")
    fLogNum.write( "#CMD: " + command+ "\n")
    
    #which one steps? what amount?
    if command.split('(')[0] == 'scan': 
        variAxis=[command.split('(')[1].split(',')[0].split('=')[1]]
        variValue=[command.split('(')[1].split(',')[2].split('=')[1]]
    if command.split('(')[0] == 'cscan':
        variAxis=[command.split('(')[1].split(',')[0].split('=')[1]]
        variValue=[command.split('(')[1].split(',')[2].split('=')[1]]
    if command.split('(')[0] == 'schkl':
        stepVals=matrix( command.split('=')[2].rsplit(',',1)[0])
        valStrings=['H', 'K', 'L', 'EN']
        variAxis=list()
        variValue=list()
        for i in range(4):
            if stepVals.item(i) != 0:
                variAxis=variAxis+[valStrings[i]]
                variValue=variValue+[stepVals.item(i)]
    
    fLogDate.write("#STEPS: ")
    fLogNum.write( "#STEPS: ")
    for i in range(variAxis.__len__()):
        fLogDate.write(variAxis[i] + " = {0}  ".format(variValue[i]))
        fLogNum.write (variAxis[i] + " = {0}  ".format(variValue[i]))
    fLogDate.write("\n")
    fLogNum.write( "\n")
    
    fLogDate.write("#ROI: Xmin={0} Xmax={1} Ymin={2} Ymax={3} \n".format(ROI[0], ROI[1], ROI[2], ROI[3]))
    fLogNum.write( "#ROI: Xmin={0} Xmax={1} Ymin={2} Ymax={3} \n".format(ROI[0], ROI[1], ROI[2], ROI[3]))
    
    fLogDate.write("#COLLI: ALF1={0} ALF2={1} ALF3={2} ALF4={3}\n".format(actSpect.colli[0], actSpect.colli[1], actSpect.colli[2], actSpect.colli[3]) )
    fLogNum.write( "#COLLI: ALF1={0} ALF2={1} ALF3={2} ALF4={3}\n".format(actSpect.colli[0], actSpect.colli[1], actSpect.colli[2], actSpect.colli[3]) )
    
    fLogDate.write("#CELL: A={0:7.4} B={1:7.4} C={2:7.4}\n".format(actSample.a, actSample.b, actSample.c ))
    fLogNum.write("#CELL: A={0:7.4} B={1:7.4} C={2:7.4}\n".format(actSample.a, actSample.b, actSample.c ))
    
    fLogDate.write("#CELL: alpha={0:5.2f} beta={1:5.2f} gamma={2:5.2f}\n".format(double(actSample.alpha), double(actSample.beta), double(actSample.gamma) ))
    fLogNum.write( "#CELL: alpha={0:5.2f} beta={1:5.2f} gamma={2:5.2f}\n".format(double(actSample.alpha), double(actSample.beta), double(actSample.gamma) ))
    
    fLogDate.write("#PVEC1: H1={0:5.3f} K1={1:5.3f} L1={2:5.3f}\n".format(double(actSample.pVec[0].item(0)), double(actSample.pVec[0].item(1)), double(actSample.pVec[0].item(2) )))
    fLogNum.write( "#PVEC1: H1={0:5.3f} K1={1:5.3f} L1={2:5.3f}\n".format(double(actSample.pVec[0].item(0)), double(actSample.pVec[0].item(1)), double(actSample.pVec[0].item(2) )))
    
    fLogDate.write("#PVEC2: H2={0:5.3f} K2={1:5.3f} L2={2:5.3f}\n".format(double(actSample.pVec[1].item(0)), double(actSample.pVec[1].item(1)), double(actSample.pVec[1].item(2) )))
    fLogNum.write( "#PVEC2: H2={0:5.3f} K2={1:5.3f} L2={2:5.3f}\n".format(double(actSample.pVec[1].item(0)), double(actSample.pVec[1].item(1)), double(actSample.pVec[1].item(2) )))
    
    # Write the actual angles
    i=0
    for actAxis in axisDictList:
        if i%3 == 0:
            fLogDate.write("#ANGLES: ")
            fLogNum.write( "#ANGLES: ")
        
        fLogDate.write(" {0}={1:8.2f} ".format(actAxis[0].rjust(10), TAScontrol.user_commands.commands.readang(actAxis[1], echoing='off')))
        fLogNum.write( " {0}={1:8.2f} ".format(actAxis[0].rjust(10), TAScontrol.user_commands.commands.readang(actAxis[1], echoing='off')))
        if i%3 == 2:
            fLogDate.write("\n")
            fLogNum.write( "\n")
        i=i+1
    if i%3 !=2 :
        fLogDate.write("\n")
        fLogNum.write( "\n")
    
    fLogDate.write("\n")
    fLogNum.write( "\n")
            
    # Write the zero angles
    i=0
    for actAxis in axisDictList:
        if i%3 == 0:
            fLogDate.write("#ZEROS: ")
            fLogNum.write( "#ZEROS: ")
        
        fLogDate.write(" {0}={1:8.2f} ".format(actAxis[0].rjust(10), actSpect.axisOffsetDict[actAxis[0]] ))
        fLogNum.write( " {0}={1:8.2f} ".format(actAxis[0].rjust(10), actSpect.axisOffsetDict[actAxis[0]] ))
        if i%3 == 2:
            fLogDate.write("\n")
            fLogNum.write( "\n")
        i=i+1
    if i%3 !=2 :
        fLogDate.write("\n")
        fLogNum.write( "\n")
        
    fLogDate.write("\n#DATA:\n")
    fLogNum.write("\n#DATA:\n")
    
    if (bool(command.split('(')[0] == 'scan') | bool(command.split('(')[0] == 'cscan')) :
        fLogDate.write("#{0}        CNT      ROICNT       MON       TIME     2DFNUM    CNT/MON   Err(CNT/MON)\n".format(variAxis[0].rjust(9)) )
        fLogNum.write( "#{0}        CNT      ROICNT       MON       TIME     2DFNUM    CNT/MON   Err(CNT/MON)\n".format(variAxis[0].rjust(9)) )
    else:
        fLogDate.write("#  H       K       L       EN      MON     TIME     CNT     ROICNT  SEQ.NUM   A1     A2     A3     A4     A5     A6     SGL    SGU\n" )
        fLogNum.write( "#  H       K       L       EN      MON     TIME     CNT     ROICNT  SEQ.NUM   A1     A2     A3     A4     A5     A6     SGL    SGU\n" )

    #Write out to the file
    fLogDate.flush()
    fLogNum.flush()
    
    #Prepare return variables
    fList=list()
    fList.append(fLogDate)
    fList.append(fLogNum)
    return fList
    
def writeToLogFile(text):
    #Writes text argument to the log file. Logs only the commands
    
    #Determine the name
    ct=time.localtime()
    name="log-{0:04d}_{1:02d}_{2:02d}".format(ct.tm_year, ct.tm_mon, ct.tm_mday)
    #Check if it exist already.
    
    #If not existing -> Create

    #If existing -> open for appending
    if listdir(logPath).count(name) > 0:
        logFile=open(logPath+name, 'a')
    else:
        logFile=open(logPath+name, 'w')
    
    logFile.write(text+"\n")
    logFile.close()
    
def writeToLogFullFile(text):
    #Writes the text argument to full log 
    #Full log contains the commands and scans also
    
    #Determine the name
    ct=time.localtime()
    name="logFull-{0:04d}_{1:02d}_{2:02d}".format(ct.tm_year, ct.tm_mon, ct.tm_mday)
    #Check if it exist already.
    
    #If not existing -> Create

    #If existing -> open for appending
    if listdir(logFullPath).count(name) > 0:
        logFile=open(logFullPath+name, 'a')
    else: #If not existing -> 
        logFile=open(logFullPath+name, 'w')
    
    logFile.write(text+"\n")
    logFile.close()
