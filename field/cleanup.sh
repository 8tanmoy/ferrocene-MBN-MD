#!/bin/bash
rm field_projection_cn_mbn.dat field_projection_cn_nombn.dat
rm parts.tar.gz
f1=field_inter_mbn.dat
f2=field_inter_nombn.dat
f3=field_mbn.dat
f4=field_lig.dat
f5=field_sol.dat
cat part_*/$f1 >> $f1
cat part_*/$f2 >> $f2
cat part_*/$f3 >> $f3
cat part_*/$f4 >> $f4
cat part_*/$f5 >> $f5
mkdir parts
mv part_* parts/
tar -zcvf  parts.tar.gz ./parts/
rm -rf parts/

