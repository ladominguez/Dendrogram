import numpy as np
def jul2mmdd(year,jday):
	if (year%4) == 0:
		days = np.array([1, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
	else:
		days = np.array([1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])

	cdays = np.cumsum(days) 
	mm    = np.where(cdays <= jday)[0][-1]
	
	dd = jday - cdays[mm] + 1
	mm = mm + 1
	return (mm,dd)
	
