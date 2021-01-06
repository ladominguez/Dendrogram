#!/bin/sh

ROOT=/Users/antonio/Dropbox/BSL/CRSMEX/Dendrograms/2020AGO07/sequence_xc9500_coh9500
CAT=/Users/antonio/Dropbox/CRSMEX/Catalogs/CATALOG_2001_2020.DAT
INPUT1=ids.dat
INPUT2=station_ids.info
OUTPUT1=cat.dat
OUTPUT2=get.stp
OUTPUT3=add_t5.macro
OUTDIR=raw
STP=/Users/antonio/bin/SSNstp

add_pickings_t0(){

touch $dir/$OUTDIR/$OUTPUT3
#echo "ADD_PICKS"
for sacfile in $(find $dir -maxdepth 1 -name "*sac" | grep -v SYN);do
    echo "file: ", $sacfile
    a=$(saclst a f $sacfile | awk '{printf("%.2f",$2)}')
    t5=$(saclst t5 f $sacfile | awk '{printf("%.2f",$2)}')
    mag=$(saclst mag f $sacfile | awk '{print $2}')
    evla=$(saclst evla f $sacfile | awk '{print $2}')
    evlo=$(saclst evlo f $sacfile | awk '{print $2}')
    evdp=$(saclst evdp f $sacfile | awk '{print $2}')
    kstnm=$(saclst kstnm f $sacfile | awk '{print $2}')
    kztime=$(saclst kztime f $sacfile | awk '{print $2}' | sed 's/://g' | awk -F. '{print $1}')
    kzdate=$(saclst kzdate f $sacfile | awk '{print $2}' | sed 's/\///g')
    if (( $(echo "$a == -12345" | bc -l ) )); then
        if (( $(echo "$t5 == -12345" | bc -l ) )); then
            echo "ERROR: No picking information."
        else
            pwave=$t5
        fi
    else
        pwave=$a
    fi

    echo $kstnm $kzdate $pwave $evla $evlo $evdp $mag | awk '{print "sac <<END\nread " $2 "*" $1 "*sac\nch t5 "$3 "\nch evla " $4 "\nch evlo " $5 "\nch evdp " $6 "\nch mag " $7 "\nwh\nquit\nEND"}' >> $dir/$OUTDIR/$OUTPUT3
    
done

}

for dir in $(find "$ROOT" -maxdepth 1 -type d -name "sequence_*N*" | sort ); do
    cd $dir
    echo $dir
    if [ ! -f "$INPUT1" ]; then
        echo "ERROR. File " $INPUT1 " does not exists in " $DIR
        exit 1
    else
        if [ ! -f "$OUTPUT1" ]; then
            grep -f $INPUT1 $CAT > $OUTPUT1
        fi

        if [ ! -d "$OUTDIR" ];then
            mkdir $OUTDIR
        fi
        rm $OUTDIR/$OUTPUT2
        if [ ! -f "$OUTPUT2" ]; then
            touch $OUTDIR/$OUTPUT2
            while read sta; do 
                awk -v st="$sta" '{print "WIN IG " st " HHZ " $1 "," $2 " +200s"}' $OUTPUT1 >> $OUTDIR/$OUTPUT2
            done < $INPUT2
        fi
        Nsac=$(find $dir/$OUTDIR -name "*.sac" | wc -l)
        if [ "$Nsac" -gt "0" ]; then
            echo "sac files already downloaded."
            cd $dir
        else   # Downlaod waveforms
            cd $dir/$OUTDIR
            $STP < $dir/$OUTDIR/$OUTPUT2
            cd $dir
        fi
        if [ ! -s "$dir/$OUTDIR/$OUTPUT3" ]; then
                echo "HOLA"
                add_pickings_t0
                cd $dir/$OUTDIR
                bash $dir/$OUTDIR/$OUTPUT3
        fi

    fi
    cd $ROOT
done

