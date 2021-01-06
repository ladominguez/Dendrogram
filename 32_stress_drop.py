import obspy as ob
import numpy as np
import json, glob, os
from matplotlib import pyplot as plt
from scipy.signal import tukey
from mtspec import mtspec
from scipy.optimize import curve_fit
plt.rcParams.update({'font.size': 16})

fparam  = open('params.json')
fstress = open('stress.json')
stress  = json.load(fstress)
params  = json.load(fparam)
path    = os.path.join(params['root'],'sequence_*','raw')  

directories=glob.glob(path)
directories.sort()

dict_ylabel = {"DISP" : f"$m$", "VEL" : f"$m/s$", "ACC" : f"$m/s^2$"}
dict_title  = {"DISP" : "Displacement", "VEL" : "Velocity", "ACC" : "Acceleration"}

def G(r):
	R0 = 100e3
	if r <= R0:
		return 1./r
	else:
		return 1.0/(np.sqrt(R0*r))

def Q(f, azimuth):
	if ((azimuth >= 270) and (azimuth <= 330)) or ((azimuth >= 90) and (azimuth <= 1500)):
		return 175.0*np.power(f, 0.52) 
	else:
		return 211.0*np.power(f, 0.46)


for dir in directories:
	print(dir)
	sac = ob.read(os.path.join(dir,"*sac"))
	sta = set([tr.stats.sac.kstnm for tr in sac])
	sequence_id = dir.split('/')[-2]

	for count, station in enumerate(sta):
		print(count + 1, " - ", station)
		RESP_FILE = os.path.join(params['iresp'],station + '.RESP')
		sel = sac.select(station=station)
		if os.path.exists(RESP_FILE):
			inv = ob.read_inventory(RESP_FILE)
			sel.detrend()
			sel.taper(max_percentage=0.05)
			sel.remove_response(inventory=inv, output=stress["resp_type"],zero_mean=True, pre_filt=stress["pre_filt"], taper=True)
			
			date = {}
			Rij  = {}
			az   = {}
			dt   = {}
			mag  = {}
			
			# Plot waveforms
			waveform_out = os.path.join(dir,station + '.waveform.png')
			PS_out       = os.path.join(dir,station + '.' + stress["type_wave"] + '.png')
			FFT_out      = os.path.join(dir,station + '.FFT.png')
			SPEC_out     = os.path.join(dir,station + '.SPE.png')
			fig, ax = plt.subplots(len(sel),1, figsize = (12,6), sharex=True)
			for k, tr in enumerate(sel):
		
				date[k] = tr.stats.starttime.strftime("%Y/%m/%d,%H:%M:%S")
				Rij[k]  = np.sqrt(tr.stats.sac.dist**2+tr.stats.sac.evdp**2)*1e3
				dt[k]   = tr.stats.delta
				mag[k]  = tr.stats.sac.mag
				az[k]   = tr.stats.saz.az
				ax[k].plot(tr.times(),tr.data,'k',linewidth=0.25, label=date[k])
				ax[k].plot(tr.stats.sac.t5,0,'r*',markersize=15)
				#ax[k].plot(tr.stats.sac.t1,0,'b*',markersize=15)
				ax[k].grid()
				ax[k].legend(fontsize=14)
				ax[k].set_ylabel(dict_ylabel[stress["resp_type"]],fontsize=14)
				
			plt.suptitle(station + ' - ' + stress["resp_type"] + ' - ' + stress["type_wave"] + ' wave' ) 
			plt.subplots_adjust(hspace=0, wspace=0)
			plt.savefig(waveform_out)

			# Trim to p-wave
			d = {}
			fig, ax = plt.subplots(len(sel),1, figsize = (12,6), sharex=True)
			for k, tr in enumerate(sel):
				t     = tr.times()
				dt[k] = tr.stats.delta
				if stress["type_wave"] == 'P':
					twave = tr.stats.sac.t5
					k_sd  = 0.32   # Madariaga 1976 - See Sheare page 270     
				else:
					twave = tr.stats.sac.t5
					k_sd  = 0.21   # Madariaga 1976 - See Sheare page 270 
        
				tpn   = np.argmax(t >= twave)
				tbef  = stress["tbef"]
				Nfft  = stress["Nfft"]
				tnbef = int(np.floor(tbef/dt[k]))
				d[k]  = tr.data[tpn - tnbef:tpn - tnbef + Nfft] - np.mean(tr.data[tpn - tnbef:tpn - tnbef + Nfft])
				taper = tukey(Nfft, alpha=0.1)
				d[k]  = np.multiply(d[k],taper)
				ax[k].plot(np.linspace(-0.5,(Nfft-1)*dt[k]-0.5,Nfft),d[k],'k',linewidth=1, label=date[k])
				ax[k].legend(fontsize=14)
				ax[k].set_ylabel(dict_ylabel[stress["resp_type"]],fontsize=14)
				ax[k].plot(np.linspace(-0.5,(Nfft-1)*dt[k]-0.5,Nfft),taper*np.max(d[k]))
				ax[k].grid()

			plt.suptitle(station + ' - ' + stress["resp_type"] + ' - ' + stress["type_wave"] + ' wave' ) 
			plt.subplots_adjust(hspace=0, wspace=0)
			plt.savefig(PS_out)

			# Estimate the spectrum
			fmin = stress["fmin"]
			fmax = stress["fmax"]
			Aspec   = {}
			fspec   = {}

			fig, ax = plt.subplots(1,1, figsize = (12,6))
			for key, tr in d.items():
				spec, freq = mtspec(data=tr, delta=dt[key], time_bandwidth=3, nfft=len(tr))
				spec       = np.sqrt(spec/2)
				index      = np.where(np.logical_and(freq>=fmin, freq<=fmax))

				Aspec[key] = spec[index]
				fspec[key] = freq[index]

				ax.semilogy(fspec[key],Aspec[key],label=date[key] + ' Mw=' + str(mag[key]))

			ax.legend(fontsize=14)
			ax.grid(b=True, which='major', color='k', linestyle='--',linewidth=0.25)
			ax.grid(b=True, which='minor', color='k', linestyle='--',linewidth=0.25)
			plt.xlabel('Frequency [Hz]',fontsize=14)
			plt.title('Corrected spectrum - ' + station + ' - ' + dict_title[stress["resp_type"]], fontsize=14)
			plt.savefig(FFT_out)

			# Geometrical spreading
			Rad = 0.55         # Radiation pattern Boore and Boatwrigth
			F   = 2.0          # Free surface
			P   = 1/np.sqrt(2) # Energy partioning
			rho = 2700.0
			C   = Rad*F*P/(4*np.pi*(vel**3))

			Slog = {}

			if type_wave == 'P':
				vel = 3600*np.sqrt(3)
			else:
				vel = 3600

			fig, ax = plt.subplots(1,1, figsize = (12,6))
			S       = {}

			for key, An in Aspec.items():
				Slog[key] = np.log10(An) - np.log10(G(Rij[key]))
				            + 1.36*fspec[key]*Rij[key]/(vel*Q(fspec[key], baz))
							 - np.log10(C) 
				S[key] = 10**(Slog[key])
				ax.semilogy(fspec[key],S[key], label=date[key] )

			ax.legend(fontsize=14)
			ax.grid(b=True, which='major', color='k', linestyle='--',linewidth=0.25)
			ax.grid(b=True, which='minor', color='k', linestyle='--',linewidth=0.25)
			plt.xlabel('Frequency [Hz]',fontsize=14)
			plt.title('Spectrum - ' + station + ' - ' + dict_title[stress["resp_type"]], fontsize=14)





		else:
			print('Intrument response not found for station ', station, ' in sequence', sequence_id)
			

	
	exit()
