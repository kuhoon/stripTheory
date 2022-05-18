import os
from pyNastran.bdf.bdf import *
import numpy as np

nodesFileName = "datFiles_numbering/1_nodes.dat"
lumpFileName = "datFiles_numbering/2_mass_lump.dat"
concFileName = "datFiles_numbering/3_mass_conc.dat"
elementsFileName = "datFiles_numbering/4_elements.dat"
sectionFileName = "datFiles_numbering/5_data_planform.dat"
machFileName = "datFiles_numbering/6_machNum.dat"
rrfFileName = "datFiles_numbering/7_redRF.dat"
v3FileName = "datfiles_numbering/8_v3.dat"

model = BDF()

idList = [] #declare a variable. start on the first line
xValueList = []
yValueList = []
zValueList = []
xLeValueList = []
xTelueList = []
conm1List = []
conm2List = []
mass = []
iYy = []
firstMoment = []
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
rechord = []

E = 72397.0
G = 27000.0
nu = 0.32
rho = 0.0000000000000001
mat = model.add_mat1(1, E, G, nu, rho)

# ====================================================================
# =========================== OPEN FILES =============================
# ====================================================================

# open 1_node.dat file_Wing
with open("datFiles_numbering/1_data_nodes.dat") as datFile:
    nodeValueList = [data.split() for data in datFile]
    del nodeValueList[0] # delete line 0
    for v in nodeValueList:
        idList.append(v[0]) # add list element
        xValueList.append(v[1])
        yValueList.append(v[2])
        zValueList.append(v[3])
        xLeValueList.append(v[5])
        xTelueList.append(v[6])

# open mass_lump.dat file_Wing
with open("datFiles_numbering/2_data_masses.dat") as datFile:
    lumpValueList = [data.split() for data in datFile]
    del lumpValueList[0]
    for v in lumpValueList:
        conm1List.append(v[0]) #conm1list 1-100
        mass.append(v[2])
        iYy.append(v[3])
        firstMoment.append(v[4])

# open mass_lump.dat file_Wing
with open("datFiles_numbering/2_mass_lump_add.dat") as datFile:
    lumpValueList1 = [data.split() for data in datFile]
    del lumpValueList1[0]
    for v in lumpValueList1:
        conm2List.append(v[0]) #conm1list 1-100
        mLump.append(v[2])

# open elements.dat file_pbeam
with open("datFiles_numbering/4_data_elements.dat") as datFile:
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
    'VECTOR(SORT1,REAL) = ALL',
    'SPCFORCES(SORT1, REAL) = ALL',
    'BEGIN BULK',
    'ANALYSIS = FLUTTER',
    'AESYMXY = Asymmetric',
    'AESYMXZ = Symmetric',
    'FMETHOD = 1',
    'SET 99 = 1,THRU, 10' #output EIGENVALUE in .06 file. The current state has requested to print all of the numbers 1 to 10.
    # 'OUTPUT(XYPLOT)'
    # 'PLOTTER NASTRAN',
    # 'CURVELINESYMBOL = -6',
    # 'CSCALE = 2.0',
    # 'YTTITLE = DAMPING G',
    # 'YBTITLE = FREQUENCY F HZ',
    # 'XTITLE = VELOCITY V (MM/SEC)',
    # 'XMIN = 52000',
    # 'XMAX = 239300',
    # 'YTMIN = -1',
    # 'YTMAX = 2',
    # 'YBMAX = 5',
    # 'YBMAX = 30',
    # 'XTGRID LINES = YES',
    # 'XBGRID LINES = YES',
    # 'YTGRID LINES = YES',
    # 'YBGRID LINES = YES',
    # 'UPPER TICS = -1',
    # 'TRIGHT TICS = -1',
    # 'BRIGHT TICS = -1',
    # 'XYPLOT = VG / 1(G,F) 2(G,F) 3(G,F) 4(G,F) 5(G,F)'
])
model.case_control_deck = cc
model.validate()

# model.add_mat1(1, E, G, nu, rho)

model.add_param('POST', [-1]) #print result. 0 = .xdb, -1 = .op2
model.add_param('PRTMAXIM', ['YES'])
model.add_param('SNORM', [20.0])
model.add_param('WTMASS', [1.0])  # default = 1.0
model.add_param('Aunit', [1.0])
model.add_param('OMODES', ['ALL']) #Output for extracted modes will be computed.(all=default)
model.add_param('WTMASS', [1.])

# insert model.add_grid(id_no, x, y, z) for 1_nodes.dat
for i, x, y, z, xl, xt in zip(idList, xValueList, yValueList, zValueList, xLeValueList, xTelueList):
    model.add_grid(int(i), [float(x), float(y), float(z)])
    model.add_grid(24+2*int(i), [float(xl), float(y), float(z)])
    model.add_grid(25+2*int(i), [float(xt), float(y), float(z)])

