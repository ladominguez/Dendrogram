import glob, yaml, os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg


plt.rcParams.update({'figure.figsize': (30,40)})
plt.rcParams.update({'font.size': 28})
plt.matplotlib.use('Agg')
params      = yaml.load(open('params.yaml','r').read(),Loader=yaml.FullLoader)
root        = params['root']
ds_lim      = float(params['ds_max'])
directories = glob.glob(root + '/sequence_*/')
directories.sort()
input1      = 'locmag.dat'
input2      = 'matrix.dist.dat'
input3      = 'inversion.dat'
input4      = 'inverted.matrix.dat'
def my_circle(pos, r):
    theta=np.linspace(0,2*np.pi, 101)
    x    = r*np.cos(theta) + pos[0]
    y    = r*np.sin(theta) + pos[1]
    
    return (x, y)

ds_lim = [1e6, 10e6, 100e6];
for dir in directories:

    plt.figure(num=None, figsize=(12, 12), dpi=400, facecolor='w', edgecolor='k')
    fig, ax = plt.subplots(2,2)
    os.chdir(dir)
    outputfig = dir.split('/')[-2] + '.rupture.circle.png'
    print(dir)
    mag = np.genfromtxt(input1, usecols=(5)  )
    loc = np.genfromtxt(input2, usecols=(0,1))
    xc  = loc[0][:]
    k   = 0
    j   = 0
    row = 0
    for ds in ds_lim:
        #plt.subplot(2,2,j)
        for pos in loc:
            #plt.subplot(2,2,j)
            ax[int(j/2)][j%2].plot(pos[0],pos[1],marker='D',markersize=20)
            r = np.power((7/16)*(np.power(10.0,1.5*mag[k] + 9.1)/ds),1.0/3)
            k = k + 1
            xc, yc = my_circle(pos, r)
            ax[int(j/2)][j%2].plot(xc, yc, linewidth=4)
        if j == 0:
            ylimit = ax[int(j/2)][j%2].get_ylim()
            xlimit = ax[int(j/2)][j%2].get_xlim()
            print(xlimit)
        else:
            ax[int(j/2)][j%2].set_ylim(ylimit)
            ax[int(j/2)][j%2].set_xlim(xlimit)
        
        ax[int(j/2)][j%2].grid('on')
        ax[int(j/2)][j%2].set_xlabel('X [m]',fontsize=28)
        ax[int(j/2)][j%2].set_ylabel('Y [m]',fontsize=28)
        ax[int(j/2)][j%2].set_title(r'$\Delta\sigma$=' +str(ds/1e6) + 'MPa')
        ax[int(j/2)][j%2].set_aspect('equal', adjustable='box')
        j = j + 1
        k = 0
    img = mpimg.imread(dir + dir.split('/')[-2] + '.dendrogram.png')
    #plt.subplot(2,2,4)
    ax[1][1].imshow(img)
    ax[1][1].axis('off')
    plt.tight_layout()    
    plt.savefig(outputfig)
    plt.close()
        

