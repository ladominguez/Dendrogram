from math import cos, sin, asin, sqrt
import numpy as np

latlon = {}
latlon['ARIG'] = np.array([ 18.2805, -100.3475])
latlon['DAIG'] = np.array([ 17.021305,-99.650691])
latlon['CRIG'] = np.array([ 16.736338,-99.131171])
latlon['CAIG'] = np.array([ 17.0478, -100.2673])
latlon['MMIG'] = np.array([ 18.2885, -103.3456])
latlon['MEIG'] = np.array([ 17.9249,  -99.6197])
latlon['OXIG'] = np.array([ 17.0726,  -96.7330])
latlon['PEIG'] = np.array([ 15.9986,  -97.1472])
latlon['PLIG'] = np.array([ 18.3923,  -99.5023])
latlon['PNIG'] = np.array([ 16.3923,  -98.1271])
latlon['TXIG'] = np.array([ 17.2532217, -97.7676667])
latlon['TLIG'] = np.array([ 17.5627,  -98.5665])
latlon['YOIG'] = np.array([ 16.8578,  -97.5459])
latlon['ZIIG'] = np.array([ 17.6067, -101.4650])
r       = 6371.0 # Radius of earth in kilometers. Use 3956 for miles
deg2rad = np.pi/180.0 

def great_circle_dist(lat_lon1, station):
        lat_lon2 = latlon[station]

        # haversine formula
        dlon = lat_lon2[1] - lat_lon1[1]
        dlat = lat_lon2[0] - lat_lon1[0]
        a = sin(deg2rad*dlat/2)**2 + cos(deg2rad*lat_lon1[0]) * cos(deg2rad*lat_lon2[0]) * sin(deg2rad*dlon/2)**2
        c = 2 * asin(sqrt(a))
        return c * r
