from numpy import *
import pickle
import math as ma

from .sample import *
from .basicSpectrometer import *
from collections import OrderedDict
from TAScontrol.others.filePath import *


class Spectrometer(basicSpectrometer):
    def __init__(self, name=''):
        if name=='':
            self.d_monok=3.35395
            self.d_ana=3.35395
            self.scattSign=matrix('1 1 1')
            self.lock=['ki',2.5618]
            self.colli=[600,30,60,60]
            self.ROI=[1,128,1,128]
            self.axisOffsetDict=OrderedDict([ ('mvfoc',0), ('monok',-0.45), ('monho',0),\
            ('s2th',0),('om',0),('ath',0),('sadist',0),('detang',1.5),\
            ('mtrX',0), ('mtrY',0), ('mgL',0), ('mgU',0), ('s1X', 0),\
            ('s1Y',0), ('s1L',0), ('s1U',0), ('s2X',0), ('s2Y',0),\
            ('s2L',0), ('s2U',0), ('strX',0), ('strY',0), ('agU',0),\
            ('agL',0), ('antrX', 0), ('antrY',0), ('angU',0), ('angL',0),\
            ('detdist',0), ('msdist',0), ('anShRot',0), ('anShLift', 0),\
            ('sgL', 0), ('sgU', 0)])
            self.axisLimitsDict=OrderedDict( [ ('mvfoc',[0,100]), ('monok',[10,70]), ('monho',[30,70]),\
            ('s2th',[-70,70]),('om',[0,355]),('ath',[0,180]),('sadist',[400,600]),('detang',[-70,70]),\
            ('mtrX',[-10,10]), ('mtrY',[-10,10]), ('mgL',[-10,10]), ('mgU',[-10,10]), ('s1X', [0,60]),\
            ('s1Y',[0,60]), ('s1L',[0,60]), ('s1U',[0,60]), ('s2X',[0,60]), ('s2Y',[0,60]),\
            ('s2L',[0,60]), ('s2U',[0,60]), ('strX',[-20,20]), ('strY',[-20,20]),\
            ('antrX', [-20,20]), ('antrY',[-20,20]), ('angU',[-5,5] ), ('angL',[-5,5]),\
            ('detdist',[600,1000]), ('msdist',[1000,1500]), ('anShRot',[0,14]), ('anShLift', [0,600]),\
            ('sgL', [-15,15]), ('sgU', [-15,15]) ] )
            
            
        else:        
            spectrometerData=pickle.load(open(configDataPath+name+'.bin', 'rb'))
            self.d_monok=spectrometerData.d_monok
            self.d_ana=spectrometerData.d_ana
            
            self.scattSign=spectrometerData.scattSign
            self.lock=spectrometerData.lock
            self.colli=spectrometerData.colli
            self.ROI=spectrometerData.ROI
            self.axisOffsetDict=spectrometerData.axisOffsetDict
            self.axisLimitsDict=spectrometerData.axisLimitsDict
            

    def save(self, filname='actSpect'):
        tmpS=basicSpectrometer(self.d_monok, self.d_ana, self.scattSign, self.lock, self.colli, self.ROI, self.axisOffsetDict, self.axisLimitsDict)
        pickle.dump(tmpS, open(configDataPath+filname+'.bin', 'wb'))
    
    def calcHKLE(self, h, k, l, E):
        #Definition of reciprocal lattice point, dE, Ei
        hkl=matrix('{0:.4} {1:.4} {2:.4}'.format(float(h), float(k), float(l)))
        
        if(self.lock[0] == 'ki'):
            ki=self.lock[1]
            lam_i=2*pi/ki
            Ei=81.808/pow(lam_i,2)
            A1=rad2deg(arcsin(lam_i/2/self.d_monok)*self.scattSign.item(0))
            
            Ef=Ei-E
            lam_f=sqrt(81.808/Ef)
            kf=2*pi/lam_f
            A5=rad2deg(arcsin(lam_f/2/self.d_ana)*self.scattSign.item(2) )
        elif(self.lock[0] == 'kf'):
            kf=self.lock[1]
            lam_f=2*pi/kf
            Ef=81.808/pow(lam_f,2)
            A5=rad2deg(arcsin(lam_f/2/self.d_ana)*self.scattSign.item(2) )

            Ei=Ef+E
            lam_i=sqrt(81.808/Ei)
            ki=2*pi/lam_i
            A1=rad2deg( arcsin(lam_i/2/self.d_monok)*self.scattSign.item(0) )
        
        B=actSample.B
        UB=actSample.UB
        h1=actSample.pVec[0,0:3].T
        h2=actSample.pVec[1,0:3].T
        #   Scattering angle
        qabs=linalg.norm(dot(B,hkl.T))
        phi=rad2deg( arccos( (pow(ki,2) + pow(kf,2) - pow(qabs,2))/(2*ki*kf) ) ) * self.scattSign.item(1)*(-1)
        phi=rad2deg( arccos( (pow(ki,2) + pow(kf,2) - pow(qabs,2))/(2*ki*kf) ) ) * self.scattSign.item(1)*(-1)
        #   Theta angle
        theta = rad2deg( arctan( (ki-kf*cos(deg2rad(phi))) / (kf*sin(deg2rad(phi))) ) ) 
        if self.scattSign.item(1) == 1:
            theta = 180+theta

        #   Vector normal to the plane h1 h2
        uh1nu=dot(UB,h1) / linalg.norm( dot(UB,h1) )    #h1 in the nu coordinate system
        uh2nu=dot(UB,h2) / linalg.norm( dot(UB,h2) )    #h2 in the nu coordinate system
        uPlaneNormal=cross(uh1nu.T, uh2nu.T)/linalg.norm(cross(uh1nu.T, uh2nu.T))*(-1)

        #   Normalized Q  (u1nu)in the nu coordinate system:
        u1nu = dot( UB, hkl.T) / linalg.norm( dot( UB, hkl.T) )
        #   u2nu (perpendicular to (u1nu anduPlaneNormal)
        u2nu = cross(uPlaneNormal, u1nu.T)

        #   Calculate the T matrix
        T=zeros((3,3))
        #       First column: u1nu
        T[0][0]=u1nu[0][0]
        T[1][0]=u1nu[1][0]
        T[2][0]=u1nu[2][0]
        #       Second column: u2nu
        T[0][1]=u2nu[0][0]
        T[1][1]=u2nu[0][1]
        T[2][1]=u2nu[0][2]
        #       Third column: cross(u1nu, u2nu)
        t3nu=cross(u1nu.T, u2nu)
        T[0][2]=t3nu[0][0]
        T[1][2]=t3nu[0][1]
        T[2][2]=t3nu[0][2]

        #   Calculation of the R matrix
        R=linalg.inv(T)
        #   Calculation of the angles
        mu=rad2deg( arctan(-1*R[2][0] / (sqrt(pow(R[0][0],2) + pow(R[1][0],2) ) )) )
        nu=rad2deg( arctan(R[2][1] / R[2][2] ) )

        ### START MU CALCULATION
        muCos=sqrt( pow(R[0][0],2) + pow(R[1][0],2)  ) 
        muSin=-1*R[2][0] 
        mu=rad2deg(math.atan2(muSin, muCos))
        #muCos1=rad2deg( arccos(sqrt( pow(R[0][0],2) + pow(R[1][0],2)  ) ) )
        #muCos2=360-muCos1
        #muSin1=rad2deg( arcsin(-1*R[2][0]) )
        #if muSin1>0:
        #    muSin2=180-muSin1
        #else:
        #    muSin2=-180+muSin1
        #    muSin1=muSin1+360
        #    muSin2=muSin2+360

        #minidev=500
        #if abs(muSin1-muCos1) < minidev:
        #    mu=muSin1
        #    minidev = abs(muSin1-muCos1)
        #if abs(muSin1-muCos2) < minidev:
        #    mu=muSin1
        #    minidev = abs(muSin1-muCos2)
        #if abs(muSin2-muCos1) < minidev:
        #    mu=muSin2
        #    minidev = abs(muSin2-muCos1)
        #if abs(muSin2-muCos2) < minidev:
        #    mu=muSin2
        #    minidev = abs(muSin2-muCos2)
        ####END MU CALCULATION
        
        ### START NU CALCULATION
        nuCos=R[2][2]/sqrt( pow(R[0][0],2) + pow(R[1][0],2) )
        nuSin=R[2][1]/sqrt( pow(R[0][0],2) + pow(R[1][0],2) ) 
        nu=rad2deg(math.atan2(nuSin, nuCos))
        
        #nuCos1=rad2deg( arccos(R[2][2]/sqrt( pow(R[0][0],2) + pow(R[1][0],2)  ) ) )
        #nuCos2=360-nuCos1
        #nuSin1=rad2deg( arcsin(R[2][1]/sqrt( pow(R[0][0],2) + pow(R[1][0],2)  ) ) )
        #if nuSin1>0:
        #    nuSin2=180-nuSin1
        #else:
        #    nuSin2=-180+nuSin1
        #    nuSin1=nuSin1+360
        #    nuSin2=nuSin2+360

        #minidev=500
        #if abs(nuSin1-nuCos1) < minidev:
        #    nu=nuSin1
        #    minidev = abs(nuSin1-nuCos1)
        #if abs(nuSin1-nuCos2) < minidev:
        #    nu=nuSin1
        #    minidev = abs(nuSin1-nuCos2)
        #if abs(nuSin2-nuCos1) < minidev:
        #    nu=nuSin2
        #    minidev = abs(nuSin2-nuCos1)
        #if abs(nuSin2-nuCos2) < minidev:
        #    nu=nuSin2
        #    minidev = abs(nuSin2-nuCos2)
        ####END NU CALCULATION
       
        ### START OMEGA CALCULATION
        omegaCos1=rad2deg( arccos(R[0][0]/sqrt( pow(R[0][0],2) + pow(R[1][0],2)  ) ) )
        omegaCos2=360-omegaCos1
        omegaSin1=rad2deg( arcsin(R[1][0]/sqrt( pow(R[0][0],2) + pow(R[1][0],2)  ) ) )
        if omegaSin1>0:
            omegaSin2=180-omegaSin1
        else:
            omegaSin2=-180+omegaSin1
            omegaSin1=omegaSin1+360
            omegaSin2=omegaSin2+360

        minidev=500
        if abs(omegaSin1-omegaCos1) < minidev:
            omega=omegaSin1
            minidev = abs(omegaSin1-omegaCos1)
        if abs(omegaSin1-omegaCos2) < minidev:
            omega=omegaSin1
            minidev = abs(omegaSin1-omegaCos2)
        if abs(omegaSin2-omegaCos1) < minidev:
            omega=omegaSin2
            minidev = abs(omegaSin2-omegaCos1)
        if abs(omegaSin2-omegaCos2) < minidev:
            omega=omegaSin2
            minidev = abs(omegaSin2-omegaCos2)
        ####END OMEGA CALCULATION
        
        s=omega + theta
        #print 'Calculated theta: {0}'.format(theta)
        #print 'Calculated omega: {0}'.format(omega)
        
        if s<0:        #To have S1 between 0 and 355
            s=360+s
        if s>360:
            s=s-360
        
        s=360-s   #Transform back
        phi=-1*phi
        mu=-1*mu
        nu=-1*nu
        return [A1, 2*A1, s, phi, A5, 2*A5, nu, mu]


    
global actSpect
actSpect=Spectrometer('actSpect')