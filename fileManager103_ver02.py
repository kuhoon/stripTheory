import os

# from IPython.display import HTML as html_print
from pyNastran.bdf.bdf import BDF, CaseControlDeck
model = BDF()

E = 72397.0
G = 27000.0
nu = 0.32
rho = 0.0000000000000001
mat = model.add_mat1(1, E, G, nu, rho)

idList = [] #변수 선언. 첫줄에서 시작
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

# open node.dat file_Wing
with open("datFiles_numbering/1_nodes.dat") as datFile:
    nodeValueList = [data.split() for data in datFile]
    del nodeValueList[0] # 0번 행을 지워라
    for v in nodeValueList:
        idList.append(v[0]) # list 원소 추가
        xValueList.append(v[1])
        yValueList.append(v[2])
        zValueList.append(v[3])

# open mass_lump.dat file_Wing
with open("datFiles_numbering/2_mass_lump.dat") as datFile:
    lumpValueList = [data.split() for data in datFile]
    del lumpValueList[0]
    for v in lumpValueList:
        conm2List.append(v[0]) #conm2list 1-100
        mLump.append(v[2])

# open mass_conc.dat file_Main Engine, Landing Gear
with open("datFiles_numbering/3_mass_conc.dat") as datFile:
    massValueList = [data.split() for data in datFile]
    del massValueList[0]
    for v in massValueList:
        idList.append(v[0])
        xValueList.append(v[2])
        yValueList.append(v[3])
        zValueList.append(v[4])
        conm2List.append(v[1]) #conm2list 100, 101 리스트 순서상 100번 101번이 뒤로 와야함.
        mLump.append(v[5])

# open elements.dat file_pbeam
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

# insert model.add_grid(id_no, x, y, z)
for i, x, y, z in zip(idList, xValueList, yValueList, zValueList):
    model.add_grid(int(i), [float(x), float(y), float(z)])

# insert model.add_conm2(id_conm2, id_no, Mlump)
for j, i, m in zip(conm2List, idList, mLump):
    model.add_conm2(int(j)+10000, int(i), float(m))

# insert model.add_pbeam(id_pbeam, mid, x/xb, so, area, i1, i2, i12, j)
for p, a, i1, i2, j in zip(pbeamList, areaList, i1List, i2List, jList):
    model.add_pbeam(int(p), 1, [0.0], ['YES'], [float(a)], [float(i1)], [float(i2)], [0], [float(j)], k1=1., k2=1.)

# insert model.add_cbeam
for p, idFrom, idTo in zip(pbeamList, idFromList, idToList):
    model.add_cbeam(int(p), int(p), [int(idFrom), int(idTo)], [], 100)

spc_id = 50
model.add_spc1(spc_id, '123456', [1])

model.add_rbe2(51, 8, '123456', [100])
model.add_rbe2(52, 8, '123456', [101])


# eigrl = model.add_eigrl(10, None, None, 10, 0, None, None, 'MASS', None, None) # how many want to mode
eigrl = model.add_eigrl(10, nd=10, msglvl=0)
model.sol = 103  # start=103
cc = CaseControlDeck([
    'SUBCASE 1',
    'SUBTITLE = Default',
    'METHOD = 10', #number of nd
    'SPC = %s' % spc_id,
    'VECTOR(SORT1,REAL)=ALL',
    'SPCFORCES(SORT1, REAL) = ALL',
    'BEGIN BULK',
])
model.case_control_deck = cc
model.validate()

model.add_param('POST', [0])
model.add_param('PRTMAXIM', ['YES'])

bdf_filename_out = os.path.join('sol103_ver04.bdf')
model.write_bdf(bdf_filename_out, enddata=True)
print(bdf_filename_out)

print('----------------------------------------------------------------------------------------------------')