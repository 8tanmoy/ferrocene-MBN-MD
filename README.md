# ferrocene-MBN-MD
electric field calculation of MBN and alkyl-ferrocene functionalized Au surface

----  
  - [X] get 1 nm x 1 nm x 2 nm surface with -S-CH2-CH3 on positions 1,5 of AU100 22% occupancy | charmm-gui jobid 1939395487
  - [X] get a copy of `step3_pbcsetup.crd/psf/pdb`  
  - [X] delete unnecessary toppar load from `toppar.str`  
  - [X] (like nitrile IL) add another pres for MBN at the end of `toppar_all36_nanolig_patch.str` in `charmm-gui-xxxx/toppar/`  
```
!tanmmoy 05/02/2020
PRES L00250 -0.000 ! linkage between THSLK and MBN
dele atom H11
dele atom H12
dele atom C2
dele atom H21
dele atom H22
dele atom H23

ATOM    S1         SG311   -0.075
ATOM    C1        CG2R61    0.085 !change to CG CG2R61
ATOM    CD1       CG2R61   -0.125
ATOM    HD1        HGR61    0.115
ATOM    CD2       CG2R61   -0.125
ATOM    HD2        HGR61    0.115
ATOM    CE1       CG2R61   -0.104
ATOM    HE1        HGR61    0.115
ATOM    CE2       CG2R61   -0.104
ATOM    HE2        HGR61    0.115
ATOM    CZ        CG2R61    0.095
ATOM    CN         CG1N1    0.356
ATOM    NZ         NG1T1   -0.463

BOND    S1  C1
BOND    C1  CD1 C1 CD2
BOND    CD1 HD1 CD1 CE1
BOND    CD2 HD2 CD2 CE2
BOND    CE1 HE1 CE2 HE2
BOND    CZ  CE1 CZ CE2 CZ CN
BOND    CN   NZ
```  
  - [X] error might be generated like: `<CODES>: No angle parameters for    17 ( IAU      SG311    CG2R61  )`  
  - [ ] run `setup/patch_mbn.inp` -> step
