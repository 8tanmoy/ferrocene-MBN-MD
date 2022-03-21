
#-- code for solvatochromatic frequency shift OF p-tolunitrile J. Chem. Phys. 137, 114307 (2012) --
#-- tanmoy 07/23/2021 --

"""
tasks
--------
for each time:
    1. calculate solvatochromatic frequency shift
    3. make sure the layer on the opposite side is not taken into account

caution
--------
1. this model is developed for p-tolunitrile 
2. needs further validation

functions
--------
    o process_gro
    o read_charges
    o strip_gold
    o add_charges
    o normalize
    o gen_trajout
    o serialize
    o calc_com
   *o calc_field_freq
    o __main__
"""
import shutil
from pathlib import Path
import matplotlib.pyplot as plt
import os
import sys
import subprocess as sp
import numpy as np
import copy
import time
np.set_printoptions(threshold=sys.maxsize)

#-- constants --
gro2si = 1.602176 * 9.0             #multiplicative factor from gromacs to MV/cm 
print(f"gro2si = {gro2si}")
r_cut   =   3.5

#-- out : 1> timestamp 2> boxinfo 3> n_atoms (debug) 4> coordonate array
def process_gro(coord_path): #-> (tstamp, nat, boxinfo, molinfo)
    print(f'processing coordinate file {coord_path}...')
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

def read_charges(ch_path): #-> arr
    print(f'reading charges from {ch_path}...')
    f1 = open(ch_path, "r")
    arr = list()
    for line in f1:
        arr.append(line.split())
    # --resname--atomanme--charge--
    f1.close()
    return(arr)

def strip_gold(withGold): #-> noGold
    print(f'stripping gold...')
    noGold = list()
    for item in withGold:
        #--item[2] is atomname--
        if item[2][:2] != 'AU':
            noGold.append(item)
    return(noGold)

def add_charges(noCharge, chargeList): #-> noCharge + atomcharge
    print(f'adding charges...')
    for item in noCharge:
        selectAtom = [ float(ii[2]) for ii in chargeList if (ii[0] == item[1] and ii[1] == item[2]) ]
        item.append(selectAtom[0])  #because using list comprehension
    return(noCharge)

def normalize(vec): #-> norm
    norm    = np.sqrt(vec[0] * vec[0] + vec[1] * vec[1] + vec[2] * vec[2])
    normi   = norm ** (-1)
    vecnorm = normi * vec
    return vecnorm

def gen_trajout(time, root): #-> gmx_trj_cmd call
    print(f'generating trajectory output at {root} for t={time}')
    gmx_trj_cmd = "echo 0 | gmx_mpi trjconv -f " + root + "prod/prod.trr -s " + root + "prod/prod.tpr"\
                  + " -b " + str(time) + " -e " + str(time) + " -pbc nojump"\
                  + " -o trajout.gro"
    #center or boxcenter does not make a difference
    #print(f'gmx_trj_cmd = {gmx_trj_cmd}')
    sp.check_call(gmx_trj_cmd, shell=True)
    return

def serialize(molinfo, resname): #-> remove duplicates of resid for particular resname
    print(f'serializing MBN resids...')
    resnrs  = []
    ii      = 0
    while ii < len(molinfo):
        if molinfo[ii][1] == 'MBN':
            if molinfo[ii][0] not in resnrs:
                temp = molinfo[ii][0]
                resnrs.append(temp)
            else:
                temp = str(int(temp) + 1)
                for jj in range(13):
                    molinfo[ii + jj][0] = temp
                resnrs.append(temp)
            ii += 13
        else:
            ii += 1
    #print(resnrs)
    return molinfo

def calc_com(pos_vec, mass_vec):
    print(f'calculating center of mass...')
    mass_vec    = mass_vec.reshape(len(mass_vec),1)
    mom_vec     = pos_vec * mass_vec
    sum_mom     = np.sum(mom_vec, axis=0)
    com         = sum_mom / np.sum(mass_vec.flatten())
    return com

