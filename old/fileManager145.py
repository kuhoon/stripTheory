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

nodeIdList = []     # ID in node file
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
bSpanList = []
aelistList = []
eId = 201
ptList = []  # [ [], [], [] ]

E = 72397.0
G = 27000.0
nu = 0.32
rho = 0.0000000000000001

# ====================================================================
# =========================== OPEN FILES =============================
# ====================================================================

# open 1_node.dat file_Wing
with open(nodesFileName) as datFile:
    nodeValueList = [data.split() for data in datFile]
    del nodeValueList[0]  # 0번 행을 지워라
    for v in nodeValueList:
        nodeIdList.append(int(v[0]))
        xValueList.append(v[1])
        yValueList.append(v[2])
        zValueList.append(v[3])

# open 2_mass_lump.dat file_Wing
with open(lumpFileName) as datFile:
    lumpValueList = [data.split() for data in datFile]
    del lumpValueList[0]
    for v in lumpValueList:
        conm2List.append(v[0])  # conm2list 1-100
        mLump.append(v[2])

# open 3_mass_conc.dat file_Main Engine, Landing Gear
with open(concFileName) as datFile:
    massValueList = [data.split() for data in datFile]
    del massValueList[0]
    for v in massValueList:
        nodeIdList.append(v[0])
        xValueList.append(v[2])
        yValueList.append(v[3])
        zValueList.append(v[4])
        conm2List.append(v[1])  # conm2list 100, 101 리스트 순서상 100번 101번이 뒤로 와야함.
        mLump.append(v[5])

# open 4_elements.dat file_pbeam
with open(elementsFileName) as datFile:
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
    del sectValueList[0]  # 0번 행을 지워라
    for v in sectValueList:
        idSectList.append(v[0])
        xLeList.append(v[1])  # list 원소 추가
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
model.case_control_deck = CaseControlDeck([
    'SUBCASE 1',
    'SUBTITLE = Default',
    'METHOD = 1',
    'SPC = 2',
    'SVECTOR(SORT1,REAL) = ALL',
    'SPCFORCES(SORT1, REAL) = ALL',
    'BEGIN BULK',
    'ANALYSIS = FLUTTER',
    'AESYMXY = Asymmetric',
    'AESYMXZ = Symmetric',
    'FMETHOD = 1'
])

model.add_mat1(1, E, G, nu, rho)

model.add_param('POST', [0])
model.add_param('PRTMAXIM', ['YES'])
model.add_param('SNORM', [20.0])
model.add_param('WTMASS', [1.0])  # default = 1.0
# model.add_param('Aunit', [1.0])

# insert model.add_grid(id_no, x, y, z)
for i, x, y, z in zip(nodeIdList, xValueList, yValueList, zValueList):
    model.add_grid(int(i), [float(x), float(y), float(z)])

# insert model.add_conm2(id_conm2, id_no, Mlump)
for j, i, m in zip(conm2List, nodeIdList, mLump):
    model.add_conm2(int(j)+1000, int(i), float(m))

# insert model.add_pbeam(id_pbeam, mid, x/xb, so, area, i1, i2, i12, j)
for p, a, i1, i2, j in zip(pbeamList, areaList, i1List, i2List, jList):
    model.add_pbeam(int(p), 1, [0.0], ['YES'], [float(a)], [float(i1)], [float(i2)], [0], [float(j)])

# insert model.add_cbeam
for p, idFrom, idTo in zip(pbeamList, idFromList, idToList):
    model.add_cbeam(int(p), int(p), [int(idFrom), int(idTo)], [], int(100))

# insert model.add_spc1, spcadd
model.add_spc1(int(50), '123456', [int(1)])
model.add_spcadd(2, 50)

# insert model.add_rbe2
model.add_rbe2(int(51), int(8), '123456', [int(100)])
model.add_rbe2(int(52), int(8), '123456', [int(101)])

# insert model.add_eigrl
model.add_eigrl(int(1), '', '', 10, 0)  # how many want to mode

# <=========== sol 145 ===============>
# insert model.add_point(id_no, x, y, z)
for x, y, z, c in zip(xLeList, yLeList, zLeList, cList):
    model.add_point(eId, [float(x), float(y), float(z)])
    ptList.append([float(x), float(y), float(z)])
    eId = eId + 1
    model.add_point(eId, [float(x) + float(c), float(y), float(z)])
    eId = eId + 1

# insert model.add_paero1, caero1
eId2 = 103001
nCh = 5  # 나스트란 기본설정. chord 박스 5개
b1Span = float(yLeList[1]) - float(yLeList[0])  # span 길이를 균일하게 하기위한.
for i in range(len(idSectList) - 1):  # leg, list = 길이, 원소의 갯수
    bSpan = round((float(yLeList[i + 1]) - float(yLeList[i])) * nCh / b1Span)  # round 반올림
    model.add_paero1(eId2)
    model.add_caero1(eId2, eId2, 1, np.array(ptList[i], float), float(cList[i]), np.array(ptList[i + 1], float), float(cList[i + 1]), 0, bSpan, 0, nCh, 0)
    eId2 += 1000
    bSpanList.append(bSpan)

# insert model.add_set1, aero, aeros
model.add_set1(1, nodeIdList)

model.add_aero(float(1.0), float(1984.0), float(1.228E-12), 0)  # velocity, aerodynamic chord, density scal, coord
model.add_aeros(float(1984.0), float(17174.0), float(3.227E7/2.0), 0, 0)  # half span model => half area

# insert model.add_mkaero2
for m in machValueList:
    for rf in rrfValueList:
        model.add_mkaero2([m], [rf])

# insert model.add_spline4
model.add_spline4(int(1), int(105001), int(1), int(1), float(), 'FPS', 'BOTH', int(10), int(10))

# manage aelist
eId2 = eId2 - (1000 * len(bSpanList))
for i in range(len(bSpanList)):
    for b in range(bSpanList[i] * 5):
        aelistList.append(eId2 + b)
    eId2 += 1000

model.add_aelist(1, aelistList)  # 그물망 수(우리가 설정한. 예를 들어 33x5면 165개

# manage flfact
seaAD = 1.225E-12
cruiseAD = 8.170E-13
model.add_flfact(1, [float(cruiseAD/seaAD)])
model.add_flfact(2, [float(0.0)])
model.add_flfact(3, v3ValueList)

# insert model.add_flutter
model.add_flutter(1, 'PK', 1, 2, 3, 'L', None, None, float(1E-3))

# write bdf file
model.validate()
bdf103_filename_out = os.path.join('sol145_ver05_usingOwnFile.bdf')
model.write_bdf(bdf103_filename_out, enddata=True)
print(bdf103_filename_out)
print("====> write bdf file success!")
