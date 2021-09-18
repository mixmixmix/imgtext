import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import numpy as np
import datetime


fdir = pd.read_csv('input/flowdirchange21.csv')
fdir['chid'] = fdir.index
fdir['datetime'] = pd.to_datetime(fdir['datetime'])
fdir['switch_time'] = fdir['datetime']
fdir = fdir.set_index(['datetime'])

#fdir = fdir[fdir.index>'23-03-2021 15:24:40']

fval = pd.read_csv('input/flowvalchange.csv')
fval['date'] = pd.to_datetime(fval['date'])

fval = fval.set_index(['date'])
fval = fval.sort_index()

fval_sec = fval['flow_v'].resample('S').median() # often we'd have a reading with wrong first digit popping up, but it is unlikely to be the most commond reading in a given second

fval_believe = fval_sec.rolling(window=5).mean() #5 second rolling average



flocs = pd.read_csv('input/flowmeterlocs21.csv')
flocs['datetime'] = pd.to_datetime(flocs['datetime'])
flocs = flocs.set_index(['datetime'])
flocs = flocs.sort_index()


fdl = pd.merge_asof(flocs, fdir, left_index=True, right_index=True, direction='nearest')

#this will require manual corrections
fdl[fdl['chid'].duplicated(keep=False)]
fdl.to_csv('input/fdl.csv', index = False)

# x = -1*fval_believe
# peaks, _ = find_peaks(x, height=-1, distance = 20) #unit is seconds
# plt.plot(fval_believe, linestyle='-')
# plt.plot(x.iloc[peaks].index, -x.iloc[peaks], "x")
# plt.plot(fval_sec, color='k')
# # plt.plot(np.zeros_like(x), "--", color="gray")
# plt.show()

fcross = pd.read_csv('input/crosszero.csv')
fcross['date'] = pd.to_datetime(fcross['date'])
fcl = pd.merge_asof(fcross, fdl, left_on='date', right_on='switch_time', direction='backward')
fcl.columns = ['cross_time', 'loc_name', 'loc_x','loc_y','flow_dir','chid','switch_time']
fcl.to_csv('input/switchcross.csv',index=False)

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
    alldf[val['loc_name']]=cti
    # cti = flocs[ind]
    # print(cti)


# same bottom middle point in gamma and beta
#y, -1.5782373878106757,1.0403632692654063
#h, 1.2118941796790834,0.9947650093408434

