import obspy as ob
from obspy.core.utcdatetime import UTCDateTime
import numpy as np
import json
import glob
import os
from matplotlib import pyplot as plt
from scipy.signal import tukey
from mtspec import mtspec
from scipy.optimize import curve_fit
plt.rcParams.update({'font.size': 16})

fparam  = open('params.json')
fstress = open('stress.json')
stress  = json.load(fstress)
params  = json.load(fparam)
path    = os.path.join(params['root'], 'sequence_00001*', 'raw')

resp_type = stress["resp_type"]
type_wave = stress["type_wave"]
pre_filt  = stress["pre_filt"]
tbef      = stress["tbef"]
Nfft      = stress["Nfft"]
fmin      = stress["fmin"]
fmax      = stress["fmax"]

directories = glob.glob(path)
directories.sort()

dict_ylabel = {"DISP": f"$m$", "VEL": f"$m/s$", "ACC": f"$m/s^2$"}
dict_title  = {"DISP": "Displacement", "VEL": "Velocity", "ACC": "Acceleration"}
vel         = {"P": 6230, "S": 3600}

print("0. stress: ", stress)

def G(r):
	R0 = 100e3
	if r <= R0:
		return 1./r
	else:
		return 1.0/(np.sqrt(R0*r))


def Q(f, azimuth):
	if ((azimuth >= 270) and (azimuth <= 330)) or ((azimuth >= 90) and (azimuth <= 150)):
		return 175.0*np.power(f, 0.52)
	else:
		return 211.0*np.power(f, 0.46)

def M0_func(Mw):
	return np.power(10,Mw*1.5+9.1)



def stress_drop(freq_cut, kappa, vel_wave, Moment):
	return (7./16)*Moment*(freq_cut/(kappa*vel_wave))**3

#def brune_spectrum(f, fc, stress):
#	print('M0: ', M0)
#	if stress["resp_type"] == "DISP":
#		Sb = M0*(2*np.pi*f)/(1+(f/fc)**2)
#	elif stress["resp_type"] == "ACC":
#		Sb = M0*(2*np.pi*f)**2/(1+(f/fc)**2)
#	else:
#		None
#	return Sb

def get_reponse_files(dir_resp, station_name, t_start):
	if station_name.strip() == 'YOIG':
#		if   t_start >= UTCDateTime(2012,9,6)  and t_start < UTCDateTime(2014,6,20):
#			RESP_FILE = os.path.join(dir_resp, 'YOIG_IG_20120906_20140620.RESP')
		if t_start >= UTCDateTime(2014,6,20) and t_start < UTCDateTime(2014,9,3):
			RESP_FILE = os.path.join(dir_resp, 'YOIG_IG_20140620_20140903.RESP')
		elif t_start >= UTCDateTime(2014,9,3): 
			RESP_FILE = os.path.join(dir_resp, 'YOIG_IG_20140903_21001231.RESP')
		else:
			print('ERROR: No RESP file for ',station_name, ' at time: ', t_start )
			return None
	elif station_name.strip() == 'TXIG':
		if   t_start >= UTCDateTime(2012,9,3)  and t_start < UTCDateTime(2014,4,8):
			RESP_FILE = os.path.join(dir_resp, 'TXIG_IG_20120903_20140408.RESP')
		elif t_start >= UTCDateTime(2014,4,8)  and t_start < UTCDateTime(2014,6,21):
			RESP_FILE = os.path.join(dir_resp, 'TXIG_IG_20140408_20140621.RESP')
		elif t_start >= UTCDateTime(2014,6,21) and t_start < UTCDateTime(2015,8,6): 
			RESP_FILE = os.path.join(dir_resp, 'TXIG_IG_20140621_20150806.RESP')
		else:
			print('ERROR: No RESP file for ',station_name, ' at time: ', t_start )
			return None
	else:
		RESP_FILE = os.path.join(dir_resp, station_name + '.RESP')
	return RESP_FILE

def brune_log(f, log_M0, fc ):
	if resp_type == "DISP":
		Sb_log = log_M0-np.log10((1+(f/fc)**2))
	elif resp_type == "VEL":
   		Sb_log = log_M0+np.log10(2*np.pi*f)-np.log10(1+(f/fc)**2)
	elif resp_type == "ACC":
		Sb_log = log_M0+2*np.log10(2*np.pi*f)-np.log10(1+(f/fc)**2)
	else:
 		None

	return Sb_log

def clean_directory(dir):
	previous = glob.glob(os.path.join(dir, "*.png"))
	for png_file in previous:
		os.remove(png_file)
	

