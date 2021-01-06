import glob, os, yaml
import numpy as np
from datetime import datetime, time, timedelta

# Input files
input1 = 'locmag_mean.dat'
input2 = 'unique_member_id.info'
input3 = '.discard.dat'
input4 = 'date_time.dat'

params  = yaml.load(open('params.yaml','r').read()) #:wq Loader=yaml.FullLoader)
root    = params['root']

os.chdir(root)
directories=glob.glob(root + "/sequence_*/")
directories.sort()

for dir in directories:
	subdir = dir.split('/')[-2]
	#print( subdir )
	if os.path.isfile(dir + subdir + input3):
		continue
	else:
		locmag = np.genfromtxt(dir + input1)
		#print(dir)
		subsequences = glob.glob(dir + '/SEQ*/');
		subsequence_flag = False
		if len(subsequences) == 0:
			subsequences = {dir}
		else:
			seq_cnt          = 0
			subsequence_flag = True
		#print('subsequences: ', subsequences, ' len - ', len(subsequences))
		for seq in subsequences:
			outline = "{0:6.3f}".format(locmag[0]) + "{0:9.3f}".format(locmag[1]) + "{0:6.1f}".format(locmag[2]) + "{0:4.1f}".format(locmag[3])
			#print(seq.split('/')[-1])
			#print(seq)	
			N_seq = np.genfromtxt(seq + input2)
			try:
				outline = outline + '   : ' + str(len(N_seq)) + '  : '
			except:
				continue
			ids = ''	
			for eq_in in N_seq:
				ids = ids + ' ' + '{:08d}'.format(int(eq_in)) 	
			f     = open(seq + input4,'r')
			lines = f.readlines()
			cnt   = 0
			for line in lines:
				if cnt == 0:
					d1       = datetime.strptime(line.strip(), '%Y-%m-%d %H:%M:%S.%f')
					cnt      = 1
					outdates = line.split()[0]
					continue
				else:
					d2  = datetime.strptime(line.strip(), '%Y-%m-%d %H:%M:%S.%f')
					dd  = d2 - d1
					dds = dd.total_seconds()/timedelta(days=365).total_seconds()
					d1  = d2
					#print(dd)
					#print(dds)
					outline  = outline + "{0:7.3f}".format(dds)
					outdates = outdates + ' ' + line.split()[0]
			
			if subsequence_flag:
				seq_cnt = seq_cnt + 1
				outline = outline + ' : ' + outdates.replace('-','/') + ' : ' + ids + ' : ' + seq.split('/')[-3] +  ' : SEQ' + str(seq_cnt)
			else: 
				outline = outline + ' : ' + outdates.replace('-','/') + ' : ' + ids + ' : ' + seq.split('/')[-2]

			f.close()
			#print(seq.split('/')[-2])
			print(outline)
print("Run python 24_generate_decluster_catalog.py ../sequence_xc9500_coh9500/time_intervals_xc9500_coh9500.declustter.dat to save the data.")
print("WARNING: Remove the last line: Run python 24_generate.... ")

