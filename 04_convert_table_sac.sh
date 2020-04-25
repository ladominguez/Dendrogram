#!/bin/sh

#  Morelia, Michoacan. 2019/06/11
# This code converts all table file in each sequence_###_### subdirectory into sac files.
#
# ladominguez@seismo.berkeley.edu


ROOT='/mnt/data01/antonio/Dropbox/BSL/CRSMEX/Dendrograms/2020MAR27/sequence_xc9500_coh9500'

cd $ROOT

for k in $(ls -d sequence_*/); do
cd $k
echo "Working on directory " $k  "..."
for m in $(ls *.table); do
t1=$(head -1 $m |           awk '{printf("%6.5f\n",$1)}')
t2=$(head -2 $m | tail -1 | awk '{printf("%6.5f\n",$1)}')
dt=$(echo $t1, $t2 | awk '{printf("%6.5f\n", $2 -$1)}')
echo $dt
sac << END
readtable $m
dc 1
ch delta $dt
lh 
w prepend SYN.
quit
END
done
cd ..
done
echo "FINISHED."
