#run eq
cxx=c11
time=50000
src_eq=/projectnb/cui-buchem/tanmoy/projects/FERRO/${cxx}-mbn/eq/
cp $src_eq/topol.top      ./
cp $src_eq/posre_au.itp   ./
cp $src_eq/disre_fec.itp  ./
cp $src_eq/angre_cp.itp   ./
cp -r $src_eq/toppar/     ./
#-- take snapshot at 100ns from prod --
#echo "0" | gmx trjconv -f ../prod/prod.xtc -s ../prod/prod.tpr -b $time -e $time -dump $time -o prod.gro
gmx solvate -cp prod.gro -cs spc216.gro -p topol.top -o prod_sol.gro
rm \#topol.top.*
echo "q" | gmx make_ndx -f prod_sol.gro -o index.ndx
rm \#index.ndx.*
gmx grompp -f prod2.mdp -n index.ndx -p topol.top -c prod_sol.gro -r prod_sol.gro -o prod2.tpr -maxwarn 10
