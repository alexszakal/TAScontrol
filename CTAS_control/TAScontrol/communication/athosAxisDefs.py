from collections import OrderedDict

monho='monho'
om='om'
s2th='2th'
ath='ath'
detang='detang'

#Dictionary readable -> ANTE layer
global axisDict
global axisDictRev

axisDict=OrderedDict( [('monho','monho'), ('om','om'),  ('2th','2th'), 
('ath','ath'), ('detang','detang') ] )

global axisDictList
axisDictList=list(axisDict.items())

axisDictRev=OrderedDict()
for i in range(0,axisDictList.__len__()):
    axisDictRev.__setitem__(axisDictList[i][1], axisDictList[i][0])
global axisDictRevList
axisDictRevList=list(axisDictRev.items())

global unitDict
unitDict=OrderedDict([ ('monho','deg'), ('om','deg'), ('2th','deg'),\
('ath','deg'),('detang','deg')])

#global axisOffsetDict   #EZT FOGJA HOZZAADNI/kivonni A SZOGHOZ
#axisOffsetDict=OrderedDict([ ('mvfoc',0), ('monok',-0.45), ('monho',0),\
#('s2th',0),('om',0),('ath',0),('sadist',0),('detang',1.5),\
#('mtrX',0), ('mtrY',0), ('mgL',0), ('mgU',0), ('s1X', 0),\
#('s1Y',0), ('s1L',0), ('s1U',0), ('s2X',0), ('s2Y',0),\
#('s2L',0), ('s2U',0), ('strX',0), ('strY',0), ('agU',0),\
#('agL',0), ('antrX', 0), ('antrY',0), ('angU',0), ('angL',0),\
#('detdist',0), ('msdist',0), ('anShRot',0), ('anShLift', 0),\
#('sgL', 0), ('sgU', 0)])


global ROI
ROI=[1,128, 1, 128] #ROI definition [Xmin, Xmax, Ymin, Ymax]
