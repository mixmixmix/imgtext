import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import numpy as np



fdir = pd.read_csv('input/flowdirchange21.csv')
fdir['chid'] = fdir.index
fdir['datetime'] = pd.to_datetime(fdir['datetime'])
fdir['switch_time'] = fdir['datetime']
fdir = fdir.set_index(['datetime'])

fdir = fdir[fdir.index>'23-03-2021 15:24:40']

fval = pd.read_csv('input/flowvalchange.csv')
fval['datetime'] = pd.to_datetime(fval['date'])

fval = fval.set_index(['datetime'])
fval_sec = fval['flow_v'].resample('S').mean()
fval_believe = fval_sec.rolling(window=5).mean() #5 second rolling average
x = -1*fval_sec
peaks, _ = find_peaks(x, height=-4, distance = 4*60) #unit is seconds

plt.plot(x)
plt.plot(x.iloc[peaks].index, x.iloc[peaks], "x")
# plt.plot(np.zeros_like(x), "--", color="gray")
plt.show()

flocs = pd.read_csv('input/flowmeterlocs.csv')
flocs['datetime'] = pd.to_datetime(flocs['datetime'])
flocs = flocs.set_index(['datetime'])
flocs = flocs.sort_index()

#TODO 1
#iterate through direction time change to prepare
# 1 a snapshot of flow profile at given point
# 2 value of the location

fdl = pd.merge_asof(flocs, fdir, left_index=True, right_index=True, direction='nearest')
#this will require manual corrections


for ind, val in fdir.iterrows():
    #print(fval[ind])
    cti = fval_sec.loc[pd.date_range(start=(ind - datetime.timedelta(0,10)),end=(ind+datetime.timedelta(0,150)), freq='1S')]
    # cti = flocs[ind]
    print(cti)
    break

#low flow get 4 min, high flo get 2.5 min

#TODO 2
#iterate through peaks to change sign of the data beyond the peaks

#TODO 3
#iterate through values of pump change to provide time relative to switch
