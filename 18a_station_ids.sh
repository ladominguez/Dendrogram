#!/bin/sh


ROOT='/mnt/data01/antonio/Dropbox/BSL/CRSMEX/Dendrograms/2020AGO07/sequence_xc9500_coh9500'
cd $ROOT

for k in $(ls -d sequence_*/SEQ*); do
	cd $k
	if [ -f "station_ids.info" ]; then
		rm station_ids.info
	fi
	ls *.sac | awk -F. '{print $2}' | uniq > station_ids.info
	cd $ROOT
done
