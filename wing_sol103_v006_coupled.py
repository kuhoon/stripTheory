# PYTHON PACKAGES
#################
# Import packages
import os
import pyNastran

# Import methods
# from IPython.display import HTML as html_print
from pyNastran.bdf.bdf import BDF, CaseControlDeck

# Instantiate FE model
model = BDF()


# LISTS
#######
# Initialize empty lists for storing input data
# Nodes
list_node_ID = []
list_node_x = []
list_node_y = []
list_node_z = []
# LE and TE nodes
list_node_LE_ID = []
list_node_LE_x = []
list_node_TE_ID = []
list_node_TE_x = []
# Lumped and concentrated masses
list_CONM_ID = []
list_CONM_node = []
list_CONM_mass = []
list_CONM_inertia = []
list_CONM_moment = []
# Beam elements
list_beam_ID = []
list_beam_area = []
list_beam_I1 = []
list_beam_I2 = []
list_beam_I12 = []
list_beam_J = []
list_beam_node1 = []
list_beam_node2 = []
# LE and TE beam elements
list_beam_LE_ID = []
list_beam_TE_ID = []
list_beam_LTE_node1 = []
list_beam_LE_node2 = []
list_beam_TE_node2 = []


# DATA INPUT
############

# Path to folder containing external files with input data
path_data = 'data_input_v006/'

# Material
MID = 1 # Material ID
E = 72397.5 # Young's modulus [MPa]
G = 27000.0 # Shear modulus [MPa]
NU = 0.32 # Poisson ratio [-]
# RHO = 1e-15 # Density [t/mm3] # not required for sol103

# Nodes
with open(path_data + 'data_nodes.dat') as dat_file:
    list_nodes = [data.split() for data in dat_file]
    del list_nodes[0] # Delete header row
    for row in list_nodes:
        list_node_ID.append(row[0]) # Node ID
        list_node_x.append(row[1]) # x-coordinate of node [mm]
        list_node_y.append(row[2]) # y-coordinate of node [mm]
        list_node_z.append(row[3]) # z-coordinate of node [mm]
        list_node_LE_x.append(row[5]) # x-coordinate of LE node [mm]
        list_node_TE_x.append(row[6]) # x-coordinate of TE node [mm]

# LE and TE nodes
for i in range(len(list_node_ID)):
    list_node_LE_ID.append(int(list_node_ID[i]) + 100)
    list_node_TE_ID.append(int(list_node_ID[i]) + 200)

# Masses
with open(path_data + 'data_masses.dat') as dat_file:
    list_masses = [data.split() for data in dat_file]
    del list_masses[0] # Delete header row
    for row in list_masses:
        list_CONM_ID.append(row[0]) # CONM2 ID
        list_CONM_node.append(row[1]) # ID of existing node
        list_CONM_mass.append(row[2]) # Mass of lumped mass [t]
        list_CONM_inertia.append(row[3]) # Mass moment of inertia [t*mm2]
        list_CONM_moment.append(row[4]) # Static moment [t*mm]

# Beam elements
with open(path_data + 'data_elements.dat') as dat_file:
    list_elements = [data.split() for data in dat_file]
    del list_elements[0] # Delete header row
    for row in list_elements:
        list_beam_ID.append(row[0]) # Beam element ID
        list_beam_node1.append(row[1]) # Start node of beam element
        list_beam_node2.append(row[2]) # End node of beam element
        list_beam_area.append(row[3]) # Cross-sectional area [mm2]
        list_beam_I1.append(row[4]) # Second area moment of inertia about 1-axis [mm4]
        list_beam_I2.append(row[5]) # Second area moment of inertia about 2-axis [mm4]
        list_beam_I12.append(row[6]) # Deviation area moment of inertia [mm4]
        list_beam_J.append(row[7]) # Mass moment of inertia [t*mm2]

# LE and TE beam elements
for i in range(len(list_node_ID)):
    list_beam_LE_ID.append(int(list_node_ID[i]) + 100)
    list_beam_TE_ID.append(int(list_node_ID[i]) + 200)
    list_beam_LTE_node1.append(int(list_node_ID[i])) # Start node of beam element
    list_beam_LE_node2.append(list_node_LE_ID[i]) # End node of beam element
    list_beam_TE_node2.append(list_node_TE_ID[i]) # End node of beam element
beam_LE_prop_val = 1e+11 # [mm2], [mm4]
beam_TE_prop_val = 1e+11 # [mm2], [mm4]
beam_LE_prop_ID = 100 # ID
beam_TE_prop_ID = 200 # ID
    
