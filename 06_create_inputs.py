import glob
import os
import yaml

# Run in the directory /data01/antonio/Dropbox/BSL/CRSMEX/Dendrograms/2019JUN11/sequence_xc9500_coh9500
params = yaml.load(open('params.yaml','r').read())
root   = params['root']

os.chdir(root)
directories=glob.glob("./sequence_*/")

print("Num. directories = ", len(directories))
directories.sort()

for dir in directories:
	os.chdir(dir)
	print("Directory ", dir)
	fsta      = open("station_ids.info")
	stations  = fsta.read().splitlines()
	Nsta      = len(stations)
	previous  = glob.glob("./input*.in")
	print("Nsta = ", Nsta)
	print(stations)
	if len(previous) >= 1:
		print("Removing previous files:")
		for prev in previous:
			os.remove(prev)
	
	for sta in stations:

		files_sac = glob.glob('SYN.' + sta + '*.sac')
		files_sac.sort()
		N         = len(files_sac)
		m         = 0
		counter   = 1
		print("Numer of files ", N)

		for file in files_sac:
			m = m + 1
			index = range(m,N)
			for k in index:
       				fileout = 'input_' +sta + '_' + '{0:03d}'.format(counter)  + '_' \
                        		           	      + '{0:03d}'.format(m      )  + '_' \
                                 		   	      + '{0:03d}'.format(k+1    )  + '.in'
	       			fid = open(fileout,'w+')
        			fid.write(file + '\n')
	        		fid.write(files_sac[k] + '\n')
	        		fid.write('\n')
	        		fid.write('\n')
	        		fid.close()
	        		print("File ", fileout, " created.")
	        		counter = counter + 1
	os.chdir("../")
