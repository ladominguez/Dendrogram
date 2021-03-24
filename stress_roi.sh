#!/bin/sh

INPUT1=/Users/antonio/Dropbox/BSL/CRSMEX/Dendrograms/2020AGO07/sequence_xc9500_coh9500/sequence_stress.dat
INPUT2=/Users/antonio/Dropbox/BSL/CRSMEX/Dendrograms/2020AGO07/sequence_xc9500_coh9500/time_intervals_xc9500_coh9500.filter.dat


echo $INPUT1
awk '{if ($2 >= 16.22 && $2 <= 16.40 && $3 >= -98.33 && $3 <= -98.21) print $0}' $INPUT1 

echo $INPUT2
awk '{if ($2 >= 16.22 && $2 <= 16.40 && $3 >= -98.33 && $3 <= -98.21) print $0}' $INPUT2
