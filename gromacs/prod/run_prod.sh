#run eq
cxx=c11
src_eq=/projectnb/cui-buchem/tanmoy/projects/FERRO/${cxx}-mbn/eq/
cp $src_eq/topol.top      ./
cp $src_eq/eq_npt.gro     ./
cp $src_eq/posre_au.itp   ./
cp $src_eq/disre_fec.itp  ./
cp $src_eq/angre_cp.itp   ./
cp -r $src_eq/toppar/     ./
cp $src_eq/index.ndx      ./
gmx grompp -f prod.mdp -n index.ndx -p topol.top -c eq_npt.gro -r eq_npt.gro -o prod.tpr -maxwarn 10
