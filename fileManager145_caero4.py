import os
from pyNastran.bdf.bdf import *
import numpy as np

nodesFileName = "datFiles_numbering/1_nodes.dat"
lumpFileName = "datFiles_numbering/2_mass_lump.dat"
concFileName = "datFiles_numbering/3_mass_conc.dat"
elementsFileName = "datFiles_numbering/4_elements.dat"
sectionFileName = "datFiles_numbering/5_sections.dat"
machFileName = "datFiles_numbering/6_machNum.dat"
rrfFileName = "datFiles_numbering/7_redRF.dat"
v3FileName = "datfiles_numbering/8_v3.dat"

model = BDF()

idList = [] #declare a variable. start on the first line
xValueList = []
yValueList = []
zValueList = []
conm2List = []
mLump = []
pbeamList = []
areaList = []
i1List = []
i2List = []
jList = []
idFromList = []
idToList = []

# ===== special for sol145
idSectList = []
xLeList = []
yLeList = []
zLeList = []
cList = []
machValueList = []
rrfValueList = []
v3ValueList = []
stripList = []
aelistList = []
eId = 201
ptList = []  # [ [], [], [] ]

E = 72397.0
G = 27000.0
nu = 0.32
rho = 0.0000000000000001
mat = model.add_mat1(1, E, G, nu, rho)

# ====================================================================
# =========================== OPEN FILES =============================
# ====================================================================

# open 1_node.dat file_Wing
with open("datFiles_numbering/1_nodes.dat") as datFile:
    nodeValueList = [data.split() for data in datFile]
    del nodeValueList[0] # delete line 0
    for v in nodeValueList:
        idList.append(v[0]) # add list element
        xValueList.append(v[1])
        yValueList.append(v[2])
        zValueList.append(v[3])

# open 2_mass_lump.dat file_Wing
with open("datFiles_numbering/2_mass_lump.dat") as datFile:
    lumpValueList = [data.split() for data in datFile]
    del lumpValueList[0]
    for v in lumpValueList:
        conm2List.append(v[0]) #conm2list 1-100
        mLump.append(v[2])

# open 3_mass_conc.dat file_Main Engine, Landing Gear
with open("datFiles_numbering/3_mass_conc.dat") as datFile:
    massValueList = [data.split() for data in datFile]
    del massValueList[0]
    for v in massValueList:
        idList.append(v[0])
        xValueList.append(v[2])
        yValueList.append(v[3])
        zValueList.append(v[4])
        conm2List.append(v[1]) #conm2list 100, 101, Numbers 100 and 101 must come last in the list order
        mLump.append(v[5])

# open 4_elements.dat file_pbeam
with open("datFiles_numbering/4_elements.dat") as datFile:
    elementValueList = [data.split() for data in datFile]
    del elementValueList[0]
    for v in elementValueList:
        pbeamList.append(v[0])
        areaList.append(v[3])
        i1List.append(v[4])
        i2List.append(v[5])
        jList.append(v[7])
        idFromList.append(v[1])
        idToList.append(v[2])

# <================ special for sol145 ===================>
# open 5_sections.dat file_Wing
with open(sectionFileName) as datFile:
    sectValueList = [data.split() for data in datFile]
    del sectValueList[0]  # delete line 0
    for v in sectValueList:
        idSectList.append(v[0])
        xLeList.append(v[1])  # add list element
        yLeList.append(v[2])
        zLeList.append(v[3])
        cList.append(v[4])

# open 6_machNum.dat file
with open(machFileName) as datFile:
    tempList = [data.split() for data in datFile]
    for t in tempList:
        machValueList.append(float(t[0]))

# open 7_redRF.dat file
with open(rrfFileName) as datFile:
    tempList = [data.split() for data in datFile]
    for t in tempList:
        rrfValueList.append(float(t[0]))

# open 8_v3.dat file
with open(v3FileName) as datFile:
    tempList = [data.split() for data in datFile]
    for t in tempList:
        v3ValueList.append(float(t[0]) * -1)

# ====================================================================
# ========================= ADD ATTRIBUTES ===========================
# ====================================================================

# start model number
model.sol = 145  # start=103

# case control
spc_id = 50
cc = CaseControlDeck([
    'SUBCASE 1',
    'SUBTITLE = Default',
    'METHOD = 10', # MODIFIED GIVENS METHOD OF REAL EIGENVALUE EXTRACTION
    'SPC = %s' % spc_id, # WING ROOT DEFLECTIONS AND PLATE IN-PLANE ROTATIONS FIXED
    'VECTOR(SORT1,REAL)=ALL',
    'SPCFORCES(SORT1, REAL) = ALL',
    'BEGIN BULK',
    'ANALYSIS = FLUTTER',
    'AESYMXY = Asymmetric',
    'AESYMXZ = Symmetric',
    'FMETHOD = 1'
])
model.case_control_deck = cc
model.validate()

# model.add_mat1(1, E, G, nu, rho)

