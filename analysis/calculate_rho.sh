#!/bin/bash
gmx make_ndx -f ../prod2/prod_sol.gro -o index.ndx
gmx density -f ../prod2/prod2.trr -s ../prod2/prod2.tpr -n index.ndx -d Z -sl 4000 -dens number -ng 4 -center yes -symm yes -relative yes -o rho_n.xvg
gmx density -f ../prod2/prod2.trr -s ../prod2/prod2.tpr -n index.ndx -d Z -sl 4000 -dens charge -ng 4 -center yes -symm yes -relative yes -o rho_c.xvg