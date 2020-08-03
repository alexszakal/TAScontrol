from numpy import *
from collections import OrderedDict

class basicSampleType():
    def __init__(self, a=2*pi, b=2*pi, c=2*pi, alpha=90, beta=90, gamma=90, B=eye(3), UB=eye(3), pVec=matrix('1 0 0; 0 1 0'), ORef=zeros((2,8)), name='dummy'):
        self.name=name
        
        self.a=a
        self.b=b
        self.c=c
    
        self.alpha=alpha
        self.beta=beta
        self.gamma=gamma
        
        self.B=B
        self.UB=UB
        
        self.pVec=pVec
        self.ORef=ORef
