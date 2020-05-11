import glob, os
import numpy                 as np
import matplotlib.pyplot     as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance  import squareform
from matplotlib              import gridspec
from greatcircle             import great_circle_dist as gc

min_members  = 1
directories  = glob.glob("/Users/antonio/Dropbox/BSL/CRSMEX/Dendrograms/2020MAR27/sequence_xc9500_coh9500/sequence_*/")
fileout      = 'matrix.dist.dat'
filedist     = 'locmag_mean.dat'
input_file   = 'merge.correli.dat'

print("Num. directories = ", len(directories))
directories.sort()
plt.rc('ytick', labelsize=14)
locmag_file     = 'locmag_mean.dat'
ds_lim          = 100e6
file_decluster = 'decluster.dat'
deg2rad        = np.pi/180.0
output_file    = 'dendrogram.png'

def distance2cluster(station):
    #print('STATION: ',station)
    
    latlon_cluster = np.genfromtxt(filedist, usecols=(1, 2), dtype = float)
    A=gc(latlon_cluster, station)
    return gc(latlon_cluster, station)

def my_squareform(filename):
    i_ind = np.array(np.genfromtxt(filename,usecols=0,dtype=int  ).transpose())
    j_ind = np.array(np.genfromtxt(filename,usecols=1,dtype=int  ).transpose())
    fval  = np.array(np.genfromtxt(filename,usecols=2,dtype=float).transpose())
    sta   = np.array(np.genfromtxt(filename,usecols=4,dtype='U4',autostrip=True ).transpose())
    ind   = np.array([i_ind, j_ind]).transpose()
    ndim  = np.max(ind)
    fout  = np.zeros((ndim,ndim))
    distm = np.ones( (ndim,ndim))*1e6 # Set minimum distance to an arbitrary large number
    nnum  = fval.size

    for k in range(fval.size):
        if nnum == 1: # This if is needed since the code files when trying to indexing a 1 element array
            fout[i_ind -1][j_ind -1] = fval
            fout[j_ind -1][i_ind -1] = fval
        else:
            dist = distance2cluster(sta[k])
            if dist < distm[i_ind[k] -1][j_ind[k] -1]:
                fout[ i_ind[k] -1][j_ind[k] -1] = fval[k]
                fout[ j_ind[k] -1][i_ind[k] -1] = fval[k]
                distm[i_ind[k] -1][j_ind[k] -1] = dist
    i_nan = np.isnan(fout)
    fout[i_nan] = 0.0
    return fout