# insert model.add_conm1(id_conm1, id_no, Mlump)
for j, i, m, s, iyy in zip(conm1List, idList, mass, firstMoment, iYy):
    model.add_card(['CONM1', int(j)+10000, int(i), 0,
                    float(m),
                    0., float(m),
                    0., 0., float(m),
                    0., 0., 0., 0.,
                    0., 0., float(s), 0., float(iyy),
                    0., 0., 0., 0., 0., 0.], 'CONM1')

# # insert model.add_conm2(id_conm2, id_no, Mlump)
for j, m in zip(conm2List, mLump):
    model.add_conm2(int(j)+10000, int(j), float(m))

# insert model.add_pbeam(id_pbeam, mid, x/xb, so, area, i1, i2, i12, j)
for p, a, i1, i2, j in zip(pbeamList, areaList, i1List, i2List, jList):
    model.add_pbeam(int(p), 1, [0.0], ['YES'], [float(a)], [float(i1)], [float(i2)], [0], [float(j)], k1=1., k2=1.)

# insert model.add_cbeam
for p, idFrom, idTo in zip(pbeamList, idFromList, idToList):
    model.add_cbeam(int(p), int(p), [int(idFrom), int(idTo)], [0., 0., 1.], None)

# insert model.add_spc1
spc_id = 50
model.add_spc1(spc_id, '123456', [1, 2, 3])

# insert model.add_rbe2
for i in range(1,26):
    model.add_rbe2(150+i, i, '123456', [24+2*i])
    model.add_rbe2(176+i, i, '123456', [25+2*i])

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
aef = [aef1, aef2, aef3]
for i in aef:
    model.add_aefact(eIdAef, i)
    eIdAef += 1

# insert model.add_paero4, caero4
chord0 = np.zeros(5) #paero4 for docs, caocs, gapocs, 5 strip
reChord0 = chord0.tolist()
chord1 = np.zeros(14) # 14 strip
reChord1 = chord1.tolist()
chord2 = np.zeros(67) # 67 strip
reChord2 = chord2.tolist()
model.add_paero4(103000, docs=reChord0, caocs=reChord0, gapocs=reChord0, cla=int(0), lcla=int(0), circ=int(0), lcirc=int(0))  # docs, caocs, gapocs with control surface, default =0. no Control surface
model.add_paero4(104000, docs=reChord1, caocs=reChord1, gapocs=reChord1, cla=int(0), lcla=int(0), circ=int(0), lcirc=int(0))  # docs, caocs, gapocs with control surface, default =0. no Control surface
model.add_paero4(105000, docs=reChord2, caocs=reChord2, gapocs=reChord2, cla=int(0), lcla=int(0), circ=int(0), lcirc=int(0))  # docs, caocs, gapocs with control surface, default =0. no Control surface

# insert model.add_caero4
eId2 = 103000
eIdAef1 = 70
for i in range(len(idSectList) - 1): #make for strip
    model.add_caero4(eId2+1, eId2, np.array(ptList[i], float), float(cList[i]), np.array(ptList[i + 1], float), float(cList[i + 1]), 0, 0, eIdAef1)
    eIdAef1 += 1
    eId2 += 1000

# insert model.add_set1, aero, aeros
model.add_set1(1, idList)
model.add_aero(float(1.0), float(1984.0), float(1.225E-12), 0)  # velocity, aerodynamic chord, density scal, coord
model.add_aeros(float(1984.0), float(17174.0), float(3.227E7 / 2), 0, 0)  # half span model => must used half area

for m in machValueList: #want to make data list for mach and reduced frequency
    for rf in rrfValueList:
        model.add_mkaero2([m], [rf])

# insert model.add_spline2
model.add_card(['SPLINE2', 1, 103001, 103001, 103005, 1, 0., 1., 0, 0., 0., None, 'BOTH'], 'SPLINE2')
model.add_card(['SPLINE2', 2, 104001, 104001, 104014, 1, 0., 1., 0, 0., 0., None, 'BOTH'], 'SPLINE2')
model.add_card(['SPLINE2', 3, 105001, 105001, 105067, 1, 0., 1., 0, 0., 0., None, 'BOTH'], 'SPLINE2')

# manage flfact
seaAD = 1.225E-12
cruiseAD = 8.170E-13

# density set
model.add_flfact(1, [float(cruiseAD/seaAD)])

# velocity set, bis zum oberen Geschwindigkeitslimit von 150% der Geschwindigkeit v_D durch, das heißt maximal 1.5 * 159.5 m/s = 239.3 m/s
model.add_flfact(2, [float(0.0)])

# mach and reduced freqency set
model.add_flfact(3, v3ValueList)

# insert model.add_flutter
model.add_flutter(1, 'PK', 1, 2, 3, 'L', None, None, float(1E-3))

# write bdf file
model.validate()
bdf145_filename_out = os.path.join('sol145_caero4_add.bdf')
model.write_bdf(bdf145_filename_out, enddata=True)
print(bdf145_filename_out)
print("====> write bdf file success!")
