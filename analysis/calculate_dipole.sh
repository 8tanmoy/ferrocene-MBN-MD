wrk=../prod2
f_en=${wrk}/prod2.edr
f_trj=${wrk}/prod2.trr
f_tpr=${wrk}/prod2.tpr
f_ndx=${wrk}/index.ndx
#---
gmx h2order -f $f_trj -n $f_ndx -s $f_tpr -b 0 -e 200000 -d Z -sl 4000
