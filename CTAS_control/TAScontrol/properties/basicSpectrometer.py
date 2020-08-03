from numpy import *
from collections import OrderedDict 

class basicSpectrometer():
    def __init__(self, d_monok=3.35395, d_ana=3.35395, scattSign=matrix('1 1 1'), lock=['ki', 2.5618], 
    colli=[600,30,60,60], ROI=[1,128,1,128], axisOffsetDict='none', axisLimitsDict='none'):
        #data part of the spectrometer
        self.d_monok=d_monok
        self.d_ana=d_ana
        
        self.scattSign=scattSign
        
        self.lock=lock
        
        self.colli=colli
        
        self.ROI=ROI
        
        if axisOffsetDict=='none':
            self.axisOffsetDict=OrderedDict([ ('mvfoc',0), ('monok',-0.45), ('monho',0),\
            ('s2th',0),('om',0),('ath',0),('sadist',0),('detang',1.5),\
            ('mtrX',0), ('mtrY',0), ('mgL',0), ('mgU',0), ('s1X', 0),\
            ('s1Y',0), ('s1L',0), ('s1U',0), ('s2X',0), ('s2Y',0),\
            ('s2L',0), ('s2U',0), ('strX',0), ('strY',0), \
            ('antrX', 0), ('antrY',0), ('angU',0), ('angL',0),\
            ('detdist',0), ('msdist',0), ('anShRot',0), ('anShLift', 0),\
            ('sgL', 0), ('sgU', 0)])
        else:
            self.axisOffsetDict=axisOffsetDict
            
        if axisLimitsDict=='none':
            self.axisLimitsDict=OrderedDict( [ ('mvfoc',[-2000,4100]), ('monok',[17,90]), ('monho',[34.5,126]),\
            ('s2th',[-130,130]),('om',[0,355]),('ath',[-90,90]),('sadist',[600,1100]),('detang',[-142,142]),\
            ('mtrX',[-20,20]), ('mtrY',[-20,20]), ('mgL',[-5,5]), ('mgU',[-5,5]), ('s1X', [0,40]),\
            ('s1Y',[0,40]), ('s1L',[0,150]), ('s1U',[0,150]), ('s2X',[0,30]), ('s2Y',[0,30]),\
            ('s2L',[0,120]), ('s2U',[0,120]), ('strX',[-45,45]), ('strY',[-45,45]),\
            ('antrX', [-20,20]), ('antrY',[-20,20]), ('angU',[-15,15] ), ('angL',[-15,15]),\
            ('detdist',[630,1000]), ('msdist',[1900,3100]), ('anShRot',[1,20]), ('anShLift', [0,165]),\
            ('sgL', [-10,10]), ('sgU', [-10,10]) ] )
        else:
            self.axisLimitsDict=axisLimitsDict
        
    