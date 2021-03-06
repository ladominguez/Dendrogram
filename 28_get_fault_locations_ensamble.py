#!/bin/python

import glob, torch, glob
import numpy as np
from scipy.spatial.distance import pdist, squareform

#params   = yaml.load(open('params.yaml','r').read(),Loader=yaml.FullLoader)
#root     = params['root']

root         = '/mnt/data01/antonio/Dropbox/BSL/CRSMEX/Dendrograms/2020AGO07/sequence_xc9500_coh9500'
output_file1 = 'inversion'
output_file2 = 'inverted.matrix'
output_file3 = 'inverted.matrix'

def get_loss():
    loss = 0.
    for i in range(N):
        for j in range(i+1,N):
            loss += torch.abs(torch.sum((xy[i]-xy[j])**2)-A[i,j]**2)
    return loss


files1 = glob.glob(root + '/sequence_00438*/matrix.dist.dat')
file=files1[0]
files1.sort()

files_all = files1

Nf     = len(files1)
Na     = len(files_all)
Ni     = 100

print('Number of matrix files: ', len(files_all))

cnt = 0
for iter in range(Ni):
    print("Runing iteration: ", iter)
    output_file1 = 'inversion.' + '{:05d}'.format(iter) + '.dat'
    output_file2 = 'inverted.matrix.' + '{:05d}'.format(iter+13) + '.dat'
    output_file3 = 'inverted.matrix.' + '{:05d}'.format(iter+13) + '.dat'
    cnt = cnt + 1
    print(files1[0])
    distan = np.genfromtxt(file,  dtype=float)
    N      = distan.shape[0]
    if N >= 5:
        if cnt > Nf:
            root_work = file.split('/')[-3] + '/' + file.split('/')[-2]
        else:
            root_work = file.split('/')[-2]
        root_work = file.split('/')[-2]
        print('Root: ', root)
        print('Root work:', root_work)
        ofile1 = root + '/' + root_work + '/' + output_file1
        ofile2 = root + '/' + root_work + '/' + output_file2

        print('Working on ' + root_work + '. ' + str(cnt) + ' out of ' + str(Na))

        A = torch.tensor(distan).float()
        xy = 100*torch.rand((N,2))
        xy.requires_grad = True

        optimizer = torch.optim.Adam([xy])



        print('Finding solution ...')
        for epoch in range(1000000):
            optimizer.zero_grad()
            loss = get_loss()
            loss.backward()
            optimizer.step()
        print('Solution found.')

        print(xy.detach().numpy())
        Y = pdist(xy.detach().numpy() ,'euclidean')
        Y = squareform(Y)
#           xy.detach().numpy()
        np.savetxt(ofile1, xy.detach().numpy(), fmt = '%6.1f')
        np.savetxt(ofile2,  Y,                  fmt = '%6.1f')
        print(' ')
        ofile3 = root + '/' + root_work + '/' + output_file3
        f      = open(ofile3,'w')
        cnt    = 0
        cumerr = 0
        f.write('i - j    Target    Inver   Diff   Error\n')
        print('\ni - j    Target    Inver   Diff   Error')

        for i in range(N):
            for j in range(i+1, N):
                log_line = str(i) + '-' + str(j) + '      ' + '{:5.2f}'.format(distan[i][j]) + '     ' + '{:5.2f}'.format(Y[i][j]) + '     ' + '{:5.2f}'.format(Y[i][j] - distan[i][j]) + '     ' +  '{:5.2f}'.format(np.abs(Y[i][j] - distan[i][j])*100/distan[i][j]) 
                f.write(log_line + '\n')
                print(log_line)
                cumerr += np.abs(Y[i][j] - distan[i][j])*100/distan[i][j]
                cnt    += 1
        f.write('Average error: ' + '{:5.2f}'.format(cumerr/cnt) + '\n')
        print('Average error: ' + '{:5.2f}'.format(cumerr/cnt) + '\n')
        print('Writting: ', ofile1)
        print('Writting: ', ofile2)
        f.close()
