from numpy import *
from collections import OrderedDict
from sample import *


class basicSample():
    def __init__(self, a=1, b=1, c=1, alpha=90, beta=90, gamma=90, UB=eye(3), ORef=zeros((2,8)), name='dummy'):
        self.name=name
        
        self.a=a
        self.b=b
        self.c=c
    
        self.alpha=alpha
        self.beta=beta
        self.gamma=gamma
    
        self.UB=UB
    
        self.ORef=ORef

class basicSpectrometer():
    def __init__(self, d_monok=3.35395, d_ana=3.35395, sample=Sample(actSample), scattSign=matrix('1 1 1')):
        #data part of the spectrometer
        self.d_monok=d_monok
        self.d_ana=d_ana
        
        self.sample=sample
        
        self.scattSign=scattSign
        
    