model.add_param('POST', [0])
model.add_param('PRTMAXIM', ['YES'])
model.add_param('SNORM', [20.0])
model.add_param('WTMASS', [1.0])  # default = 1.0
model.add_param('Aunit', [1.0])

# # insert model.add_grid(id_no, x, y, z)
for i, x, y, z in zip(idList, xValueList, yValueList, zValueList):
    model.add_grid(int(i), [float(x), float(y), float(z)])

# insert model.add_conm2(id_conm2, id_no, Mlump)
for j, i, m in zip(conm2List, idList, mLump):
    model.add_conm2(int(j)+10000, int(i), float(m))

# insert model.add_pbeam(id_pbeam, mid, x/xb, so, area, i1, i2, i12, j)
for p, a, i1, i2, j in zip(pbeamList, areaList, i1List, i2List, jList):
    model.add_pbeam(int(p), 1, [0.0], ['YES'], [float(a)], [float(i1)], [float(i2)], [0], [float(j)])

# insert model.add_cbeam
for p, idFrom, idTo in zip(pbeamList, idFromList, idToList):
    model.add_cbeam(int(p), int(p), [int(idFrom), int(idTo)], [], 100)

# insert model.add_spc1, spcadd
model.add_spc1(spc_id, '123456', [1])
model.add_spcadd(1, spc_id)

# insert model.add_rbe2
model.add_rbe2(51, 8, '123456', [100])
model.add_rbe2(52, 8, '123456', [101])

# insert model.add_eigrl
eigrl = model.add_eigrl(10, nd=10, msglvl=0) # how many want to mode

# <=========== sol 145 ===============>
# insert model.add_point(id_no, x, y, z)
for x, y, z, c in zip(xLeList, yLeList, zLeList, cList):
    model.add_point(eId, [float(x), float(y), float(z)])
    ptList.append([float(x), float(y), float(z)])
    eId = eId + 1
    model.add_point(eId, [float(x) + float(c), float(y), float(z)])
    eId = eId + 1

# insert model.add_aefact
eIdAef = 70
aef1 = list(np.linspace(0, 1, 6)) #Creates n-1 boxes with a ratio between 0 and 1.
aef2 = list(np.linspace(0, 1, 15)) #Enter the number of strips you want n + 1
aef3 = list(np.linspace(0, 1, 68))
model.add_aefact(eIdAef, aef1)
model.add_aefact(eIdAef+1, aef2)
model.add_aefact(eIdAef+2, aef3)

# insert model.add_paero4, caero4
eId2 = 103001
for i in range(len(idSectList) - 1): #make for strip
    model.add_paero4(eId2, [0.0], [0.0], [0.0], cla = int(0), lcla = int(0), circ=int(0), lcirc = int(0)) #docs, caocs, gapocs with control surface, default =0. no Control surface
    model.add_caero4(eId2, eId2, np.array(ptList[i], float), float(cList[i]), np.array(ptList[i + 1], float), float(cList[i + 1]), 0, 0, eIdAef)
    eId2 += 1000
    eIdAef += 1
    # stripList.append(bSpan)

# manage add_aelist
eId3 = 103001
eId4 = 104001
eId5 = 105001
for i in range(5): #write down your number of strip in first box
    aelistList.append(eId3 + i)
for i in range(14): #write down your number of strip in second box
    aelistList.append(eId4 + i)
for i in range(67): #write down your number of strip in third box
    aelistList.append(eId5 + i)
model.add_aelist(1, aelistList)

# insert model.add_set1, aero, aeros
model.add_set1(1, idList)
model.add_aero(float(1.0), float(1984.0), float(1.225E-12), 0)  # velocity, aerodynamic chord, density scal, coord
model.add_aeros(float(1984.0), float(17174.0), float(3.227E7 / 2), 0, 0)  # half span model => must used half area

for m in machValueList: #want to make data list for mach and reduced frequency
    for rf in rrfValueList:
        model.add_mkaero2([m], [rf])

# insert model.add_spline4
model.add_spline4(int(1), int(103001), int(1), int(1), float(), 'FPS', 'BOTH', int(10), int(10)) #Still considering which spline is suitable
# model.add_spline2(int(1), int(105001), int(103001), int(105067), int(1), float(0.), float(1.), int(0), float(0.), float(0.), 'BOTH')

# manage flfact
seaAD = 1.225E-12
cruiseAD = 8.170E-13
model.add_flfact(1, [float(cruiseAD/seaAD)]) # density set
model.add_flfact(2, [float(0.0)]) # velocity set
model.add_flfact(3, v3ValueList) # mach and reduced freqency set

# insert model.add_flutter
model.add_flutter(1, 'PK', 1, 2, 3, 'L', None, None, float(1E-3))

# write bdf file
model.validate()
bdf145_filename_out = os.path.join('sol145_caero4.bdf')
model.write_bdf(bdf145_filename_out, enddata=True)
print(bdf145_filename_out)
print("====> write bdf file success!")