def calc_field_freq(resid_mbn, noGold, boxDim, chargeList, rcut):
    print(f'calculating electric field and frequency for resid =\t{resid_mbn}')
    #-- make a copy of the molinfo array --
    inMol       = copy.deepcopy(noGold)

    #-- position of CoM --
    mass_ref = {'S1'  : 32.0600,
                'C1'  : 12.0110,
                'CD1' : 12.0110,
                'HD1' : 1.00800,
                'CD2' : 12.0110,
                'HD2' : 1.00800,
                'CE1' : 12.0110,
                'HE1' : 1.00800,
                'CE2' : 12.0110,
                'HE2' : 1.00800,
                'CZ'  : 12.0110,
                'CN'  : 12.0110,
                'NZ'  : 14.0070 }

    pos_mbn     = []
    mass_mbn    = []
    for item in inMol:
        if  (item[0] == resid_mbn and item[1] == 'MBN'):
            pos_mbn.append([float(item[4]), float(item[5]), float(item[6])])
            mass_mbn.append(mass_ref[item[2]])
    pos_mbn     = np.array(pos_mbn)
    mass_mbn    = np.array(mass_mbn)
    com_mbn     = calc_com(pos_mbn, mass_mbn)

    print(f'Center of Mass of MBN #{resid_mbn} is at {com_mbn}')

    boxDim = [float(ii) for ii in boxDim]
    #-- calculate vector and use PBC wrt center of mass --
    for atom in inMol:
        for cart in [4, 5, 6]:
            atom[cart] = float(atom[cart])
            atom[cart] -= com_mbn[cart - 4]
        #--set pbc--
            if abs(atom[cart]) > boxDim[cart - 4]*0.5:
                if atom[cart] > boxDim[cart - 4]*0.5:
                    atom[cart] -= boxDim[cart - 4]
                else:
                    atom[cart] += boxDim[cart - 4]
    
    #-- get a new list of distances with cutoff rcut --
    noGoldCut   = []
    for atom in inMol:
        dr2     = atom[4]*atom[4] + atom[5]*atom[5] + atom[6]*atom[6]
        if dr2 < rcut*rcut:
            noGoldCut.append(atom)
    noGoldCut = add_charges(noGoldCut, chargeList)
    print(f'number of atoms within rcut = {rcut} is {len(noGoldCut)}')

    #-- get direction cosines --
    mol_nz      = [item for item in noGoldCut if (item[0] == resid_mbn and item[1] == 'MBN' and item[2] == 'NZ')]
    mol_cn      = [item for item in noGoldCut if (item[0] == resid_mbn and item[1] == 'MBN' and item[2] == 'CN')]
    mol_ce1     = [item for item in noGoldCut if (item[0] == resid_mbn and item[1] == 'MBN' and item[2] == 'CE1')]
    mol_ce2     = [item for item in noGoldCut if (item[0] == resid_mbn and item[1] == 'MBN' and item[2] == 'CE2')]

    assert len(mol_nz) == len(mol_cn) == 1, 'need unique NZ and CN'
    assert len(mol_ce1) == len(mol_ce2) == 1, 'need unique CE1 and CE2'

    mol_nz      = mol_nz[0]
    mol_cn      = mol_cn[0]
    mol_ce1     = mol_ce1[0]
    mol_ce2     = mol_ce2[0]

    ez          = np.array([mol_nz[4], mol_nz[5], mol_nz[6]]) - np.array([mol_cn[4], mol_cn[5], mol_cn[6]])
    ce12        = np.array([mol_ce2[4], mol_ce2[5], mol_ce2[6]]) - np.array([mol_ce1[4], mol_ce1[5], mol_ce1[6]])
    ez          = normalize(ez)
    ce12        = normalize(ce12)
    ex          = np.cross(ez, np.cross(ce12, ez))
    ey          = np.cross(ez, ex)
    ex          = normalize(ex)
    ey          = normalize(ey)
 
    print(f'molecule fixed unit vectors are: \nex\t\t{ex}\ney\t\t{ey}\nez\t\t{ez}')
    assert round(ex.dot(ey),4) == round(ey.dot(ez),4) == round(ez.dot(ex),4) == 0.0, "new unit vectors are not orthogonal"
    assert round(ex.dot(ex),4) == round(ey.dot(ey),4) == round(ez.dot(ez),4) == 1.0, "unit vectors not normalized"
    dircos      = np.array([ex, ey, ez])  #because x, y, z is simple cartesian
    print(f'direction cosine\'s (transpose - inverse) should be 0:\n {np.transpose(dircos) - np.linalg.inv(dircos)}')
    print(f'direction cosine matrix:\n{dircos}')

    #-- loop over atoms and collect field with conditionals --
    dNuInter        = 0.0 
    dNuMu           = 0.0
    dNuTheta        = 0.0
    dNuOmega        = 0.0
    E0      = np.zeros((3))
    dE0     = np.zeros((3,3))
    ddE0    = np.zeros((3,3,3))
    countInter, countMBN, countLig, countSol, countTotal = 0, 0, 0, 0, 0

    for atom in noGoldCut:
        if not (atom[1] == 'MBN' and atom[0] == resid_mbn):
            countInter += 1            
            dr2     = atom[4]*atom[4] + atom[5]*atom[5] + atom[6]*atom[6]
            dr1i    = np.sqrt((dr2)**(-1)) 
            dr2i    = dr2**(-1)
            dr3i    = dr2**(-1.5)
            dr4i    = (dr2i)**2
            r_hat_c = dr1i * np.array([atom[4], atom[5], atom[6]])  #r_hat cartesian
            r_hat   = dircos.dot(r_hat_c)                           #r_hat in molecule coordinates
            #-- field for dipole --
            E0      += atom[7] * dr2i * r_hat

            #-- grad field for quadrupole --
            r2_hat = np.zeros((3,3))
            for ii in range(3):
                for jj in range(3):
                    if ii == jj:
                        r2_hat[ii][jj] = 3 * (r_hat[ii] * r_hat[jj]) - 1.0
                    else:
                        r2_hat[ii][jj] = 3 * (r_hat[ii] * r_hat[jj])
            dE0     += atom[7] * dr3i * r2_hat

            #-- grad grad field for octupole --
            r3_hat  = np.zeros((3,3,3))
            for ii in range(3):
                for jj in range(3):
                    for kk in range(3):
                        r3_hat[ii][jj][kk] = 5 * r_hat[ii] * r_hat[jj] * r_hat[kk]
                        if kk == jj:
                            r3_hat[ii][jj][kk] -= r_hat[ii]
                        if kk == ii:
                            r3_hat[ii][jj][kk] -= r_hat[jj]
                        if ii == jj:
                            r3_hat[ii][jj][kk] -= r_hat[kk]
            ddE0    += atom[7] * dr4i * r3_hat

    #-- use prefactor and change units --
    E0          = -1.0 * gro2si * E0
    dE0         = -1.0 * gro2si * 0.1 * dE0         #dTheta is 1E-8, (nm-1 = 1E7 cm-1)
    ddE0        = -3.0 * gro2si * 0.01 * ddE0       #dOmega is 1E-16, (nm-2 = 1E14 cm-2)
    
    #-- collect final frequency shift --
    dNuMu       = -1.0 * np.dot(dMu, E0)
    dNuTheta    = -(1.0/6.0) * np.tensordot(dTheta, dE0)
    dNuOmega    = -(1.0/30.0) * np.sum([np.tensordot(dOmega[ii], ddE0[ii]) for ii in range(3)])
    dNuInter    = dNuMu + dNuTheta + dNuOmega
    return(dNuInter, dNuMu, dNuTheta, dNuOmega)

