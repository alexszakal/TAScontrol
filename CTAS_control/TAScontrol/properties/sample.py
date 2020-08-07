from numpy import *
import pickle

from .basicSample import *

from TAScontrol.others.filePath import *

class Sample(basicSampleType):
    ###Sample object
    def __init__(self, name=''):
        if name=='':
            self.name='dummy'
            self.a=2*pi
            self.b=2*pi
            self.c=2*pi
            
            self.alpha=90
            self.beta=90
            self.gamma=90
            
            self.B=eye(3)
            self.UB=eye(3)
            self.ORef=zeros((2,8))
            self.pVec=matrix('1 0 0; 0 1 0')
        else:
            print('Loading file: '+name+'.bin\n')
            try:
                sampleData=pickle.load(open(configDataPath+'defaultSample.bin', 'rb'))
            except:
                print('WARNING: The ' + name +'.bin could not be loaded. Loading the default values!' )
                pickle.dump(Sample(), open(configDataPath+'defaultSample.bin', 'wb'))
                sampleData=pickle.load(open(configDataPath+'defaultSample.bin', 'rb'))
            self.name=sampleData.name
            self.a=sampleData.a
            self.b=sampleData.b
            self.c=sampleData.c
        
            self.alpha=sampleData.alpha
            self.beta=sampleData.beta
            self.gamma=sampleData.gamma
            
            self.B=sampleData.B
            self.UB=sampleData.UB
            self.ORef=sampleData.ORef
            self.pVec=sampleData.pVec
        

    def save(self, filname='actSample'):
        tmpS=basicSampleType(self.a,self.b,self.c,self.alpha,self.beta,self.gamma,self.B,self.UB,self.pVec,self.ORef,self.name)
        pickle.dump(tmpS, open(configDataPath+filname+'.bin', 'wb'))

    def refreshUB(self):
        #Calculation of direct lattice vectors
        a1v=matrix('{0:.5f} 0 0'.format(self.a))
        a2v=matrix('{0:.5f} {1:.5f} 0'.format(self.b*cos(deg2rad(self.gamma)), self.b*sin(deg2rad(self.gamma))))
        a31=cos(deg2rad(self.beta))*self.c
        a32=(self.c*cos(deg2rad(self.alpha))-a31*cos(deg2rad(self.gamma))) / sin(deg2rad(self.gamma))
        a33=sqrt(pow(self.c,2)-pow(a31,2)-pow(a32,2))
        a3v=matrix('{0:.5f} {1:.5f} {2:.5f}'.format(a31,a32,a33))
        
        #Direct lattice volume:
        V=dot(cross(a1v, a2v), a3v.transpose())
        
        #Reciprocal lattice vectors:
        b1v=2*pi*cross(a2v,a3v)/V
        b2v=2*pi*cross(a3v,a1v)/V
        b3v=2*pi*cross(a1v,a2v)/V
        #Absolute values of reciprocal lattice vetors:
        b1=sqrt(pow(b1v[0,0],2)+pow(b1v[0,1],2)+pow(b1v[0,2],2))
        b2=sqrt(pow(b2v[0,0],2)+pow(b2v[0,1],2)+pow(b2v[0,2],2))
        b3=sqrt(pow(b3v[0,0],2)+pow(b3v[0,1],2)+pow(b3v[0,2],2))
        #angles between reciprocal lattice vectors:
        beta1=arccos( dot(b2v,b3v.transpose())/b2/b3 ) /pi *180
        beta2=arccos( dot(b1v,b3v.transpose())/b1/b3 ) /pi *180
        beta3=arccos( dot(b1v,b2v.transpose())/b1/b2 ) /pi *180
        
        #Calculation of B matrix 
        B=zeros((3,3))
        B[0][0]=float(b1)
        B[0][1]=float(b2)*cos(deg2rad(beta3))
        B[0][2]=float(b3)*cos(deg2rad(beta2))
        B[1][1]=float(b2)*sin(deg2rad(beta3))
        B[1][2]=-1*sin(deg2rad(beta2))*cos(deg2rad(self.alpha))
        B[2][2]=2*pi/float(self.c)
        
        self.B=B
        
        #################################
        #### CALCULATION OF U matrix ####
        #################################
        #calculate u_nu1, u_nu2
        theta1=self.ORef[0][5]/2 * (-1)
        theta2=self.ORef[1][5]/2 * (-1)

        omBL1=self.ORef[0][4]*(-1)-theta1  #omega in frame of Busing-Levy definitions
        omBL2=self.ORef[1][4]*(-1)-theta2

        uNu1=zeros((3,1))
        uNu1[0][0]=cos(deg2rad(omBL1))*cos(-1*deg2rad(-1*self.ORef[0][6]))
        uNu1[1][0]=-1*sin(deg2rad(omBL1))*cos(-1*deg2rad(-1*self.ORef[0][7])) + cos(deg2rad(omBL1))*sin(deg2rad(-1*self.ORef[0][6]))*sin(deg2rad(-1*self.ORef[0][7])) 
        uNu1[2][0]=sin(deg2rad(omBL1))*sin(deg2rad(-1*self.ORef[0][7])) + cos(deg2rad(omBL1))*sin(deg2rad(-1*self.ORef[0][6]))*cos(deg2rad(-1*self.ORef[0][7]))

        uNu2=zeros((3,1))
        uNu2[0][0]=cos(deg2rad(omBL2))*cos(-1*deg2rad(-1*self.ORef[1][6]))
        uNu2[1][0]=-1*sin(deg2rad(omBL2))*cos(-1*deg2rad(-1*self.ORef[1][7])) + cos(deg2rad(omBL2))*sin(deg2rad(-1*self.ORef[1][6]))*sin(deg2rad(-1*self.ORef[1][7]))
        uNu2[2][0]=sin(deg2rad(omBL2))*sin(deg2rad(-1*self.ORef[1][7])) + cos(deg2rad(omBL2))*sin(deg2rad(-1*self.ORef[1][6]))*cos(deg2rad(-1*self.ORef[1][7]))
        
        #Coordinates of the reflections in the cartesian system of the crystal
        h1c=dot(B, self.ORef[0,0:3])
        h2c=dot(B, self.ORef[1,0:3])
        

        #Construction of T_(crystal cartesian)
        Tc=zeros((3,3))
        t1c=h1c/linalg.norm(h1c)
        Tc[0][0]=t1c[0]
        Tc[1][0]=t1c[1]
        Tc[2][0]=t1c[2]

        t3c=cross(h1c.T,h2c.T)     / linalg.norm(cross(h1c.T,h2c.T))
        Tc[0][2]=t3c[0]
        Tc[1][2]=t3c[1]
        Tc[2][2]=t3c[2]

        t2c=-1* cross(t1c.T,t3c) / linalg.norm(cross(t1c.T,t3c))
        Tc[0][1]=t2c[0]
        Tc[1][1]=t2c[1]
        Tc[2][1]=t2c[2]

        #Constructions of T_(phi cartesian)
        Tphi=zeros((3,3))
        t1phi=uNu1/linalg.norm(uNu1)
        Tphi[0][0]=t1phi[0]
        Tphi[1][0]=t1phi[1]
        Tphi[2][0]=t1phi[2]

        t3phi=cross(uNu1.T,uNu2.T) / linalg.norm(cross(uNu1.T, uNu2.T))
        Tphi[0][2]=t3phi[0][0]
        Tphi[1][2]=t3phi[0][1]
        Tphi[2][2]=t3phi[0][2]

        t2phi=-1*cross(t1phi.T,t3phi) / linalg.norm(cross(t1phi.T,t3phi))
        Tphi[0][1]=t2phi[0][0]
        Tphi[1][1]=t2phi[0][1]
        Tphi[2][1]=t2phi[0][2]

        U=dot(Tphi,linalg.inv(Tc))
        self.UB=dot(U,B)
        
        print('\n Refreshed UB:')
        print(self.UB)



global actSample
actSample=Sample('actSample') #Ha itt baj van, akkor ki kell kommentelni,
                                #elinditani, es elmenteni, hogy a pickle a 
                                #helyes utakat irja a fileba!!!!!!!

