import os
from pyNastran.bdf.bdf import BDF, CaseControlDeck
model = BDF()

E = 72397.0
G = 27000.0
nu = 0.32
rho = 0.0000000000000001
mat = model.add_mat1(1, E, G, nu, rho)

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

# open node.dat file_Wing
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

# insert model.add_grid(id_no, x, y, z) for 1_nodes.dat
for i, x, y, z, xl, xt in zip(idList, xValueList, yValueList, zValueList, xLeValueList, xTelueList):
    model.add_grid(int(i), [float(x), float(y), float(z)])
    model.add_grid(24+2*int(i), [float(xl), float(y), float(z)])
    model.add_grid(25+2*int(i), [float(xt), float(y), float(z)])

# insert model.add_conm1(id_conm1, id_no, Mlump)
for j, i, m, s, iyy in zip(conm1List, idList, mass, firstMoment, iYy):
    model.add_card(['CONM1', int(j)+10000, int(i), 0,
                    float(m),
                    0.0, float(m),
                    0.0, 0.0, float(m),
                    0.0, 0.0, 0.0, 0.0,
                    0.0, 0.0, float(s), 0.0, float(iyy),
                    0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'CONM1')

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


# eigrl = model.add_eigrl(10, None, None, 10, 0, None, None, 'MASS', None, None) # how many want to mode
eigrl = model.add_eigrl(10, nd=10, msglvl=0)
model.sol = 103  # start=103
cc = CaseControlDeck([
    'SUBCASE 1',
    'SUBTITLE = Default',
    'METHOD = 10', #number of nd
    'SPC = %s' % spc_id,
    'VECTOR(SORT1,PUNCH, REAL)=ALL',
    'SPCFORCES(SORT1, REAL) = ALL',
    'BEGIN BULK',
    'SET 99 = 1,THRU, 10', #which mode do you want to print
    'MEFFMASS(ALL) = YES'
])
model.case_control_deck = cc
model.validate()

model.add_param('POST', [0]) #print result. 0 = .xdb, -1 = .op2
model.add_param('PRTMAXIM', ['YES'])
model.add_param('OMODES', ['ALL']) #Output for extracted modes will be computed.(all=default)
model.add_param('WTMASS', [1.])

bdf_filename_out = os.path.join('sol103_addstrip.bdf')
model.write_bdf(bdf_filename_out, enddata=True)
print(bdf_filename_out)

print('----------------------------------------------------------------------------------------------------')