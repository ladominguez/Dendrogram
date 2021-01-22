# Some files have missing information, since the file was not used to detect the repeater.

INPUT=/Users/antonio/Dropbox/BSL/CRSMEX/Dendrograms/2020AGO07/scripts/fix_header_patch_31.dat
saclst kzdate kztime kstnm t5 dist f /Users/antonio/Dropbox/BSL/CRSMEX/Dendrograms/2020AGO07/sequence_xc9500_coh9500/sequence_*/raw/*sac | grep "\-12345" > $INPUT
while read line; do
    DIR=$(echo $line | cut -c 1-103)
    FILE=$(echo $line | cut -c 104-133)
    CAT=$(echo $line | awk -F'raw' '{print $1 "cat.dat"}')
    echo $line | awk  '{print $2 " "  $3 }'  | awk -F. '{print $1}' | awk -v cat="$CAT" '{print "grep \x22" $1 " " $2 "\x22 " cat}' | sh > tmp
    STA=$(echo $line | awk '{print $1}')
    T5=$(echo $line  | awk '{printf("%4.2f",$5)}')
    EVLA=$(awk '{print $3}' tmp)
    EVLO=$(awk '{print $4}' tmp)
    DEPT=$(awk '{print $5}' tmp)
    MAG=$( awk '{print $6}' tmp)
    echo $DIR $FILE $T5 $EVLA $EVLO $DEPT $MAG | awk '{print "cd " $1 "\nsac <<END\nread " $2 "\nch evla " $4 "\nch evlo " $5 "\nch evdp " $6 "\nch mag " $7 "\nch t5 " $3 "\nwh\nquit\nEND"}'
done < $INPUT
