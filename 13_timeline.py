import glob, os
import numpy as np
from datetime import datetime, time
#matplotlib.use('agg')
import matplotlib.pyplot as plt

root='/mnt/data01/antonio/Dropbox/BSL/CRSMEX/Dendrograms/2020MAR27/sequence_xc9500_coh9500'
directories=glob.glob(root + "/sequence_*/")

# Input:
#   1. date_time.dat
#   2. time_dist.dat
#
# Output:
#   1. timeline.eps

input_file  = 'date_time.dat'
dist_file   = 'time_dist.dat'

lim_down    = 2001.0
lim_up      = 2019.0

print("Num. directories = ", len(directories))
directories.sort()

for dir in directories:
	first=True
	os.chdir(dir)
	outputfile = dir.split('/')[-2] + '.timeline.eps'
	print(dir)
	fin   = open(input_file,'r')
	dates = fin.read().splitlines()
	print(dates)
	files_prev = glob.glob("*.timeline.eps")
	dist       = np.genfromtxt(dist_file, usecols=1, dtype=float)
	for file in files_prev:
		os.remove(file)
	for date in dates:
		if first:
			b        = datetime.strptime(date,'%Y-%m-%d %H:%M:%S.%f')
			b_year   = datetime.strptime(str(b.year),'%Y')
			b_num    = b.year + (b-b_year).total_seconds()/(3600*24*365)
			first    = False
			timel    = list()
			lim_down = b.year - 0.5
			timel.append(b_num)
			continue
		else:
			a  = datetime.strptime(date,'%Y-%m-%d %H:%M:%S.%f')
			a_year = datetime.strptime(str(a.year),'%Y')
			a_num  = a.year + (a-a_year).total_seconds()/(3600*24*365)
			dt = a-b
			print("T1 = ", b_num, " T2 = ", a_num, " dt = ", dt)
			b  = a
			b_year = datetime.strptime(str(b.year),'%Y')
			b_num  = b.year + (b-b_year).total_seconds()/(3600*24*365)
			lim_up = np.ceil(b.year) + 0.5
			timel.append(b_num)
	timea = np.asarray(timel, dtype=np.float32)
	#print(timel)
	plt.figure(num=None, figsize=(6, 2), dpi=120, facecolor='w', edgecolor='k') 
	try:
		plt.plot(timea,dist[0]*np.ones(timea.size),'ko-',markerfacecolor='r')		
	except:
		ferr = open(root+"/logs/12_error.log", "a+")

		ferr.write("# Error ocurred at:" + str(datetime.now()) + "in file 12_timeline.py\n")
		ferr.write("Impossible to plot " + dir + "\n")
		ferr.close()
		continue	
	
	plt.xlim([lim_down,lim_up])
	plt.ylim([0.0, 800.0])
	plt.ylabel('Distance along the coast [km]')
	plt.xlabel('Year')
	plt.title(dir.split('/')[-2])
	plt.grid(linestyle='dotted')
	plt.savefig(outputfile)
	del timel
	del timea
	del dist 
