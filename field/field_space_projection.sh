#!/bin/bash
for((ii=0;ii<100;ii++))	#1000
do
	mkdir part_$ii
	sed "s/_PARTNO_/${ii}/g" sub.sh > part_$ii/sub.sh
	cd part_$ii
	qsub sub.sh
	cd ../
done