# # Couplings
# RBE2_ID_1 = 51 # RBE2 ID
# RBE2_no_indep_1 = 8 # ID of independet node
# RBE2_DOF_1 = '123456' # Degress of freedom
# RBE2_no_dep_1 = [100] # Set of IDs of dependet nodes

# RBE2_ID_2 = 52 # RBE2 ID
# RBE2_no_indep_2 =8 # ID of independet node
# RBE2_DOF_2 = '123456' # Degress of freedom
# RBE2_no_dep_2 = [101] # Set of IDs of dependet nodes

# Boundary conditions
SPC_ID = 900 # SPC ID
BC = '123456' # Component numbers of fixed degress of freedom
list_BC_nodes = [1,2,3] # Grid identification numbers (node IDs)


# MODEL GENERATION
##################

# Create material property as MAT1
# model.add_mat(MID, E, G2, NU, RHO)
mat1 = model.add_mat1(MID, E, G, NU)
  
# Create nodes as GRID
for ID, X1, X2, X3 in zip(list_node_ID, list_node_x, list_node_y, list_node_z):
    # model.add_grid(nid: int, xyz: Union[None, List[float], Any], cp: int = 0, cd: int = 0, 
    #                ps: str = '', seid: int = 0, comment: str = '')
    # here:        NID       xyz[list]
    model.add_grid(int(ID), [float(X1), float(X2), float(X3)])
    
# Create LE and TE nodes as GRID
for ID, X1_LE, X1_TE, X2, X3 in zip(list_node_ID, list_node_LE_x, list_node_TE_x, list_node_y, list_node_z):
    # model.add_grid(nid: int, xyz: Union[None, List[float], Any], cp: int = 0, cd: int = 0, 
    #                ps: str = '', seid: int = 0, comment: str = '')
    # here:        NID       xyz[list]
    model.add_grid(int(ID)+100, [float(X1_LE), float(X2), float(X3)])
    model.add_grid(int(ID)+200, [float(X1_TE), float(X2), float(X3)])    
    
