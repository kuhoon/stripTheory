import os

from sol103 import *
from sol145 import *
from pyNastran.bdf.bdf import *
# from solMerged import *

nodesFileName = "datFiles/nodes.dat" #둘다 가능
lumpFileName = "datFiles/mass_lump.dat"
concFileName = "datFiles/mass_conc.dat"
elementsFileName = "datFiles/elements.dat"
sectionFileName = "datFiles/sections.dat"
machFileName = "datFiles/machNum.dat"
rrfFileName = "datFiles/redRF.dat"
v3FileName = "datfiles/v3.dat"

# create sol103 file
model103 = BDF()
create103(model103, nodesFileName, lumpFileName, concFileName, elementsFileName) #sol103 파일 만들기

bdf103_filename_out = os.path.join('../../sol103_ver01.bdf')
model103.write_bdf(bdf103_filename_out, enddata=True)
print(bdf103_filename_out)

print('----------------------------------------------------------------------------------------------------')

# create sol145 file
model145 = BDF()
create103(model145, nodesFileName, lumpFileName, concFileName, elementsFileName)
create145(model145, sectionFileName, concFileName, nodesFileName, machFileName, rrfFileName, v3FileName)
bdf145_filename_out = os.path.join('sol145_ver01.bdf')
model145.write_bdf(bdf145_filename_out, enddata=True)
print(bdf145_filename_out)