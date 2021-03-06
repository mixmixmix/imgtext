import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import numpy as np
import datetime


#fdir = pd.read_csv('input/flowdirchange21.csv')
fdir = pd.read_csv('input/fchangeoct5.csv')
fdir['chid'] = fdir.index
fdir['datetime'] = pd.to_datetime(fdir['datetime'])
fdir['switch_time'] = fdir['datetime']
fdir = fdir.set_index(['datetime'])

#fdir = fdir[fdir.index>'23-03-2021 15:24:40']

fval = pd.read_csv('input/5oct.csv')
fval['date'] = pd.to_datetime(fval['date'])

fval = fval.set_index(['date'])
fval = fval.sort_index()

fval_sec = fval['flow_v'].resample('S').median() # often we'd have a reading with wrong first digit popping up, but it is unlikely to be the most commond reading in a given second

fval_believe = fval_sec.rolling(window=5).mean() #5 second rolling average



flocs = pd.read_csv('input/flowmeterlocs21.csv')
flocs['datetime'] = pd.to_datetime(flocs['datetime'])
flocs = flocs.set_index(['datetime'])
flocs = flocs.sort_index()


fdl = pd.merge(flocs, fdir, on='loc_name', how='outer')
fdl  = fdl.dropna(subset=[' flow_dir'])


#this will require manual corrections
# fdl[fdl['chid'].duplicated(keep=False)]
fdl.to_csv('input/fdl5.csv', index = False)

#x = -1*fval_sec
#peaks, _ = find_peaks(x, height=-5, distance = 10) #unit is seconds
#plt.plot(fval_believe, linestyle='-')
#plt.plot(x.iloc[peaks].index, -x.iloc[peaks], "x")
#plt.plot(fval_sec, color='k')
## plt.plot(np.zeros_like(x), "--", color="gray")
#print(len(x.iloc[peaks]))
#pd.DataFrame(x.iloc[peaks].index).to_csv('crosszero5in.csv', index=False)
#plt.show()
#finding the cropssing point is a bit difficult (should I use fval_beleive of fval_sec? But near that point values are near zero regardless of the sign. However it matters for timing.

fdl['fs']=fdl.apply(lambda x: 'low' if x['switch_time']< datetime.datetime(2021,5,21,14,38,36) else 'high', axis=1)

vx = []
for ind, val in fdl.iterrows():
    if val['loc_x']<0:
        vx.append(2.79+val['loc_x'])
    else:
        vx.append(val['loc_x'])

fdl['loc_x'] = vx


fcross = pd.read_csv('input/crosszero5.csv')
fcross['date'] = pd.to_datetime(fcross['date'])
fcl = pd.merge_asof(fcross, fdl, left_on='date', right_on='switch_time', direction='backward')
fcl.columns = ['cross_time', 'loc_name', 'loc_x','loc_y','flow_dir','chid','switch_time','fs']
fcl.to_csv('input/switchcross5.csv',index=False)

#TODO
#switch profile sign on the crosszero point


#TODO 1
#iterate through direction time change to prepare
# 1 a snapshot of flow profile at given point
# 2 value of the location
#low flow get 4 min, high flo get 2.5 min

alldf = dict()


for ind, val in fcl.iterrows():
    #print(fval[ind])
    cti = fval_believe.loc[pd.date_range(start=(val['switch_time'] - datetime.timedelta(0,10)),end=(val['switch_time']+datetime.timedelta(0,150)), freq='1S')]

    cttrue = cti.reset_index().apply(lambda x: -1*x['flow_v']*val['flow_dir'] if x['index'] < val['cross_time'] else x['flow_v']*val['flow_dir'],axis=1)

    alldf[val['loc_name']]=cttrue
    # cti = flocs[ind]
    # print(cti)



# same bottom middle point in gamma and beta
#y, -1.5782373878106757,1.0403632692654063
#h, 1.2118941796790834,0.9947650093408434

