import glob, os
import numpy as np


root   = '/mnt/data01/antonio/Dropbox/BSL/CRSMEX/Dendrograms/2020AGO07/sequence_xc9500_coh9500'
files  = glob.glob(root + "/sequence_*/*sequence.dat" )
ds_lim = 100e6  # Stress drop in Pa



files.sort()
seq_id  = 0
for file in files:
	sequence  = file.split('/')[-2]
	directory = root + '/' + sequence +'/'
	prev_file = glob.glob(directory + '*.discard.dat')
	for f in prev_file:
		print(f)
		os.remove(f)

	prev_file = glob.glob(directory + '*.make.subsequences.sh')
	for f in prev_file:
		print(f)
		os.remove(f)
	
	if os.stat(file).st_size == 0:
		print('Directory', directory, ' is empty.')
		fout = open(directory + sequence + '.discard.dat','w') 
		fout.write('Discard sequence ' + sequence + '\n')
		fout.close()
		
	else:
		print(file)
		out_file = directory + sequence + '.make.subsequences.sh'
		fsh      = open(out_file, 'w')
		with open(file) as fp:
			line = fp.readline()
			cnt  = 0
			while line:
				cnt     = cnt + 1
				seq_id  = line.strip().split(':')[0] 
				mem_id  = line.strip().split(':')[1]
				mem_id  = mem_id.replace('[', '')
				mem_id  = mem_id.replace(']', '')
				members = list(mem_id.split(','))
				fsh.write('mkdir ' + directory + seq_id + '\n')
				for k in members:
					k_int = int(float(k))
					lout1 = 'cp ' + directory + '*' + '{0:02d}'.format(k_int) + '.sac '   + directory + seq_id + '/\n'
					lout2 = 'cp ' + directory + '*' + '{0:02d}'.format(k_int) + '.dat '   + directory + seq_id + '/\n'
					lout3 = 'cp ' + directory + '*' + '{0:02d}'.format(k_int) + '.table ' + directory + seq_id + '/\n'
					fsh.write(lout1)
					fsh.write(lout2)
					fsh.write(lout3)
				line = fp.readline()
		fp.close()
	