if __name__ == '__main__':
    root        = '/projectnb/cui-buchem/tanmoy/projects/' + 'FERRO_RAND/c11-mbn/'
    drf         = root + 'field_time_cho'
    wrk         = os.getcwd()
    tbeg        = time.perf_counter()
    simTime     = 0 + 20 * _TNO_   #after first 100ns, take last 100ns
    gen_trajout(simTime, root)
    
    #-- process gro file --
    tstamp, n_atoms, boxInfo, molinfo = process_gro(wrk + '/trajout.gro')
    chargeList  = read_charges( drf + '/charges.dat')
    noGold      = strip_gold(molinfo)
    noGoldSerialmbn = serialize(noGold, 'MBN')

    #-- find unique MBN residues --
    mbn_resid = []
    for atom in noGold:
        if atom[1] == 'MBN':
            mbn_resid.append(atom[0])
    mbn_resid_unique    = [ii for ii in set(mbn_resid)]
    mbn_resid_unique.sort()

    #-- define dipole, quadrupole and octupole moments for p-tolunitrile --
    #-- 1 cm^(-1)/(MV/cm) = 10 cm^(-1)/(V/nm) --
    dMu         = np.array([0.0, 0.0, -0.46])
    dTheta      = np.array([[-1.54, 0.0, 0.0],
                            [0.0, -1.61, 0.0],
                            [0.0, 0.0, 3.15]])
    dOmegaX     = [[0.0, 0.0, 0.23],    [0.0, 0.0, 0.0],    [0.0, 0.0, 0.0]]
    dOmegaY     = [[0.0, 0.0, 0.0],     [0.0, 0.0, 1.38],   [0.0, 0.0, 0.0]]
    dOmegaZ     = [[0.0, 0.0, 0.0],     [0.0, 0.0, 0.0],    [0.0, 0.0, -1.61]]
    dOmega      = np.array([dOmegaX,
                            dOmegaY,
                            dOmegaZ])
    print(f'shape of dMu\t\t= {dMu.shape}')
    print(f'shape of dTheta\t\t= {dTheta.shape}')
    print(f'shape of dOmega\t\t= {dOmega.shape}')

    #calc_field_freq(mbn_resid_unique[0], noGold, boxInfo, chargeList, r_cut)
    
    #-- grab output and put in files --
    f01     = open("nu_inter.dat",  "w")
    f02     = open("nu_dp.dat",     "w")
    f03     = open("nu_qp.dat",     "w")
    f04     = open("nu_op.dat",     "w")

    #-- for each unique MBN, calculate field --
    for imbn in mbn_resid_unique:
        dNuInter, dNuMu, dNuTheta, dNuOmega = calc_field_freq(imbn, noGoldSerialmbn, boxInfo, chargeList, r_cut)
        f01.write(f'{dNuInter}\n')
        f02.write(f'{dNuMu}\n')
        f03.write(f'{dNuTheta}\n')
        f04.write(f'{dNuOmega}\n')

    f01.close()
    f02.close()
    f03.close()
    f04.close()

    tend = time.perf_counter()
    print(f'took {tend - tbeg} s for {len(mbn_resid_unique)} refs')