for dir in directories:
	print(dir)
	sac = ob.read(os.path.join(dir, "*sac"))
	sta = set([tr.stats.sac.kstnm     for tr in sac])
	sta = sorted(sta)
	clean_directory(dir)
	sequence_id = dir.split('/')[-2]
	Data_out    = os.path.join(dir, sequence_id + '.stress_drop.' + resp_type + '.dat')
	fout        = open(Data_out, 'w')

	fout.write('Station  Wave    Type      date_time           mag   distance    fcut   std_fcut    Mcorr std_Mcorr strees_drop    ID \n')
	for count, station in enumerate(sta):
		print(count + 1, " - ", station)
		sel = sac.select(station=station)
		#if True: #os.path.exists(RESP_FILE):
		sel.detrend()
		sel.taper(max_percentage=0.05)

		tp_wave = np.zeros((len(sel),1))
		Invalid = False
		for k in range(len(sel)):
			RESP_FILE = get_reponse_files(params['iresp'], station, sel[k].stats.starttime)
			if RESP_FILE is None:
				Invalid = True
				continue
			inv = ob.read_inventory(RESP_FILE)
			sel[k].remove_response(inventory=inv, output=resp_type, zero_mean=True, pre_filt=pre_filt, taper=True)
			tp_wave[k] = sel[k].stats.sac.t5

		if Invalid:
			continue

		date  = {}
		Rij   = {}
		az    = {}
		dt    = {}
		mag   = {}


		# Plot waveforms
		waveform_out = os.path.join(dir, station + '.waveform.png')
		PS_out       = os.path.join(dir, station + '.' + type_wave + '.png')
		FFT_out      = os.path.join(dir, station + '.FFT.png')
		SPEC_out     = os.path.join(dir, station + '.SPE.png')
		Brune_out    = os.path.join(dir, station + '.BRUNE.png')

		fig, ax = plt.subplots(len(sel), 1, figsize=(12, 6), sharex=True , squeeze=False)
		ax = ax.flatten()
		for k, tr in enumerate(sel):

			date[k] = tr.stats.starttime.strftime("%Y/%m/%d,%H:%M:%S")
			Rij[k]  = np.sqrt(tr.stats.sac.dist**2+tr.stats.sac.evdp**2)*1e3
			dt[k]   = tr.stats.delta
			mag[k]  = tr.stats.sac.mag
			az[k]   = tr.stats.sac.az
			ax[k].plot(tr.times(), tr.data, 'k', linewidth=0.25, label=date[k])
			ax[k].plot(tr.stats.sac.t5, 0, 'r*', markersize=15)
				# ax[k].plot(tr.stats.sac.t1,0,'b*',markersize=15)
			ax[k].grid()
			ax[k].legend(fontsize=14)
			ax[k].set_ylabel(dict_ylabel[resp_type], fontsize=14)
			ax[k].set_xlim([0,np.ceil(tp_wave.max()*3/5)*5])


		plt.suptitle(station + ' - ' + resp_type + ' - ' + type_wave + ' wave')
		plt.subplots_adjust(hspace=0, wspace=0)
		plt.savefig(waveform_out)
		plt.close()

		# Trim to p-wave
		d = {}
		fig, ax = plt.subplots(len(sel), 1, figsize=(12, 6), sharex=True, squeeze=False )
		ax      = ax.flatten()
		for k, tr in enumerate(sel):
			t = tr.times() + tr.stats.sac.b
			dt[k] = tr.stats.delta
			if type_wave == 'P':
				twave = tr.stats.sac.t5
				k_sd = 0.32   # Madariaga 1976 - See Sheare page 270
			else:
				twave = tr.stats.sac.t5
				k_sd = 0.21   # Madariaga 1976 - See Sheare page 270

			tpn = np.argmax(t >= twave)
			tnbef = int(np.floor(tbef/dt[k]))
			d[k] = tr.data[tpn - tnbef:tpn - tnbef + Nfft] - \
			    np.mean(tr.data[tpn - tnbef:tpn - tnbef + Nfft])
			taper = tukey(Nfft, alpha=0.1)
			d[k]  = np.multiply(d[k], taper)
			ax[k].plot(np.linspace(-0.5, (Nfft-1)*dt[k]-0.5, Nfft),
			           d[k], 'k', linewidth=1, label=date[k])
			ax[k].legend(fontsize=14)
			ax[k].set_ylabel(dict_ylabel[resp_type], fontsize=14)
			ax[k].plot(np.linspace(-0.5, (Nfft-1)*dt[k]-0.5, Nfft), taper*np.max(d[k]))
			ax[k].grid()

		plt.suptitle(station + ' - ' + resp_type + ' - ' + type_wave + ' wave')
		plt.subplots_adjust(hspace=0, wspace=0)
		plt.savefig(PS_out)
		plt.close()

		# Estimate the spectrum
		Aspec = {}
		fspec = {}

		fig, ax = plt.subplots(1, 1, figsize=(12, 6))
		for key, tr in d.items():
			spec, freq = mtspec(data=tr, delta=dt[key], time_bandwidth=3, nfft=len(tr))
			spec = np.sqrt(spec/2)
			index = np.where(np.logical_and(freq >= fmin, freq <= fmax))

			Aspec[key] = spec[index]
			fspec[key] = freq[index]

			ax.semilogy(fspec[key], Aspec[key],
			            label=date[key] + ' Mw=' + str(mag[key]))

		ax.legend(fontsize=14)
		ax.grid(b=True, which='major', color='k', linestyle='--', linewidth=0.25)
		ax.grid(b=True, which='minor', color='k', linestyle='--', linewidth=0.25)
		plt.xlabel('Frequency [Hz]', fontsize=14)
		plt.title('Corrected spectrum - ' + station + ' - ' +
		          dict_title[resp_type], fontsize=14)
		plt.savefig(FFT_out)
		plt.close()

		# Geometrical spreading
		Rad = 0.55         # Radiation pattern Boore and Boatwrigth
		F   = 2.0          # Free surface
		P   = 1/np.sqrt(2)  # Energy partioning
		rho = 2700.0
		C   = Rad*F*P/(4*np.pi*(vel[type_wave]**3))

		Slog = {}

		fig, ax = plt.subplots(1, 1, figsize=(12, 6))
		S = {}

		for key, An in Aspec.items():
			Slog[key] = np.log10(An) - np.log10(G(Rij[key])) + 1.36*fspec[key] * \
			                     Rij[key]/(vel[type_wave] *
			                               Q(fspec[key], az[key])) - np.log10(C)
			S[key] = 10**(Slog[key])
			ax.semilogy(fspec[key], S[key], label=date[key])

		ax.legend(fontsize=14)
		ax.grid(b=True, which='major', color='k', linestyle='--', linewidth=0.25)
		ax.grid(b=True, which='minor', color='k', linestyle='--', linewidth=0.25)
		plt.xlabel('Frequency [Hz]', fontsize=14)
		plt.title('Spectrum - ' + station + ' - ' +
		          dict_title[resp_type], fontsize=14)
		plt.savefig(SPEC_out)
		plt.close()

		fcut   = {}
		fcuts  = {}
		Mcorr  = {}
		Mcorrs = {}
		stress = {}

		fig, ax = plt.subplots(2,1, figsize = (10,8))
		for key, fb in fspec.items():
		    M0 = M0_func(mag[key])
		    ax[0].semilogy(fspec[key],S[key], label=date[key] )
		    ax[1].plot(fspec[key],np.log10(S[key]), label=date[key] )
		    popt, pcov  = curve_fit(brune_log, fspec[key],np.log10(S[key]), bounds=(0,[20, fmax]), maxfev=1000)
		    errors      = np.sqrt(np.diag((pcov)))
		    fcut[key]   = popt[1]
		    fcuts[key]  = errors[0]
		    Mcorr[key]  = popt[0]
		    Mcorrs[key] = errors[1] 
		    stress[key] = stress_drop(fcut[key], k_sd, vel[type_wave], M0)/1e6

		plt.gca().set_prop_cycle(None)
		for key, fb in fspec.items():
		    M0 = M0_func(mag[key])
		    ax[1].plot(fb, brune_log(fb,  Mcorr[key], fcut[key]),'o-')
		    #print('fcut')
		    print('fcut[', key,']: ', '%5.2f'%fcut[key], ' Mcorr[', key, ']: ', '%5.2f'%Mcorr[key], 
			' Stress drop[', key, ']: ', '%5.2f'%stress[key], 'MPa')
		    fout.write(station + '       ' + type_wave + '     ' + resp_type + '    ' + date[key] + '    ' + '%3.1f'%mag[key]  
				+ '    ' + '%6.1f'%(Rij[key]/1e3) + '    ' + '%5.2f'%fcut[key] + '    ' + '%6.3f'%fcuts[key]  + '    '
				+ '%5.2f'%Mcorr[key] + '    ' + '%6.3f'%Mcorrs[key]  + '    '
				+ '%6.2f'%stress[key]  + '    ' + sequence_id.split('_')[1] + '\n')

		ax[0].grid(b=True, which='major', color='k', linestyle='--',linewidth=0.25)
		ax[0].grid(b=True, which='minor', color='k', linestyle='--',linewidth=0.25)  
		ax[1].grid(b=True, which='major', color='k', linestyle='--',linewidth=0.25)
		ax[1].grid(b=True, which='minor', color='k', linestyle='--',linewidth=0.25)  
		plt.suptitle('Brune Spectrum ' + dict_title[resp_type] + ' - ' + station 
			+ '- fc = ' + '%5.2f'%fcut[key] + 'Hz ' + ' Stress Drop = ' + '%5.2f'%stress[key] + 'MPa', fontsize=17)
		plt.xlabel('Frequency [Hz]',fontsize=14)
		plt.savefig(Brune_out)
		plt.close()
			

			
	fout.close()
	
