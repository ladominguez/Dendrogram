#!/bin/bash

root=/mnt/data01/antonio/Dropbox/BSL/CRSMEX/Dendrograms/2020MAR27/sequence_xc9500_coh9500
CAT=/mnt/data01/antonio/Dropbox/CRSMEX/Catalogs/CATALOG_2001_2019.DAT
cd $root

for dir in $(find -maxdepth 1 -type d -name "sequence_*" | sort);do
	cd $dir
	pwd
	awk -v cat="$CAT" '{print "grep " $1 " " cat}' ids.dat | bash > locmag.dat
	cd $root
done

