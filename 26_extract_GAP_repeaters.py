#!/bin/python

import yaml, glob
from datetime import datetime

params   = yaml.load(open('params.yaml','r').read(), Loader=yaml.FullLoader)
root     = params['root']

input1   = root + '/time_intervals_xc9500_coh9500.declustter.dat'
lat_min  = 16.2
lat_max  = 17.8
lon_min  = -102.0
lon_max  = -100.0

date1    = datetime.strptime('2017-11-01', '%Y-%m-%d')
date2    = datetime.strptime('2018-11-16', '%Y-%m-%d')

crs_file = glob.glob(input1)

with open(crs_file[0]) as fp:
    line = fp.readline()
    while line:
        line = line.strip()
        info = line.split(':')
        loc  = info[0].split()
        date = info[3].split()
        lat  = float(loc[0])
        lon  = float(loc[1])
        if lat >= lat_min and lat <= lat_max:
            if lon >= lon_min and lon <= lon_max:
                for dt in date:
                    dtf = datetime.strptime(dt, '%Y/%m/%d')
                    if dtf >= date1 and dtf <=date2:
                        print(line)
                        break
        
        line = fp.readline()

print("Run python 26_extract_GAP_repeaters.py > obs_recorded.dat to save data.")
