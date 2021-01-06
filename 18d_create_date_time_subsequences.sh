#!/bin/sh


ROOT='/mnt/data01/antonio/Dropbox/BSL/CRSMEX/Dendrograms/2020AGO07/sequence_xc9500_coh9500'
CAT='/mnt/data01/antonio/Dropbox/CRSMEX/Catalogs/CATALOG_2001_2020.DAT'
cd $ROOT

for k in $(ls -d sequence_*/SEQ*); do
	cd $k
	echo "Working on file " $k " ..."
	if [ -f "date_time.dat" ]; then
		rm date_time.dat
	fi
	touch date_time.dat
	
	for id_seq in $(cat unique_member_id.info); do
		grep $id_seq $CAT | awk '{print $1, $2}' | sed 's/\//-/g' >> date_time.dat

	done
		
	cd $ROOT
done

echo "FINISHED"
