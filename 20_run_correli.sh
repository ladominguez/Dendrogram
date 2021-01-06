#!/bin/bash

#  Morelia, Michoacan. 2019/08/28
# This code converts all table file in each sequence_###_### subdirectory into sac files.
#
# ladominguez@seismo.berkeley.edu


ROOT='/mnt/data01/antonio/Dropbox/BSL/CRSMEX/Dendrograms/2020AGO07/sequence_xc9500_coh9500'
CORRELI='/mnt/data01/antonio/Dropbox/CRSMEX/code_arturo/correli'

cd $ROOT

for k in $(ls -d sequence_*/SEQ*); do
	echo $k
	cd $k
	rm CORR.*.dat
	echo "Working on directory " $k  "..."
	ls input*.in > in_files.tmp
	awk -v var="$CORRELI" '{print var " < " $1 }' in_files.tmp > exec_sh.tmp
	sh  -v exec_sh.tmp
	rm *.tmp
	cd $ROOT
done
echo "FINISHED."
