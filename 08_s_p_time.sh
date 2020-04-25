#!/bin/bash

ROOT='/mnt/data01/antonio/Dropbox/BSL/CRSMEX/Dendrograms/2020MAR27/sequence_xc9500_coh9500'

cd $ROOT
FILE=s_p_time.dat

find . -name s_p_time.dat | xargs rm

for k in $(ls -d sequence_*/); do
	cd $k
	for file in $(ls *sac |grep -v SYN );do
		p_time=$(echo $file | awk '{print "saclst t0 f " $1 }' | sh | awk '{print $2}')
		if [ "$p_time" == "-12345" ]; then
                        echo $file | awk '{print "taup_setsac -ph p-0 -evdpkm " $1}' | sh
                fi		

		p_time=$(echo $file | awk '{print "saclst t0 f " $1 }' | sh | awk '{print $2}')
		if [ "$p_time" == "-12345" ]; then
                        echo $file | awk '{print "taup_setsac -ph P-0 -evdpkm " $1}' | sh
                fi		
	
                echo $file | awk '{print "taup_setsac -ph s-7 -evdpkm " $1}' | sh
		s_time=$(echo $file | awk '{print "saclst t7 f " $1 }' | sh | awk '{print $2}')
		if [ "$s_time" == "-12345" ]; then
			echo $file | awk '{print "taup_setsac -ph S-7 -evdpkm " $1}' | sh
		fi 
	done
	
	if [ -f "$FILE" ]; then
		echo "Removing previous file. " $FILE
		rm $FILE
	fi

	touch $FILE

	for station in $(cat station_ids.info); do
		test_sta=$(ls $station*.sac | head -1) # Choose only one station
		echo $test_sta | awk '{print "saclst t0 t7 f " $1}' | sh | awk -v sta="$station" '{print sta " " $3-$2}' >> $FILE
		
	done
	echo $FILE  " written."
	cd ..
	echo "Leaving directory " $k
done

echo "Checking for errors."
find . -name "*.sac" | grep -v SYN | awk '{print "saclst t0 t7 f " $1}' | sh > time.log
grep 12345 time.log

