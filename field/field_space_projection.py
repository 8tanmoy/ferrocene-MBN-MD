
#--field calculation second version--
#--tanmoy jun 19, 2020--
"""
tasks
_____
for each time:
    1. decomposition of electric field
    3. make sure the layer on the opposite side is not taken into account
"""
import shutil
import matplotlib.pyplot as plt
import os
import sys
import subprocess as sp
import numpy as np
import copy
import time
np.set_printoptions(threshold=sys.maxsize)

#--constants--
gro2si = 1.602176 * 9.0 * 0.1
#print(f"gro2si = {gro2si}")

root    =   '/projectnb/cui-buchem/tanmoy/projects/FERRO/c6-mbn/prod2/'
drf     =   root + '../field_time'
wrk     =   os.getcwd()
r_cut   =   3.5

#--process gro file--
#--inp : .gro file path--
#--out : 1> timestamp 2> boxinfo 3> n_atoms (debug) 4> coordonate array
def process_gro(coord_path):
    f1 = open(coord_path, "r")
    arr = list()
    for line in f1:
        arr.append(line)
    f1.close()
    tstamp = arr[0]
    nat = int(arr[1])
    boxinfo = arr[-1].split()
    arr = arr[2:-1]
    molinfo = list()        #information array
    #--06/22--
    for jj in arr:
        temp_resid      = jj[0:5].strip()
        temp_resname    = jj[5:10].strip()
        temp_atname     = jj[10:15].strip()
        temp_idx        = jj[15:20].strip()
        molinfo.append([temp_resid, temp_resname, temp_atname, temp_idx])
    #print(molinfo)
    arr = [ii.split() for ii in arr]
    arr = [ii[-3:] for ii in arr]                                           #new
    assert nat == len(arr), "natoms error in process_gro function"
    assert len(arr[0]) == len(arr[-1]), "len error in process_gro"
    assert len(molinfo) == len(arr), "len molinfo != len coordinates"
    #--zip molinfo and coordinates--
    for ii in range(len(molinfo)):
        molinfo[ii].extend(arr[ii])
    return(tstamp, nat, boxinfo, molinfo)

def read_charges(ch_path):
    f1 = open(ch_path, "r")
    arr = list()
    for line in f1:
        arr.append(line.split())
    # --resname--atomanme--charge--
    f1.close()
    return(arr)

def calc_maxmin(arr_coord):
    x_arr   = [ float(row[0]) for row in arr_coord]
    y_arr   = [ float(row[1]) for row in arr_coord]
    z_arr   = [ float(row[2]) for row in arr_coord]
    print(f"xmax = {np.max(x_arr)}\t\
xmin = {np.min(x_arr)}\n\
ymax = {np.max(y_arr)}\t\
ymin = {np.min(y_arr)}\n\
zmax = {np.max(z_arr)}\t\
zmin = {np.min(z_arr)}\n")
    return

def get_ref_idx(fname):
    f1 = open(fname, "r")
    data_idx    = f1.read().replace('\n',' ')
    data_idx    = data_idx.split()
    f1.close()
    print("ref array passed from ", fname)
    return(data_idx)

def strip_gold(withGold):
    noGold = list()
    for item in withGold:
        #--item[2] is atomname--
        if item[2][:2] != 'AU':
            noGold.append(item)
    return(noGold)

def add_charges(noCharge, chargeList):
    for item in noCharge:
        selectAtom = [ float(ii[2]) for ii in chargeList if (ii[0] == item[1] and ii[1] == item[2]) ]
        item.append(selectAtom[0])  #because using list comprehension
    return(noCharge)

