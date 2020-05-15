import glob, os
import numpy as np
from datetime import datetime, time
#matplotlib.use('agg')
import matplotlib.pyplot as plt
from   matplotlib import cm
import matplotlib as mpl
import yaml

params = yaml.load(open('params.yaml','r').read())#,Loader=yaml.FullLoader)
root   = params['root']
#root='/Users/antonio/Dropbox/BSL/CRSMEX/Dendrograms/2020MAR27/sequence_xc9500_coh9500'
directories=glob.glob(root + "/sequence_*/")

# Input:
#   1. date_time.dat
#   2. matrix.dist.dat
#   3. locmag_mean.dat
#
# Output:
#   1. sequence_xc9500_coh9500.time_vs_dist.eps

input_file  = 'date_time.dat'
rel_distf   = 'matrix.dist.dat'
dist_file   = 'time_dist.dat'
locmag_file = 'locmag_mean.dat'

ds          = 100e6
dt_lim      = params['dt_lim']
# Guerrero Gap
ggap_W      = 321.42;
ggap_E      = 544.37;
ggap_x      = np.array([ggap_W, ggap_E])
err_flag    = False

print("Num. directories = ", len(directories))
directories.sort()
outputfile = root + '/' + root.split('/')[-1] + '.time_vs_distance_coast.png'

plt.figure(num=None, figsize=(9, 6), dpi=300, facecolor='w', edgecolor='k') 

cmap   = plt.cm.get_cmap('hot')
#norm   = mpl.colors.SymLogNorm(2.6, vmin=2.5, vmax=4.5)
norm   = mpl.colors.Normalize(vmin=2000, vmax=2020)

sm = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)
sm.set_array([])
mag   = [2.5,   3.0,  3.5,  4.0,  4.5]
tyear = [2000, 2005, 2010, 2015, 2020]
#cm.set_clim(0, 2.0)
for dir in directories:
	first=True
	os.chdir(dir)
	
	#print(dir)
	fin   = open(input_file,'r')
	dates = fin.read().splitlines()

	#if not len(dates) == 2:
	#	print('Skipping ', dir)
	#	continue
	
	dist_coast = np.genfromtxt(dist_file, usecols=1, dtype=float)
	locmag     = np.genfromtxt(locmag_file, dtype=float)
	try:
		rel_dist   = np.genfromtxt(rel_distf, dtype=float )
	except:
		ferr = open(root+"/logs/13_error.log", "a+")
		ferr.write("# Error ocurred at:" + str(datetime.now()) + "in file 13_time_vs_dist.py\n")
		ferr.write("Couldn't open file " + root + rel_distf)
		ferr.close()
	counter = 0
	for date in dates:
		if first:
			b      = datetime.strptime(date,'%Y-%m-%d %H:%M:%S.%f')
			b_year = datetime.strptime(str(b.year),'%Y')
			b_num  = b.year + (b-b_year).total_seconds()/(3600*24*365)
			first  = False
			timel  = list()
			timel.append(b_num)
			continue
		else:
			a      = datetime.strptime(date,'%Y-%m-%d %H:%M:%S.%f')
			a_year = datetime.strptime(str(a.year),'%Y')
			a_num  = a.year + (a-a_year).total_seconds()/(3600*24*365)
			dt     = a-b
			b      = a
			b_year = datetime.strptime(str(b.year),'%Y')
			b_num  = b.year + (b-b_year).total_seconds()/(3600*24*365)
			if rel_dist[counter][counter+1] == 0.0:
				continue

			r_max = np.power((7/16)*(np.power(10.0,1.5*locmag[3] + 9.1)/ds),1.0/3)
			mag_size=20*((locmag[3]-2)/3) + 1
		
			if len(dates) >= 2:
				#rgb = cmap((locmag[3] - 2.5)/2.0) 
				rgb = cmap((b_num - 2000)/20) 
				if dt.total_seconds() >= dt_lim: 
					if rel_dist[counter][counter+1] < r_max:
						plt.semilogy(dist_coast[0], (dt.total_seconds()),'ko-',markerfacecolor=rgb, markersize=np.round(mag_size))		
					else:
						plt.semilogy(dist_coast[0], (dt.total_seconds()),'ko-',markerfacecolor=rgb, markersize=np.round(mag_size))
		del dt
	del date
	del dates
fig  = plt.gcf()
axes = plt.gca()
limx = axes.get_xlim()
limy = axes.get_ylim()
top = np.array([limy[1], limy[1]])
axes.fill_between(ggap_x, limy[0], top, facecolor='red', alpha=0.25, edgecolor='r')
plt.semilogy(np.array(limx),np.array([     3600,       3600]),'k',linestyle='--',linewidth = 1)
plt.semilogy(np.array(limx),np.array([    86400,      86400]),'k',linestyle='--',linewidth = 1)
plt.semilogy(np.array(limx),np.array([  2419200,    2419200]),'k',linestyle='--',linewidth = 1)
plt.semilogy(np.array(limx),np.array([ 31536000,   31536000]),'k',linestyle='--',linewidth = 1)
plt.semilogy(np.array(limx),np.array([315360000, 315360000]),'k',linestyle='--',linewidth = 1)

plt.text(250, 1.2*3600,      '1hour',   color='k')		
plt.text(250, 1.2*86400,     '1day',    color='k')		
plt.text(250, 1.2*2419200,   '1month',  color='k')		
plt.text(250, 1.2*31536000,  '1year',   color='k')		
plt.text(250, 1.2*315360000, '10years', color='k')		
plt.text(340,     1400, 'Guerrero Gap', color='k',fontsize=16)		

#plt.xlim([lim_down,lim_up])
#plt.ylim([0.0, 800.0])
#plt.title(dir.split('/')[-2])
plt.grid(linestyle='dotted')
plt.xlabel('Distance along the coast [m]')
plt.ylabel('Time [s]')
plt.title('Assumed stress drop - ' + r'$\Delta\sigma=\,$' + str(int(np.round(ds/1e6))) + r'$\,MPa$')
axes.set_xlim(limx)
axes.set_ylim(limy)
plt.colorbar(sm, ticks=tyear, format=mpl.ticker.ScalarFormatter(),)
plt.savefig(outputfile)
