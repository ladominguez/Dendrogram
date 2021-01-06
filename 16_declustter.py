import glob
import numpy as np


root   = '/mnt/data01/antonio/Dropbox/BSL/CRSMEX/Dendrograms/2020AGO07/sequence_xc9500_coh9500'
files  = glob.glob(root + "/sequence_*/decluster.dat" )
ds_lim = 100e6

files.sort()
seq_id  = 0
print("No. files: ", len(files))
for file in files:
	file_log = ".decluster.log"
	seq_file = ".subsequence.dat"
	seq_id  = file.split('/')[-2]

	for pfile in glob.glob(root + '/*' + file_log):
		os.remove(pfile)
	
	for pfile in glob.glob(root + '/*' + seq_file):
		os.remove(pfile)
	 
	file_log = root + '/' + seq_id   + '/' + seq_id + file_log
	seq_file = root + '/' + seq_id   + '/' + seq_id + seq_file
	print(file_log)
	print(seq_file)

	flog     = open(file_log, 'w')
	fsub     = open(seq_file, 'w')


	locmag_file = file.replace('decluster.dat','locmag_mean.dat')
	out_seq = list([])
	print( '\n\nDeclustering ', file)
	flog.write('Declustering ' +  file)

	mag         = np.genfromtxt(locmag_file, usecols=3, dtype=float)
	r_max       = np.power((7/16)*(np.power(10.0,1.5*mag + 9.1)/ds_lim),1.0/3)
	decluster   = np.genfromtxt(file,dtype=float) 
	N           = decluster.shape[0] + 1
	print(     'Magnitude: ', mag)
	print('r_max:     ', r_max, ' m.')
	print('************')
	flog.write('Magnitude: '+  str(mag) + '\n')
	flog.write('r_max:     '+  str(r_max) + ' m.\n')
	flog.write('************\n')

	if decluster.ndim == 1:
		print(decluster)
		print('Remove sequence: ', file )
		flog.write(str(decluster) + '\n')
		flog.write('Remove sequence: ' + file + '\n' )
		continue
	
	decluster[:,0] = decluster[:,0] + 1
	decluster[:,1] = decluster[:,1] + 1
	print('decluster.shape: ', decluster.shape)
	print(decluster)
	print('N: ', N)
	flog.write('decluster.shape: ' +  str(decluster.shape) + '\n')
	flog.write(str(decluster) + '\n')
	flog.write('N: ' + str(N) + '\n')

	row_no = 0
	seq_id = 0
	links  = {}
	for row in decluster:
		row_no = row_no + 1
		if row[2] < r_max:
			
			if row[0] <= N and row[1] <= N:
				seq = []
				seq.append(row[0])
				seq.append(row[1])
				out_seq.append(seq)
				links[N+row_no] = seq_id
				seq_id          = seq_id + 1  
				print('Row: ', row_no, ' Members: ', int(row[0]), int(row[1]), ' New sequence created. Seq_id: ', seq_id - 1, ' link_id: ', N+row_no)
				flog.write('Row: ' +  str(row_no) + ' Members: ' + str(int(row[0])) + ' '+ str(int(row[1])) + ' New sequence created. Seq_id: ' +  str(seq_id - 1) + ' link_id: ' +  str(N+row_no) + '\n')

			if row[0] <= N and row[1] > N:
				id_link = links[row[1]]
				N_seq   = len(out_seq)
				if N_seq > 1:
					out_seq[id_link].append(row[0])
				else:
					
					out_seq[0].append(row[0])

				links[N+row_no] = id_link
				print('Row: ', row_no, ' Members: ', int(row[0]), int(row[1]), ' Member: ', row[0], ' added to sequence: ', id_link, ' link_id: ', N+row_no )
				flog.write('Row: ' + str(row_no) + ' Members: ' + str(int(row[0])) + ' ' + str(int(row[1])) + ' Member: ' + str(row[0]) + ' added to sequence: ' + str(id_link) + ' link_id: ' +  str(N+row_no) + '\n' )

			if row[0] > N and row[1] > N:
				links[N+row_no] = seq_id
				#seq_id          = seq_id + 1 
				 
				A_seq = links[row[0]]
				B_seq = links[row[1]]
				print('Merging sequence ' + str(A_seq) + ' and ' +  str(B_seq))
				flog.write('Merging sequence ' + str(A_seq) + ' and ' +  str(B_seq) + '\n')
				for member in out_seq[B_seq]:
					out_seq[A_seq].append(member)
				out_seq[B_seq].clear()
				links[N+row_no] = A_seq
				print('Merged sequence: ', out_seq[A_seq], ' new_link_id: ', N+row_no)
				print('Row: ', row_no, ' Members: ', int(row[0]), int(row[1]), ' Merged in seq: ', A_seq, ' link_id: ', N+row_no)
				flog.write('Merged sequence: ' + str(out_seq[A_seq]) + ' new_link_id: ' +  str(N+row_no) + '\n')
				flog.write('Row: ' + str(row_no) + ' Members: ' +  str(int(row[0])) + ' ' + str(int(row[1])) + ' Merged in seq: ' +  str(A_seq) + ' link_id: ' + str( N+row_no) + '\n')
			print('Links: ',links)
		else:
			print(     'Row: ', row_no, ' Members: ', row[0], row[1], '. Out of range: ', row[2], ' > ', r_max)
			flog.write('Row: ' +  str(row_no) + ' Members: ' +  str(row[0]) + ' ' + str(row[1]) + '. Out of range: ' + str(row[2]) +  ' > ' +  str(r_max) + '\n')

	seq_id = 1
	print(     'out_seq: ', out_seq)
	flog.write('out_seq: ' +  str(out_seq) + '\n')
	for seq in out_seq:
		seq.sort()
		if len(seq) >= 2:
			print('SEQ', seq_id, ': ',seq )
			fsub.write('SEQ' +  str(seq_id) +  ': ' + str(seq) + '\n')
			seq_id = seq_id + 1
	del links
	del out_seq
	flog.close()
	fsub.close()
				
						
