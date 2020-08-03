from collections import OrderedDict

mvfoc='STP1'
monok='STP4'
monho='SRV32'
s2th='SRV34'
om='STP13'
ath='STP25'
sadist='STP28'
detang='SRV35'
mtrX='STP2'
mtrY='STP3'
mgL='STP5'
mgU='STP6'

s1X='STP7'
s1Y='STP8'
s1L='STP9'
s1U='STP10'
s2X='STP17'
s2Y='STP18'
s2L='STP19'
s2U='STP20'

strX='STP11'
strY='STP12'

agL='STP26'
agU='STP27'

antrX='STP23'
antrY='STP24'
angU='STP26'      #Analyzer upper? goniometer
angL='STP27'
detdist='STP29'
msdist='SRV33'    #Monochromator-Sample distance

anShRot='STP21'    #Analyzer shielding Rotation
anShLift='STP22'   #Analyzer shield Lift

sgL='STP14'
sgU='STP15'

#Dictionary readable -> ANTE layer
global axisDict
global axisDictRev
#axisDict=OrderedDict([ ('mvfoc','STP1'), ('monok','STP4'), ('monho','SRV32'),\
#('s2th','SRV34'),('om','STP13'),('ath','STP25'),('sadist','STP28'),('detang','SRV35'),\
#('mtrX','STP2'), ('mtrY','STP3'), ('mgL','STP5'), ('mgU','STP6'), ('s1X', 'STP7'),\
#('s1Y','STP8'), ('s1L','STP9'), ('s1U','STP10'), ('s2X','STP17'), ('s2Y','STP18'),\
#('s2L','STP19'), ('s2U','STP20'), ('strX','STP11'), ('strY','STP12'), ('agU','STP27'),\
#('agL','STP27'), ('antrX', 'STP23'), ('antrY','STP24'), ('angU','STP26'), ('angL','STP27'),\
#('detdist','STP29'), ('msdist','SRV33'), ('anShRot', 'STP21'), ('anShLift', 'STP22'),\
#('sgL', 'STP14'), ('sgU', 'STP15')])

axisDict=OrderedDict( [('monok','STP4'), ('monho','SRV32'),  ('om','STP13'), ('s2th','SRV34'),
('ath','STP25'), ('detang','SRV35'), ('sgU', 'STP15'), ('sgL', 'STP14'),   ('mvfoc','STP1'),
 ('mtrX','STP2'), ('mtrY','STP3'), ('mgU','STP6'), ('mgL','STP5'), ('s1X', 'STP7'), ('s1Y','STP8'),
 ('s1L','STP9'), ('s1U','STP10'), ('s2X','STP17'), ('s2Y','STP18'), ('s2L','STP19'), ('s2U','STP20'),
 ('strX','STP11'), ('strY','STP12'), ('antrX', 'STP23'), ('antrY','STP24'), 
 ('angL','STP27'),  ('angU','STP26'),  ('msdist','SRV33'), ('sadist','STP28'), 
 ('detdist','STP29'), ('anShRot', 'STP21'), ('anShLift', 'STP22') ] )

global axisDictList
axisDictList=axisDict.items()

axisDictRev=OrderedDict()
for i in range(0,axisDictList.__len__()):
    axisDictRev.__setitem__(axisDictList[i][1], axisDictList[i][0])
global axisDictRevList
axisDictRevList=axisDictRev.items()

global unitDict
unitDict=OrderedDict([ ('mvfoc','step'), ('monok','degree'), ('monho','degree'),\
('s2th','degree'),('om','degree'),('ath','degree'),('sadist','mm'),('detang','degree'),\
('mtrX','mm'), ('mtrY','mm'), ('mgL','degree'), ('mgU','degree'), ('s1X', 'mm'),\
('s1Y','mm'), ('s1L','mm'), ('s1U','mm'), ('s2X','mm'), ('s2Y','mm'),\
('s2L','mm'), ('s2U','mm'), ('strX','mm'), ('strY','mm'), ('agU','degree'),\
('agL','degree'), ('antrX', 'mm'), ('antrY','mm'), ('angU','degree'), ('angL','degree'),\
('detdist','mm'), ('msdist','mm'), ('anShRot','position'), ('anShLift', 'mm'),\
('sgL', 'degree'),('sgU', 'degree')])

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
