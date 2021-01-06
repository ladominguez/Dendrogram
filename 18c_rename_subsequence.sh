#!/bin/sh


ROOT='/mnt/data01/antonio/Dropbox/BSL/CRSMEX/Dendrograms/2020AGO07/sequence_xc9500_coh9500'

cd $ROOT

for k in $(ls -d sequence_*/SEQ*); do
	cd $k
	echo "Working on file " $k " ..."
	if [ -f "rename_seq.sh" ]; then
		rm rename_seq.sh
	fi
	touch rename_seq.sh
	cnt=0
	for id_seq in $(cat unique_member_id.info); do
		cnt=$((cnt+1))
		for sac_list in $(ls *$id_seq*sac); do
			echo $sac_list | awk -F$id_seq -v id="$id_seq" -v n="$cnt" '{printf("mv %s %s%s.%02d.sac\n" ,$0, $1, id, n )}' >> rename_seq.sh
		done
	done
	
	cat rename_seq.sh                                   > tmp0
	sed 's/sac/table/g' rename_seq.sh | sed 's/SYN.//g' > tmp1
	sed 's/sac/dat/g'   rename_seq.sh                   > tmp2

	cat  tmp0 tmp1 tmp2 > rename_seq.sh
        
	bash -v rename_seq.sh

	rm tmp*
		
	cd $ROOT
done

echo "FINISHED"