def calc_field(refIndex, noGold, boxDim, chargeList, rcut):
    inMol       = copy.deepcopy(noGold)
    ref_atom    = [ item for item in inMol if item[3] == refIndex ]
    ref_atom    = ref_atom[0]
    #print(f'using reference: {ref_atom}')
    inMol.remove(ref_atom)                 #inplace removal
    ref_atom[4], ref_atom[5], ref_atom[6] = float(ref_atom[4]), float(ref_atom[5]), float(ref_atom[6])
    boxDim = [float(ii) for ii in boxDim]
    #--calculate vector and use PBC--
    for atom in inMol:
        for cart in [4, 5, 6]:
            atom[cart] = float(atom[cart])
            atom[cart] -= ref_atom[cart]
        #--set pbc--
            if abs(atom[cart]) > boxDim[cart - 4]*0.5:
                if atom[cart] > boxDim[cart - 4]*0.5:
                    atom[cart] -= boxDim[cart - 4]
                else:
                    atom[cart] += boxDim[cart - 4]

    #--get a new list with max distance rcut--
    noGoldCut = list()
    for atom in inMol:
        dr2     = atom[4]*atom[4] + atom[5]*atom[5] + atom[6]*atom[6]
        if dr2 < rcut*rcut:
            noGoldCut.append(atom)
    noGoldCut = add_charges(noGoldCut, chargeList)
    #--scoop the vector for CN atom, flip, normalize--
    #--make sure resid, resname same, atomname CN and index 1 less--
    projVec		= [ item for item in noGoldCut if (item[0] == ref_atom[0] and item[1] == ref_atom[1] and item[2] == 'CN' and item[3] == str(int(ref_atom[3]) - 1))]
    projVec		= projVec[0]
    #print(f'projection reference atom: {projVec}')
    #--normalize projVec
    projVec = [projVec[4], projVec[5], projVec[6]]		#take just coordinates
    normVec		= np.sqrt(projVec[0]*projVec[0] + projVec[1]*projVec[1] + projVec[2]*projVec[2])
    projVecNorm	= np.array(projVec)
    projVecNorm	= ( -1.0 / normVec) * projVecNorm
    #--loop over atoms and collect field with conditionals--
    fIntraX,    fIntraY,    fIntraZ     = 0.0, 0.0, 0.0
    fmbnX,      fmbnY,      fmbnZ       = 0.0, 0.0, 0.0
    fLigandX,   fLigandY,   fLigandZ    = 0.0, 0.0, 0.0
    fSolX,      fSolY,      fSolZ       = 0.0, 0.0, 0.0
    fTotalX,    fTotalY,    fTotalZ     = 0.0, 0.0, 0.0
    fProjCN_mbn                         = 0.0
    fProjCN_nombn                       = 0.0
    countIntra, countmbn, countLigand, countSol, countTotal = 0, 0, 0, 0, 0
    #print(f'len inMol : {len(inMol)} \nlen noGoldCut : {len(noGoldCut)} \n')
    #print(f'len inMol[0] : {len(inMol[0])}')
    for atom in noGoldCut:
        #print(atom)
        countTotal += 1
        dr2     = atom[4]*atom[4] + atom[5]*atom[5] + atom[6]*atom[6]
        dr3i    = dr2**(-1.5)
        #--check for intra. Match 0resid and 1resname
        if (atom[0] == ref_atom[0] and atom[1] == ref_atom[1]):
            countIntra += 1
            fIntraX    += atom[7] * dr3i * atom[4]
            fIntraY    += atom[7] * dr3i * atom[5]
            fIntraZ    += atom[7] * dr3i * atom[6]
        #--check for ligand
        elif (atom[1] == 'MBN'):
            countmbn += 1
            fmbnX    += atom[7] * dr3i * atom[4]
            fmbnY    += atom[7] * dr3i * atom[5]
            fmbnZ    += atom[7] * dr3i * atom[6]            
        #--check for cation, assuming we are just using EMIM
        elif (atom[1] == 'THDLK'):
            countLigand += 1
            fLigandX    += atom[7] * dr3i * atom[4]
            fLigandY    += atom[7] * dr3i * atom[5]
            fLigandZ    += atom[7] * dr3i * atom[6]            
        #--check for anion
        elif (atom[1] == 'SOL'):
            countSol += 1
            fSolX    += atom[7] * dr3i * atom[4]
            fSolY    += atom[7] * dr3i * atom[5]
            fSolZ    += atom[7] * dr3i * atom[6]
        #--total field--
        fTotalX    += atom[7] * dr3i * atom[4]
        fTotalY    += atom[7] * dr3i * atom[5]
        fTotalZ    += atom[7] * dr3i * atom[6]
    #print(f'countTotal : {countTotal} \ncountIntra : {countIntra} \ncountmbn : {countmbn} \ncountLigand : {countLigand} \ncountSol : {countSol} \n')
    assert countTotal == (countIntra + countmbn + countLigand + countSol), 'error in decomposition'
    #--collect arrays--
    fIntra      = gro2si * np.array([fIntraX, fIntraY, fIntraZ])
    fmbn        = gro2si * np.array([fmbnX, fmbnY, fmbnZ])
    fLigand     = gro2si * np.array([fLigandX, fLigandY, fLigandZ])
    fSol        = gro2si * np.array([fSolX, fSolY, fSolZ])
    fTotal      = gro2si * np.array([fTotalX, fTotalY, fTotalZ])
    fTotNoIntra_mbn     = fLigand + fSol + fmbn
    fTotNoIntra_nombn   = fLigand + fSol
    fProjCNNoIntra_mbn      = np.dot(fTotNoIntra_mbn, projVecNorm)
    fProjCNNoIntra_nombn    = np.dot(fTotNoIntra_nombn, projVecNorm)
    fProjCN_mbn             = np.dot(fmbn, projVecNorm)
    fProjCN_lig             = np.dot(fLigand, projVecNorm)
    fProjCN_sol             = np.dot(fSol, projVecNorm)    
    return(fProjCNNoIntra_mbn, fProjCNNoIntra_nombn, fProjCN_mbn, fProjCN_lig, fProjCN_sol)

