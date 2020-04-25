#!/bin/bash


cat=$(grep  catalog params.yaml | awk '{print $2}')
obs=$(grep  obs     params.yaml | awk '{print $2}')
root=$(grep root    params.yaml | awk '{print $2}')
input='obs_recorded.dat'
outfile='get_obs_recording.sh'

if [ -f "$outfile" ]; then
	echo "Removing previous output ..."
	rm $outfile
fi

touch $outfile

echo "Processing ..."
while read line; do
	ids=$(echo $line | awk -F: '{print $5}')
	seq=$(echo $line | awk -F: '{print $6}')
	echo "Searchin" $seq "..."
	IFS=' '
	read -ra idenyfier <<< "$ids"
	for id in "${idenyfier[@]}"; do
		
		nsac=$(grep $id $cat | cut -c 3-10 | sed 's/\///g' | awk -v var="$obs" -v eq_id="$id" '{print "ls " var "/" $1 "/*" eq_id "*.sac"}' | sh 2> /dev/null | wc -l)
		#grep $id $cat | cut -c 3-10 | sed 's/\///g' | awk -v var="$obs" -v eq_id="$id" '{print "ls " var "/" $1 "/*" eq_id "*.sac"}'
		if [ $nsac -gt 0 ]; then
			path=$root/OBS/$id
			if [ ! -d "$path" ]; then
				echo "mkdir -p " $path >> $outfile
				echo "cp " $obs/$(grep $id $cat | cut -c 3-10 | sed 's/\///g')/"*"$id"*.sac " $path >> $outfile

			fi
		fi
	done
	
done < $root/$input

echo "Run" $outfile"."
