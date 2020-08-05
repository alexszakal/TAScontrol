from numpy import *
import pickle

from .basicExp import *
from TAScontrol.others.filePath import *

class Experiment(BasicExperiment):
    def __init__(self, name=''):
        if name=='':
            self.user='CNTAS_user'
            self.title='Exp.Title'
        else:
            expData=pickle.load(open(configDataPath+name+'.bin', 'rb'))
            self.user=expData.user
            self.title=expData.title
    
    def save(self, filname='actExp'):
        tmpE=BasicExperiment(self.user, self.title)
        pickle.dump(tmpE, open(configDataPath+filname+'.bin', 'wb'))
        
global actExp
actExp=Experiment('actExp')