# Create lumped and concentrated masses as CONM1 elements   
for j, G, M, Iyy, Syx in zip(list_CONM_ID, list_CONM_node, list_CONM_mass, list_CONM_inertia, list_CONM_moment):
    # add_card(card, comment='')
    # here:         [CONM1, eid: int, nid: int, cid: int, 
    #               M11, 
    #               M21, M22, 
    #               M31, M32, M33, 
    #               M41, M42, M43, M44, 
    #               M51, M52, M53, M54, M55, 
    #               M61, M52, M63, M64, M65, M66], 'CONM1'
    model.add_card(['CONM1', int(j)+1000, int(G), 0, 
                    float(M), 
                    0.0, float(M), 
                    0.0, 0.0, float(M), 
                    0.0, 0.0, 0.0, 0.0, 
                    0.0, 0.0, float(Syx), 0.0, float(Iyy), 
                    0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'CONM1')    

# # Create lumped and concentrated masses as CONM2 elements
# for j, G, M, I22 in zip(list_CONM_ID, list_CONM_node, list_CONM_mass, list_CONM_inertia):
#     # model.add_conm2(eid: int, nid: int, mass: float, cid: int = 0, 
#     #                 X: Optional[List[float]] = None, I: Optional[List[float]] = None, comment: str = '')
#     # here:         EID          NID     mass      CID     X[list]
#     #               I[list]
#     model.add_conm2(int(j)+1000, int(G), float(M), 
#                     I=[0.0, 0.0, float(I22), 0.0, 0.0, 0.0])
     
# Create properties for beam elements as PBEAM entries
for PID, A, I1, I2, I12, J in zip(list_beam_ID, list_beam_area, 
                                  list_beam_I1, list_beam_I2, list_beam_I12, list_beam_J):
    #model.add_pbeam(pid, mid, xxb, so, area, i1, i2, i12, j, 
    #                nsm=None, c1=None, c2=None, d1=None, d2=None, e1=None, e2=None, f1=None, f2=None, 
    #                k1=1.0, k2=1.0, s1=0.0, s2=0.0, nsia=0.0, nsib=None, cwa=0.0, cwb=None, 
    #                m1a=0.0, m2a=0.0, m1b=None, m2b=None, n1a=0.0, n2a=0.0, n1b=None, n2b=None, comment='')
    # here:         PID      MID x/xb   SO       area
    #               I1           I2           I12           J           k1     k2
    model.add_pbeam(int(PID), 1, [0.0], ['YES'], [float(A)], 
                    [float(I1)], [float(I2)], [float(I12)], [float(J)], k1=1., k2=1.)
    
# Create properties for LE and TE beam elements as PBEAM entries
#model.add_pbeam(pid, mid, xxb, so, area, i1, i2, i12, j, 
#                nsm=None, c1=None, c2=None, d1=None, d2=None, e1=None, e2=None, f1=None, f2=None, 
#                k1=1.0, k2=1.0, s1=0.0, s2=0.0, nsia=0.0, nsib=None, cwa=0.0, cwb=None, 
#                m1a=0.0, m2a=0.0, m1b=None, m2b=None, n1a=0.0, n2a=0.0, n1b=None, n2b=None, comment='')
# here:         PID      MID x/xb   SO       area
#               I1           I2           I12           J           k1     k2
model.add_pbeam(int(beam_LE_prop_ID), 1, [0.0], ['YES'], [float(beam_LE_prop_val)], 
                [float(beam_LE_prop_val)], [float(beam_LE_prop_val)], [0.0], [float(beam_LE_prop_val)], k1=1., k2=1.)
model.add_pbeam(int(beam_TE_prop_ID), 1, [0.0], ['YES'], [float(beam_TE_prop_val)], 
                [float(beam_TE_prop_val)], [float(beam_TE_prop_val)], [0.0], [float(beam_TE_prop_val)], k1=1., k2=1.)
    
# Create beams as CBEAM elements
for ID, GA, GB in zip(list_beam_ID, list_beam_node1, list_beam_node2):
    # model.add_cbeam(eid, pid, nids, x, g0, offt='GGG', bit=None, pa=0, pb=0, 
    #                 wa=None, wb=None, sa=0, sb=0, comment='')
    # here:         EID      PID      NIDS[list]       X[list] g0
    model.add_cbeam(int(ID), int(ID), [int(GA), int(GB)], [0.0, 0.0, 1.0], None)
    
# Create LE and TE beams as CBEAM elements
for ID_LE, ID_TE, GA, GB_LE, GB_TE in zip(list_beam_LE_ID, list_beam_TE_ID, 
                                          list_beam_LTE_node1, list_beam_LE_node2, list_beam_TE_node2):
    # model.add_cbeam(eid, pid, nids, x, g0, offt='GGG', bit=None, pa=0, pb=0, 
    #                 wa=None, wb=None, sa=0, sb=0, comment='')
    # here:         EID      PID      NIDS[list]       X[list] g0
    model.add_cbeam(int(ID_LE), int(beam_LE_prop_ID), [int(GA), int(GB_LE)], [0.0, 0.0, 1.0], None)
    model.add_cbeam(int(ID_TE), int(beam_TE_prop_ID), [int(GA), int(GB_TE)], [0.0, 0.0, 1.0], None)

# Create couplings
# model.add_rbe2(eid, gn, cm, Gmi, alpha: float = 0.0, tref: float = 0.0, comment='')
# here:        EID        GN               CM          GMi
# model.add_rbe2(RBE2_ID_1, RBE2_no_indep_1, RBE2_DOF_1, RBE2_no_dep_1)
# model.add_rbe2(RBE2_ID_2, RBE2_no_indep_2, RBE2_DOF_2, RBE2_no_dep_2)

# Create boundary conditions
# model.add_spc1(conid, components, nodes, comment='')
# here:        CONID compDOF nodes[list]
model.add_spc1(SPC_ID, BC, list_BC_nodes)


# ANALYSIS SETTINGS
###################

# Create normal modes analysis step
# model.add_eigrl(sid, v1=None, v2=None, nd=None, msglvl=0, 
#                 maxset=None, shfscl=None, norm=None, options=None, values=None, comment='')
# here:                SID ND     MSGLVL    Norm
eigrl = model.add_eigrl(5, nd=12, msglvl=0, norm='MAX')

# Set type of solution
model.sol = 103 # 103: normal modes analysis

# Write input deck
cc = CaseControlDeck([
    'SUBCASE 1', # case ID
    'SUBTITLE = Ref2025_220421_flex_f050',
    'METHOD = 5', # method ID
    'SPC = %s' % SPC_ID, # SPC ID
    'VECTOR(SORT1,REAL)=ALL',
    'SPCFORCES(SORT1, REAL) = ALL',
    'BEGIN BULK',
])
model.case_control_deck = cc
model.validate()

model.add_param('POST', [0])
model.add_param('PRTMAXIM', ['YES'])


# BDF FILE
##########
# Set path and name of bdf file
bdf_filename_out = os.path.join('sol103_Ref2025_220421_flex_f050_coupled.bdf')
# Write bdf file
model.write_bdf(bdf_filename_out, enddata=True)

print(bdf_filename_out)


print(50*"-", "\nGeneration of bdf file finished.\n", 50*"-")