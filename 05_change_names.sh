#!/bin/sh

ROOT='/mnt/data01/antonio/Dropbox/BSL/CRSMEX/Dendrograms/2020MAR27/sequence_xc9500_coh9500'

cd $ROOT

find . -name "*.table02" > tmp_table_name
sed 's/table02/sac/g' tmp_table_name > tmp_sac_names
paste tmp_table_name tmp_sac_names | awk '{print "mv " $1,$2}' > tmp.sh

sh tmp.sh

rm tmp*
