#run eq
cxx=c11
src_mini=/projectnb/cui-buchem/tanmoy/projects/FERRO/${cxx}-mbn/mini/
cp $src_mini/topol.top      ./
cp $src_mini/${cxx}_sol.gro ./
cp $src_mini/posre_au.itp   ./
cp $src_mini/disre_fec.itp  ./
cp $src_mini/angre_cp.itp  ./
cp -r $src_mini/toppar/     ./
cp $src_mini/index.ndx      ./
echo "uncomment posre_au and disre_fec? y/n"
read prompt
if [[ $prompt == 'y' ]]; then
    gmx grompp -f eq_npt.mdp -n index.ndx -p topol.top -c ${cxx}_sol.gro -r ${cxx}_sol.gro -o eq_npt.tpr -maxwarn 10
else
    echo "grompp :("
fi
