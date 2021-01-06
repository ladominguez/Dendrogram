#!/bin/bash

ROOT='/mnt/data01/antonio/Dropbox/BSL/CRSMEX/Dendrograms/2020AGO07/sequence_xc9500_coh9500'

cd $ROOT
pwd
for k in $(ls -d sequence_*/SEQ*); do
	cd $k
	pwd
 	if [ -f "merge.correli.dat" ]; then
		rm merge.correli.dat
	fi 
	cat *.correli.dat | awk -F. '{print$2}' | sed 's/-/ /g' > index.tmp
	cat *.correli.dat | awk -F. '{print$3}'                 > id.tmp
	cat *.correli.dat | awk '{print $3,$4}'                 > dist_mean.tmp

	paste index.tmp dist_mean.tmp id.tmp > merge.correli.dat
	rm *.tmp
	cd ../../
done
