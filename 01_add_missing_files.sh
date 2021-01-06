#!/bin/bash

# This scrips adds missing files in the sequence to compute the dendrograms. Missing files
# occur when a coh and cc of a sequence lies beneath the threshold.

# Luis. A. Dominguez Mexico City, 2019

ROOT='/mnt/data01/antonio/Dropbox/BSL/CRSMEX/Dendrograms/2020AGO07/sequence_xc9500_coh9500'
DATA='/mnt/data01/antonio/Dropbox/BSL/CRSMEX/data'

INPUT1=unique_member_id.info
INPUT2=station_ids.info

OUTPUT1=$ROOT/missing_list.sh


cd $ROOT

if [ -f $OUTPUT1 ]; then
	rm $OUTPUT1
fi

touch $OUTPUT1

for k in $(ls -d sequence_*/); do
cd $k
echo "Working on file " $k " ..."
	while read line1; do 
		while read line2; do
                        miss=$(echo $line2 $line1 | awk -v id=$line1 -v sta=$line2 '{print "find . -name \"" sta "*BH*" id "*.sac\""}' | sh | wc -l)
			#miss=$(echo $line2 $line1 | awk -v id=$line1 -v sta=$line2 '{print "ls " sta "*BH*" id "*.sac"}' | sh | wc -l)
			if [ "$miss" == 0 ];then
				missed_file=$(echo $line2 $line1 | awk -v data=$DATA -v id=$line1 -v sta=$line2 '{print "find " data " -name \"" sta "*BHZ*" id "*.sac\""}' | sh | tail -1)
				if [ ! -z "$missed_file" ]; then
					echo $(pwd) $missed_file | awk '{print "cp " $2 " " $1}'				
				fi

			fi
		done < $INPUT2 >> $OUTPUT1
	done < $INPUT1
	cd ..
	
done

echo "Run the file " $OUTPUT1