#--get coordinates as gro file--
def gen_trajout(time):
    gmx_trj_cmd = "echo 0 | gmx trjconv -f " + root + "prod2.trr -s " + root + "prod2.tpr"\
                  + " -b " + str(time) + " -e " + str(time) + " -pbc none"\
                  + " -o trajout.gro"
    #center or boxcenter does not make a difference
    #print(f'gmx_trj_cmd = {gmx_trj_cmd}')
    sp.check_call(gmx_trj_cmd, shell=True)
    return

#--FEC study c6-mbn etc, if MBNs are kept as THDLK, change their names
#use increasing number scheme for residues instead of calling them just 181 and 182
def correct_info(molinfo):
    #-- if there is no MBN, rename 182 to MBN
    all_resn = [ii[1] for ii in molinfo]
    if 'MBN' not in all_resn:
        for item in molinfo:
            if (item[0] == '182' and item[1] == 'THDLK'):
                item[1] = 'MBN'
    #-- serialize resid numbers --
    flag = 0
    resnr = 1
    resn_mbn_thdlk = [ii for ii in all_resn if (ii == 'MBN' or ii == 'THDLK')]
    for ii in range(len(resn_mbn_thdlk)):
        if (molinfo[ii][1] == 'MBN' or molinfo[ii][1] == 'THDLK'):
            if flag == 0:
                resnr_trail = molinfo[ii][0]
                molinfo[ii][0] = str(resnr)
                flag = 1
            else:
                resnr_curr = molinfo[ii][0]
                if resnr_curr != resnr_trail:
                    resnr += 1
                    molinfo[ii][0] = str(resnr)
                    resnr_trail = resnr_curr
                else:
                    molinfo[ii][0] = str(resnr)
    return molinfo

tbeg    = time.perf_counter()

simTime        = 0 + 50 * _TNO_   #after first 100ns, take last 100ns
gen_trajout(simTime)

#--process gro file--
tstamp, n_atoms, boxInfo, molinfo = process_gro(wrk + '/trajout.gro')
idx_ref     = get_ref_idx( drf + '/index_nz.ndx')
chargeList  = read_charges( drf + '/charges.dat')
noGold      = strip_gold(molinfo)
noGold      = correct_info(noGold)

#print(chargeList)
#print(idx_ref)
#test = add_charges(noGold, chargeList)
#print(test[0])
'''
#-- output file for checking --
with open("trajout_corr.dat", "w") as fcorr:
    for item in noGold:
        fcorr.write(" ".join(item))
        fcorr.write('\n')
'''
#--make files for field output--
f01     = open("field_inter_mbn.dat", "w")
f02		= open("field_inter_nombn.dat", "w")
f03		= open("field_mbn.dat", "w")
f04		= open("field_lig.dat", "w")
f05		= open("field_sol.dat", "w")
#--read charges from charges

for index in idx_ref:
    fProjCNNoIntra_mbn, fProjCNNoIntra_nombn, fProjCN_mbn, fProjCN_lig, fProjCN_sol = calc_field(index, noGold, boxInfo, chargeList, r_cut)
    f01.write(f'{fProjCNNoIntra_mbn}\n')
    f02.write(f'{fProjCNNoIntra_nombn}\n')
    f03.write(f'{fProjCN_mbn}\n')
    f04.write(f'{fProjCN_lig}\n')
    f05.write(f'{fProjCN_sol}\n')
f01.close()
f02.close()
f03.close()
f04.close()
f05.close()

tend    = time.perf_counter()
print(f'took {tend - tbeg} s for {len(idx_ref)} refs')
#os.remove(wrk + '/trajout.gro')