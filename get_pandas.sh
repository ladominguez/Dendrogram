#!/bin/sh

cat ../sequence_xc9500_coh9500/sequence_*/raw/s*.DISP.dat | head -1 >       ../sequence_xc9500_coh9500/stress_drop.DISP.dat
cat ../sequence_xc9500_coh9500/sequence_*/raw/s*.DISP.dat | grep -v Wave >> ../sequence_xc9500_coh9500/stress_drop.DISP.dat 

cat ../sequence_xc9500_coh9500/sequence_*/raw/s*.VEL.dat | head -1      >  ../sequence_xc9500_coh9500/stress_drop.VEL.dat
cat ../sequence_xc9500_coh9500/sequence_*/raw/s*.VEL.dat | grep -v Wave >> ../sequence_xc9500_coh9500/stress_drop.VEL.dat 

cat ../sequence_xc9500_coh9500/sequence_*/raw/s*.ACC.dat | head -1      >  ../sequence_xc9500_coh9500/stress_drop.ACC.dat
cat ../sequence_xc9500_coh9500/sequence_*/raw/s*.ACC.dat | grep -v Wave >> ../sequence_xc9500_coh9500/stress_drop.ACC.dat 