for dir in directories:
    # For testing use the following directory
    # dir='/home/u2/antonio/CRSMEX/Dendrograms/2015JUN10/sequences_xc9500_coh9500/sequence_084_N07'
    os.chdir(dir)
    print("Directory ", dir)
        # Removing previus files    
    previous = glob.glob("*dendrogram.png")
    for file in previous:
        os.remove(file)
    fout_pre = glob.glob(fileout)
    for file in fout_pre:
        os.remove(file)
    fout_dec = glob.glob(file_decluster)
    for file in fout_dec:
        os.remove(file)
    
    fsta      = open("station_ids.info")
    stations  = fsta.read().splitlines()
    Nsta      = len(stations)
    fids      = open("unique_member_id.info")
    u_ids     = fids.read().splitlines()
    eq_id     = list()
    mag       = np.genfromtxt(locmag_file, usecols=3, dtype=float)

    counter   = 0
    for id in u_ids:
        counter = counter + 1    
        eq_id.extend([id + "." + "{:02d}".format(counter)])
    eq_ids=tuple(eq_id)

    if os.stat(input_file).st_size == 0:
        print("No data found.")
        continue
    print("Reading ", input_file)

        # /* DRLA
    #try:
    #    events = np.genfromtxt(input_file, usecols=0,dtype='S')
    #    distan = np.genfromtxt(input_file, usecols=2,dtype=float)
    #except:
    #    print("Couldnt open file ", input_file)
    #    break
    # */ DRLA

    #N = distan.size
    N = 1
    print("Nsta = ", Nsta)
    r_max = np.zeros(3)    
    if N >= min_members:
        # /* DRLA
        #sac_files = glob.glob('SYN*' + sta + '*.sac')
        #for sac in sac_files:
        #    print(sac)
        #    eq_id.extend([sac.split('.')[9] + '.' + sac.split('.')[10]])
    
        #if distan.size == 1: # This avoids an error when a single value is present. Only two repeaters within the sequence
        #    distan=np.array([distan.astype(float)])            
        #Y=squareform(distan)

        Yout = my_squareform(input_file)    
        Ycon = squareform(Yout)             # Get condense matrix
        np.savetxt(fileout,Yout,'%.2f')
        Y  = np.genfromtxt(input_file, usecols=2, dtype=float)
        #Z = linkage(distan,method='single')
        Z = linkage(Ycon,method='single')
        print(Z.shape)
        #Z[:,2] = Z[:,2]*(1/np.sqrt(2))
        print(Z)
        fig = plt.figure(figsize=(6, 10), dpi=120)
        ax = fig.add_axes([0,0,1,1])

        gs  = gridspec.GridSpec(2,2 , height_ratios=[5, 1])
        #plt.subplot(211)
        ax0 = plt.subplot(gs[0,:])
        dendrogram(Z,leaf_rotation=90.,leaf_font_size=16., labels=eq_ids)
        #dendrogram(Z,leaf_rotation=90.,leaf_font_size=16.)
        ds_lim   = [1e6, 10e6, 100e6]
        r_max[0] = np.power((7/16)*(np.power(10.0,1.5*mag + 9.1)/ds_lim[0]),1.0/3)    
        r_max[1] = np.power((7/16)*(np.power(10.0,1.5*mag + 9.1)/ds_lim[1]),1.0/3)    
        r_max[2] = np.power((7/16)*(np.power(10.0,1.5*mag + 9.1)/ds_lim[2]),1.0/3)    
        print('mag   = ', mag,)
        print('Y_max = ', np.max(Z[:,2]))
        
        if r_max[2] <= np.max(Z[:,2]):
            plt.axhline(y=r_max[0],linewidth=4, color='r')
            plt.axhline(y=r_max[1],linewidth=4, color='r')
            plt.axhline(y=r_max[2],linewidth=4, color='r')
            np.savetxt(file_decluster,Z,'%.2f')
        xlimits = plt.gca().get_xlim()
        ylimits = plt.gca().get_ylim()
        print('xlim: ',xlimits)
        m = 0
        for rt in r_max:
            if rt < ylimits[1]:
                plt.text(0.65*xlimits[1], 1.025*rt,r'$\Delta\sigma=\,$' + str(int(np.round(ds_lim[m]/1e6))) + r'$\,MPa$',fontsize=16)
                plt.text(0, 1.025*rt,r'$r_{max}=$' + str(int(np.round(rt))) + r'$\,m$',fontsize=18)
            m = m + 1
        #plt.text(0.65*xlimits[1], 1.025*r_max[1],r'$\Delta\sigma=\,$' + str(int(np.round(ds_lim[1]/1e6))) + r'$\,MPa$',fontsize=16)
        #plt.text(0, 1.025*r_max[1],r'$r_{max}=$' + str(int(np.round(r_max[1]))) + r'$\,m$',fontsize=18)
        #plt.text(0.65*xlimits[1], 1.025*r_max[2],r'$\Delta\sigma=\,$' + str(int(np.round(ds_lim[2]/1e6))) + r'$\,MPa$',fontsize=16)
        #plt.text(0, 1.025*r_max[2],r'$r_{max}=$' + str(int(np.round(r_max[2]))) + r'$\,m$',fontsize=18)
        plt.xlabel('Earthquake id . Member Id', fontsize=16)
        plt.ylabel('Relative Distance [m]',     fontsize=16)
        #plt.title(dir.split('/')[-2] + ' - ' +sta)
        plt.title('Detected by: ' + ', '.join(stations), fontsize=18)
        #filename_fig = dir.split('/')[-2] + '.' + sta + '.dendrogram.png'
        filename_fig = dir.split('/')[-2] + '.'  + output_file
        
        print("Creating figure ", filename_fig)
        plt.savefig(filename_fig)
        plt.close("all")
        del Y
        del Z
        del Ycon
        del Yout
        
    #DRLA del events
    #DRLA del distan
    exit
    os.chdir("../")

