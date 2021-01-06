#!/bin/sh


ROOT='/mnt/data01/antonio/Dropbox/BSL/CRSMEX/Dendrograms/2020AGO07/sequence_xc9500_coh9500'

cd $ROOT

for k in $(ls -d sequence_*/SEQ*); do
cd $k
if [ -f "unique_member_id.info" ]; then
		rm unique_member_id.info
fi
echo "Working on file " $k " ..."
ls *.sac | awk -F. '{print $10}' | sort -n | uniq  > unique_member_id.info
cd $ROOT
done

echo "FINISHED"
