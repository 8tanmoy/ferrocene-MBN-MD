# ferrocene-MBN-MD
electric field calculation of MBN and alkyl-ferrocene functionalized Au surface

----  
  - [X] Get 1 nm x 1 nm x 2 nm surface with -S-CH2-CH3 on positions 1,5 of AU100 22% occupancy | charmm-gui jobid 1939395487
  - [X] Get a copy of `step3_pbcsetup.crd/psf/pdb`  
  - [X] Delete unnecessary toppar load from [`toppar.str`](/setup/toppar.str)  
  - [X] Add MBN patch `L00250` in [`toppar_all36_nanolig_patch.str`](/setup/toppar/toppar_all36_nanolig_patch.str)  
  - [X] error might be generated like: `<CODES>: No angle parameters for    17 ( IAU      SG311    CG2R61  )`. For this [`par_interface.prm`](/setup/toppar/par_interface.prm) needs to be modified. in `ANGLES`  
```
IAU  SG311     CG2R61   35.0000   105.0   ! 10.1007/s10853-012-6356-8
AUS  SG311     CG2R61   35.0000   105.0   ! 10.1007/s10853-012-6356-8
```  
and in `DIHEDRALS`  
```
IAU       SG311    CG2R61   CG2R61 0.0000 2 0.00
AUS       SG311    CG2R61   CG2R61 0.0000 2 0.00
```
  - [X] [`t1_patch_mbn.inp`](/setup/t1_patch_mbn.inp) : -> `t2_mbnpatch.{psf,crd,pdb}`  
  - [X] [`gaussian`](/setup/gaussian) For detailed reference equilibrium structural information (bondlength/angles/IC), optimize ferrocene RB3LYP/Aug-CC-pVDZ charge 0 spin singlet  
    staggered (Energy: -1650.91044652 A.U., DM: 0.0006) and eclipsed (Energy: -1650.91158318 A.U., DM: 0.000755)  
    WARNING: partial charges for Fe turns out to be negative.  
  - [X] [`toppar_fec.str`](/setup/toppar/toppar_fec.str) : Use FEC parameters instead from SI of [Hatten et. al.](https://chemistry-europe.onlinelibrary.wiley.com/doi/abs/10.1002/chem.200700358)
  - [X] make two patch residues : -C6-FEC, -C11-FEC
    - [X] make alkane patches -C6 and -C11 with missing last hydrogen. New atom names in patch residues must not be the same as deleted ones. Patches added as `PHEX` (patch hexane) and `PUND` (patch undecane) in [`toppar_all36_nanolig_patch.str`](/setup/toppar/toppar_all36_nanolig_patch.str)    
    - [X] make patch for ferrocene and patch it on the alkanes. Patch for ferronece is `FEC` in [`toppar_all36_nanolig_patch.str`](/setup/toppar/toppar_all36_nanolig_patch.str)  
    - [X] [`t2-c6_patch.inp`](/setup/t2-c6_patch.inp) : patch -C6HX  
          [`t3.1-c6_patch_fec.inp`](/setup/t3.1-c6_patch_fec.inp) : patch one ferrocene ring.
          [`t3.2-c6_patch_fec.inp`](/setup/t3.2-c6_patch_fec.inp) : patch the rest of the ferrocene ring.
          [`t2-c11_patch.inp](/setup/t2-c11_patch.inp) : patch -C11HX  

  - [X] make necessary orientations, rotations, and translations to make 4x4x4 Au slab with ligands on both sides of density 2 nm^-2.  
  - [X] make gromacs `.itp` and `.top` files. [CHARMM-GUI FF Cconverter](https://charmm-gui.org/?doc=input/converter.ffconverter) is giving `/` error. Use old [`psf2itp.py`](/setup/tools/psf2itp.py).
  - [X]


