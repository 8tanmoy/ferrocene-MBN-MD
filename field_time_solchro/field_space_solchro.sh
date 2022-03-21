#!/bin/bash
for((ii=0;ii<200;ii++))
do
	mkdir part_$ii
	sed "s/_PARTNO_/${ii}/g" sub.sh > part_$ii/sub.sh
	cd part_$ii
	qsub sub.sh
	cd ../
done
