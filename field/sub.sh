#!/bin/bash -l 
#$ -l h_rt=4:00:00
#$ -j y
#$ -N field
#$ -pe omp 1

module load intel/2019 openmpi/3.1.4_intel-2019 gcc/5.5.0 cuda/10.0 && export PATH=/projectnb/cui-buchem/tanmoy/projects/RL/md_tools-master/install/bin:$PATH && export PLUMED_USE_LEPTON=yes

source /projectnb/cui-buchem/tanmoy/projects/RL/gromacs-2018.3/install/bin/GMXRC

module load python3

f1=field_inter_mbn.dat
f2=field_inter_nombn.dat
f3=field_mbn.dat
f4=field_lig.dat
f5=field_sol.dat
touch $f1
touch $f2
touch $f3
touch $f4
touch $f5
for((ii=0;ii<40;ii++))
do
    mkdir t_${ii}
    cd t_${ii}
    jj=$(( _PARTNO_ * 40 + ii ))
    sed "s/_TNO_/${jj}/g" ../../field_space_projection.py > field_space_projection.py
    python3 field_space_projection.py &> field_space_projection.out
    cat $f1 >> ../$f1
    cat $f2 >> ../$f2
    cat $f3 >> ../$f3
    cat $f4 >> ../$f4
    cat $f5 >> ../$f5
    cd ../
done
sleep 2 
rm -rf t_*

