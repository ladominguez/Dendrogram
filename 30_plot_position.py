import glob, yaml, os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg


plt.rcParams.update({'figure.figsize': (30,30)})
plt.matplotlib.use('Agg')
params      = yaml.load(open('params.yaml','r').read())#,Loader=yaml.FullLoader)
root        = params['root']
ds_lim      = float(params['ds_max'])
directories = glob.glob(root + '/sequence_00413*/')
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
    os.chdir(dir)
    outputfig = dir.split('/')[-2] + '.rupture.circle.pdf'
    print(dir)
    mag = np.genfromtxt(input1, usecols=(5)  )
    loc = np.genfromtxt(input2, usecols=(0,1))
    xc = loc[0][:]
    k  = 0
    j  = 1
    for ds in ds_lim:
        plt.subplot(2,2,j)
        for pos in loc:
            plt.subplot(2,2,j)
            plt.plot(pos[0],pos[1],marker='D')
            r = np.power((7/16)*(np.power(10.0,1.5*mag[k] + 9.1)/ds),1.0/3)
            k = k + 1
            xc, yc = my_circle(pos, r)
            plt.plot(xc, yc)
        if j == 1:
            ylimit = plt.gca().get_ylim()
            xlimit = plt.gca().get_xlim()
            print(xlimit)
        else:
            plt.gca().set_ylim(ylimit)
            plt.gca().set_xlim(xlimit)
        
        plt.grid('on')
        plt.xlabel('X [m]',FontSize=18)
        plt.ylabel('Y [m]',FontSize=18)
        plt.title(r'$\Delta\sigma$=' +str(ds/1e6) + 'MPa')
        plt.gca().set_aspect('equal', adjustable='box')
        j = j + 1
        k = 0
    img = mpimg.imread(dir + dir.split('/')[-2] + '.dendrogram.png')
    plt.subplot(2,2,4)
    plt.imshow(img)
    plt.axis('off')
    plt.savefig(outputfig)
    plt.close()
        

