#!/bin/sh


ROOT='/mnt/data01/antonio/Dropbox/BSL/CRSMEX/Dendrograms/2020MAR27/sequence_xc9500_coh9500'

cd $ROOT

for k in $(ls -d sequence_*/); do
cd $k
echo "Working on file " $k " ..."
ls *.sac | awk -F. '{print $9}' | sort -n | uniq  > unique_member_id.info
cd ..
done

echo "FINISHED"
