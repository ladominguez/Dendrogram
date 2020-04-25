import glob
import os
import numpy as np
#matplotlib.use('agg')
import matplotlib.pyplot as plt
import jul2mmdd

root='/mnt/data01/antonio/Dropbox/BSL/CRSMEX/Dendrograms/2020MAR27/sequence_xc9500_coh9500'
directories=glob.glob(root + "/sequence_*/SEQ*")

# Input: 
#   1. files stations_ids.info
#   2. s_p_time.dat
#   3. CORR.(Station name).dat
#
# Output:
#   1. (Station name).correli.dat
#   2. (Station name).correli.eps

print("Num. directories = ", len(directories))
directories.sort()

lim_down = 0.0  #lim_down and lim_up are estimated during runtime
lim_up   = 0.0
win_time = 5.0
scl_time = 3.0 # the time window will start at scl_time time the s-p time

for dir in directories:
	os.chdir(dir)

	correli_dat = glob.glob("*correli.dat")
	correli_png = glob.glob("*correli.png")
	correli_eps = glob.glob("*correli.eps")
 
	for file_dat in correli_dat:
		os.remove(file_dat)

	for file_png in correli_png:
		os.remove(file_png)

	for file_eps in correli_eps:
		os.remove(file_eps)

	print("Directory ", dir)
	fsta      = open("../station_ids.info")
	stations  = fsta.read().splitlines()
	Nsta      = len(stations)
	print("Nsta = ", Nsta)
	print(stations)
	sp_time={}
	with open('../s_p_time.dat') as f:
		for line in f:
			(key,val)    = line.split()
			sp_time[key] = float(val)
	
	for sta in stations:
		files_corr = glob.glob('CORR.*' + sta + '*.dat')
		files_corr.sort()
		N          = len(files_corr)
		m          = 0
		counter    = 0
		print("Number of files ", N)
		fileout    = sta + ".correli.dat"
		fout       = open(fileout, 'w+')
		lim_down   = scl_time*sp_time[sta]
		lim_up     = lim_down + win_time
		plt.figure(num=None, figsize=(6, 10), dpi=80, facecolor='w', edgecolor='k')
		files_wav  = glob.glob('SYN.*' + sta + '*.dat')
		files_wav.sort()
		plt.subplot(311)
		offset     = 1
		for wavefile in  files_wav:
			wave            = np.genfromtxt(wavefile)
			print("Reading ", wavefile, " size = ", wave.size)
			year   = wavefile.split('.')[6]
			jday   = wavefile.split('.')[7]
			hhmm   = wavefile.split('.')[8]
			mm, dd = jul2mmdd.jul2mmdd(int(year), int(jday))
			date   = year + "/" + str(mm) + "/" + str(dd) + " " + hhmm[0:2] + ":" + hhmm[2:4]
			if wave.size == 0:
				print("Error in ", dir, wavefile, " size = ", wave.size)
				break
			t               = wave[:,0]
			A               = wave[:,1]
			A               = 0.5*A/A.max() + offset
			offset          = offset + 1
			plt.plot(t,A,linewidth=0.25)
			plt.text(0.70*t[-1],offset - 0.95,date)
		plt.axvspan(lim_down, lim_up, color='0.75', alpha=0.5, lw=0)
		plt.title(sta)
		plt.axis('tight')
			
		for filec in files_corr:
			data            = np.genfromtxt(filec)
			counter         = counter +1
			time            = data[:,0]
			xcorr           = data[:,1]
			distv           = data[:,2]
			plt.subplot(312)
			plt.plot(time,xcorr,linewidth=0.5)
			plt.ylabel('X-corr Max')
			plt.xlabel('Time, s')
			plt.axvspan(lim_down, lim_up, color='0.75', alpha=0.5, lw=0)
			plt.axis('tight')
			plt.subplot(313)
			plt.plot(time,distv,linewidth=0.5)
			plt.ylabel('Relat. Dist, m')
			plt.xlabel('Time, s')
			plt.axvspan(lim_down, lim_up, color='0.75', alpha=0.5, lw=0)
			plt.axis('tight')
			ind     = np.where((time >= lim_down) & (time <= lim_up)) 
			dist    = distv[ind]
			dmean   = np.mean(dist)
			dstd    = np.std(dist)
			lout    = filec + ' ' + '{0:3d}'.format(counter)   + \
					  ' ' + '{0:7.3f}'.format(dmean)   + \
                                          ' ' + '{0:7.3f}'.format(dstd)    + '\n'
			fout.write(lout)
			del data 
			del time 
			del distv 
			del xcorr 
			del ind 
			del dist 
			del dmean 
			del dstd

		plt.tight_layout()
		plt.savefig(sta + '.correli.eps')
		plt.close()
		fout.close()
		print("Writing file ", fileout, " ...")
	
	os.chdir(root)
