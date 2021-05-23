#!/bin/bash
#-- NZ-OW --
gmx rdf -f ../prod2/prod2.trr -s ../prod2/prod2.tpr -b 100000 -e 200000 -dt 1 -pbc yes -selrpos atom -seltype atom -bin 0.005 -ref "atomname NZ" -sel "atomname OW" -norm rdf -rmax 2.0 -o rdf_NZ_OW.xvg -cn rdf_cn_NZ_OW.xvg
#-- FE-OW --
gmx rdf -f ../prod2/prod2.trr -s ../prod2/prod2.tpr -b 100000 -e 200000 -dt 1 -pbc yes -selrpos atom -seltype atom -bin 0.005 -ref "atomname FE" -sel "atomname OW" -norm rdf -rmax 2.0 -o rdf_FE_OW.xvg -cn rdf_cn_FE_OW.xvg
#-- NZ-FE --
gmx rdf -f ../prod2/prod2.trr -s ../prod2/prod2.tpr -b 100000 -e 200000 -dt 1 -pbc yes -selrpos atom -seltype atom -bin 0.005 -ref "atomname NZ" -sel "atomname FE" -norm rdf -rmax 2.0 -o rdf_NZ_FE.xvg -cn rdf_cn_NZ_FE.xvg
