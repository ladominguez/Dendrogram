#!/bin/python

import yaml, glob
import numpy as np
from scipy.spatial.distance import pdist, squareform

# From M. Raggi - START
from differential_evolution import *
from timer import Timer
import torch.nn.functional as F
import torch.nn as nn
import argparse
from functools import partial
# END
 
#params   = yaml.load(open('params.yaml','r').read(),Loader=yaml.FullLoader)
#root     = params['root']

root         = '/mnt/data01/antonio/Dropbox/BSL/CRSMEX/Dendrograms/2020AGO07/sequence_xc9500_coh9500'
output_file1 = 'inversion.dat'
output_file2 = 'inverted.matrix.dat'
output_file3 = 'inverted.matrix.error'

def pairwise_dist_sq(P,Q):
    # P.shape = (batch, m, 2)
    # Q.shape = (batch, n, 2)
    # result.shape = (batch, m, n)
    P = P[...,None,:] # (batch, m, 1, 2)
    Q = Q[...,None,:,:] # (batch, 1, n, 2)
    R = P-Q
    R *= R
    return R.sum(dim=-1)

def pairwise_dist2_batch(x):
    return pairwise_dist_sq(x,x)

def l1_batch(x,A,smooth=False):
    D = torch.abs(pairwise_dist2_batch(x)-A)
    if smooth:
        smalls = D[D<1.0]
        D[D<1.0] =  smalls**2 # smooth L1
    return torch.mean(D,dim=(1,2))

def l2_batch(x,A):
    D = pairwise_dist2_batch(x)-A
    return torch.mean(D*D,dim=(1,2))

def clamp(x):
    #x -= x.mean(dim=0)*0.9
    mask = (x > 4.0) + (x < -4.0)
    x[mask] = torch.randn_like(x[mask])*2
    return x



def get_loss():
    loss = 0.
    for i in range(N):
        for j in range(i+1,N):
            loss += torch.abs(torch.sum((xy[i]-xy[j])**2)-A[i,j]**2)
    return loss

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
#    parser.add_argument('matrix',type=str, help="file with (symmetric) distance matrix")

    parser.add_argument("-t","--time", type=float, default=32, help="Number of seconds to spend finding a good solution (per restart)")
    parser.add_argument("-n","--num_restarts", type=int, default=8, help="Number of times that we try to restart")
    parser.add_argument("-e","--error", type=str, default="L2", help="either use L1, L2, or smoothL1")
    parser.add_argument("-p","--pop_size", type=int, default=64, help="Population size for diff evo")

    parser.add_argument("-c","--try_with_cuda", type=str, default="false", help="Use cuda (if available)")

    args = parser.parse_args()
    use_cuda = torch.cuda.is_available() if args.try_with_cuda.lower() == "true" else False

    errstr = args.error.lower()
    if errstr == 'l2':
        error_func = l2_batch
    elif errstr == 'l1':
        error_func = partial(l1_batch,smooth=False)
    else:
        error_func = partial(l1_batch,smooth=True)


    files1 = glob.glob(root + '/sequence_*/matrix.dist.dat')
    files2 = glob.glob(root + '/sequence_*/SEQ*/matrix.dist.dat')

    files1.sort()
    files2.sort()

    files_all = files1 + files2

    Nf     = len(files1)
    Na     = len(files_all)

    print('Number of matrix files: ', len(files_all))

    cnt = 0
    for file in files_all:
        cnt    = cnt + 1
        D      = torch.tensor(np.loadtxt(file, delimiter=" ")).double()
        N      = D.shape[0]
        distan = np.loadtxt(file, delimiter=" ")

        if N >= 3:
                if cnt > Nf:
                    root_work = file.split('/')[-3] + '/' + file.split('/')[-2]
                else:
                    root_work = file.split('/')[-2]
                ofile1 = root + '/' + root_work + '/' + output_file1
                ofile2 = root + '/' + root_work + '/' + output_file2

                print('Working on ' + root_work + '. ' + str(cnt) + ' out of ' + str(Na))

                scale = D.max()/2
                M = D/scale
                A = (M*M)[None]

                best_x    = None
                best_cost = 1e15

                print('Finding solution ...')
                for epoch in range(args.num_restarts):
                    print(f"\n\n Epoch {epoch+1}/{args.num_restarts}:")
                    initial_pop = 2*torch.randn(args.pop_size, A.shape[1], 2).double()

                    if epoch > 0: initial_pop[0] = best_x

                    loss, x = optimize(lambda x: error_func(x,A),
                            initial_pop=initial_pop,
                            use_cuda=use_cuda,
                            mut=(0.1,0.9),crossp=(0.3,0.7),
                            proj_to_domain=clamp,
                            prob_choosing_method='auto')

                    if loss < best_cost:
                        best_cost = loss
                        best_x = x

                print('Solution found.')

                x  = best_x
                x  = x.cpu()
                dx = torch.sqrt(pairwise_dist2_batch(x[None])).squeeze()

                x  *= scale
                dx *= scale


                diff = D - dx
                error = torch.mean(torch.abs(diff)).item()
                np.set_printoptions(precision=6, suppress=True, linewidth=10000, floatmode='maxprec_equal')
                print(x.detach().numpy())
                Y = pdist(x.detach().numpy() ,'euclidean')
                Y = squareform(Y)
#		xy.detach().numpy()
                np.savetxt(ofile1,  x.detach().numpy(), fmt = '%6.1f')
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
