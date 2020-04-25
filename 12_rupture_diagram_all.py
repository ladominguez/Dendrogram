import glob
import os
import numpy as np
import datetime
#matplotlib.use('agg')
import matplotlib.pyplot as plt
from random import choice

root='/mnt/data01/antonio/Dropbox/BSL/CRSMEX/Dendrograms/2020MAR27/sequence_xc9500_coh9500'
directories=glob.glob(root + "/sequence_*/")


# Input: 
#   1. matrix.dist.dat
#   2. locmag_mean.dat
#
# Output:
#   1. rupture.eps

input_file  = 'matrix.dist.dat'
locmag_file = 'locmag_mean.dat'


print("Num. directories = ", len(directories))
directories.sort()
err=True
m=["o","v","^","<",">","s","p","P","D"]
c=["b", "g", "r", "c", "m", "y", "k", "w"]
outputfile = root + '/' + root.split('/')[-1] + '.rupture.eps'
plt.figure(num=None, figsize=(6, 5), dpi=120, facecolor='w', edgecolor='k')


for dir in directories:
	os.chdir(dir)
	print(dir)



	if not os.path.exists(input_file):
		continue
	

	distan = np.genfromtxt(input_file,  dtype=float)	
	locmag = np.genfromtxt(locmag_file, dtype=float)
	print(distan)
	distan = np.unique(distan)
	print(distan)
	#for dl in distan:
	for d in distan:
		if d != 0.0:
			print('dl : ', d, ' mag : ', locmag[3])
			plt.plot(locmag[3],d,markersize=12, markerfacecolor=choice(c), markeredgecolor='k',marker=choice(m))
	
	del distan
	del locmag
	#os.chdir("../")


ds     = np.linspace(10e6,10e7,11, endpoint=True)	
Mw     = np.linspace(  2.0,4.5,26, endpoint=True) 
M0     = np.power(10.0,1.5*Mw + 9.1);
for stress in ds:
	r = np.power((7/16)*(M0/stress),1.0/3);
	plt.plot(Mw, r)
plt.text(3.75, 290.0, r'$\Delta\sigma=10\,MPa$', rotation=60.0, rotation_mode='anchor')
plt.text(4.15, 180.0, r'$\Delta\sigma=100\,MPa$',rotation=50.0, rotation_mode='anchor')
plt.grid(linestyle='dotted')
plt.xlabel('Magnitude')
plt.ylabel('radius [m]')
plt.xlim([2.5,4.5])
	#plt.axvspan(lim_down, lim_up, color='0.75', alpha=0.5, lw=0)
plt.ylim([0.0, 400.0])

files_out = glob.glob(outputfile)
for file in files_out:
	os.remove(file)
plt.savefig(outputfile)
plt.close("all")

print("Figure save as : ", outputfile)
