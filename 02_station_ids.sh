#!/bin/sh


ROOT='/mnt/data01/antonio/Dropbox/BSL/CRSMEX/Dendrograms/2020MAR27/sequence_xc9500_coh9500'
cd $ROOT

for k in $(ls -d sequence_*/); do
	cd $k
	if [ -f "station_ids.info" ]; then
		rm station_ids.info
	fi
	#ls *.sac | grep -v SYN | awk -F. '{print $1}' | uniq  > station_ids.info
        saclst kstnm f *.sac | awk '{print $2}' | sort | uniq > station_ids.info	
	cd ..
done
