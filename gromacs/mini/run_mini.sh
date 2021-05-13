cxx=c11
xdim=4.87
ydim=$xdim
zdim=`echo "5 * $xdim" | bc -l`
echo "${xdim} x ${ydim} x ${zdim}"
gmx editconf -f t6_${cxx}_double.pdb -box $xdim $ydim $zdim -c yes -o ${cxx}_box.gro
rm \#${cxx}_box.gro*

#-- generate index files
echo "q" | gmx make_ndx -f ${cxx}_box.gro -o index.ndx
gmx select -f ${cxx}_box.gro -s ${cxx}_box.gro -select "name AUS AU" -on index_au.ndx
gmx select -f ${cxx}_box.gro -s ${cxx}_box.gro -select "resid 181 and name C1 C2 C3 C4 C5" -on index_r1.ndx
gmx select -f ${cxx}_box.gro -s ${cxx}_box.gro -select "resid 181 and name C6 C7 C8 C9 C10" -on index_r2.ndx
gmx select -f ${cxx}_box.gro -s ${cxx}_box.gro -select "resid 181 and name FE" -on index_fe.ndx
rm \#index*
cat index_au.ndx >> index.ndx
cat index_r1.ndx >> index.ndx
cat index_r2.ndx >> index.ndx
cat index_fe.ndx >> index.ndx
#rm index_*.ndx
cp topol_charmm.top topol.top
gmx solvate -cp ${cxx}_box.gro -cs spc216.gro -p topol.top -o ${cxx}_sol.gro
rm \#${cxx}_sol.gro.*
rm \#topol.top.*
echo "q" | gmx make_ndx -f ${cxx}_sol.gro -o index.ndx
rm \#index.ndx*
gmx grompp -f mini.mdp -n index.ndx -p topol.top -c ${cxx}_sol.gro -o mini.tpr -maxwarn 10
rm \#mini.tpr*
