import glob
import os
import numpy as np
import datetime
#matplotlib.use('agg')
import matplotlib.pyplot as plt
from   matplotlib import cm
root='/mnt/data01/antonio/Dropbox/BSL/CRSMEX/Dendrograms/2020MAR27/sequence_xc9500_coh9500'
directories=glob.glob(root + "/sequence_*/")


# Input: 
#   1. matrix.dist.dat
#   2. locmag_mean.dat
#
# Output:
#   1. rupture.eps
#   2. declusttering.log

input_file  = 'matrix.dist.dat'
locmag_file = 'locmag_mean.dat'
decluster_f = root + '/' + root.split('/')[-1] + '.declustter.log'
ds_lim      = 100e6

fout = open(decluster_f, "w+")
fout.write("# Decluster log from file 11_rupture_diagram.py\n ")
fout.write("# Stress drop limit - " + str(int(np.round(ds_lim/1e6))))
#print("Num. directories = ", len(directories))
directories.sort()
err=True

cmap = cm.get_cmap('gist_heat')

for dir in directories:
	os.chdir(dir)
	#print(dir)

	outputfile = dir.split('/')[-2] + '.rupture.eps'
	decluster  = False
	files_eps = glob.glob(outputfile)
	for file in files_eps:
		os.remove(file)

	if not os.path.exists(input_file):
		ferr = open(root+"/logs/11_error.log", "a+")
		if err:
			err=False
			ferr.write("# Error ocurred at:" + str(datetime.datetime.now()) + " in file 11_rupture_diagram.py\n")
		ferr.write(dir+ " is missing the file "+ input_file+ ".\n")
		ferr.close()		
		continue
	

	distan = np.genfromtxt(input_file,  dtype=float)	
	locmag = np.genfromtxt(locmag_file, dtype=float)
	
	ds     = np.linspace(10e6,10e7,11, endpoint=True)	
	Mw     = np.linspace(  2.0,4.5,26, endpoint=True) 
	M0     = np.power(10.0,1.5*Mw + 9.1);
	#print('Mw =', locmag[3])
	plt.figure(num=None, figsize=(6, 5), dpi=120, facecolor='w', edgecolor='k')
	for stress in ds:
		rgb = cmap(0.7*(stress - np.min(ds))/(np.max(ds)-np.min(ds)) + 0.3) 
		r = np.power((7/16)*(M0/stress),1.0/3);
		plt.plot(Mw, r,c=rgb)
	r_max = np.power((7/16)*(np.power(10.0,1.5*locmag[3] + 9.1)/ds_lim),1.0/3)
	for dl in distan:
		for d in dl:
			if d != 0.0:
				if d > r_max:
					decluster = True
				 
				plt.plot(locmag[3],d,"^",markersize=12, markerfacecolor='r', markeredgecolor='k')
	if decluster:
		ax = plt.gca()
		ax.set_facecolor('yellow')
		print(dir.split('/')[-2], ' needs to be decluster.')
		fout.write(dir.split('/')[-2] + ' needs to be decluster.\n')
				
	plt.text(3.75, 290.0, r'$\Delta\sigma=10\,MPa$', rotation=45.0, rotation_mode='anchor')
	plt.text(4.15, 180.0, r'$\Delta\sigma=100\,MPa$',rotation=35.0, rotation_mode='anchor')	
	plt.grid(linestyle='dotted')
	plt.xlabel('Magnitude')
	plt.ylabel('radius [m]')
	plt.xlim([Mw[0],Mw[-1]])
	plt.title(dir.split('/')[-2] + r'$\Delta\sigma_{Th}=$' + str(int(np.round(ds_lim/1e6))) + r'$\,MPa$')
	#plt.axvspan(lim_down, lim_up, color='0.75', alpha=0.5, lw=0)
	plt.tight_layout()
	plt.savefig(outputfile)
	plt.close("all")
	del distan
	del locmag
	os.chdir("../")
fout.close()
if not err:
	print("Errors occured during execution. Check file :", root+"/logs/11_error.log\n" ) 
