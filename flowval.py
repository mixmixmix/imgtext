import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import numpy as np



fdir = pd.read_csv('input/152440flow.csv')
fval = pd.read_csv('input/152440out.csv')

fval['dtime'] = pd.to_datetime(fval['date'])

fval = fval[['dtime','flow_v']].set_index(['dtime'])
fval_sec = fval['flow_v'].resample('S').mean()
fval_believe = fval_sec.rolling(window=5).mean() #5 second rolling average
x = -1*fval_believe
peaks, _ = find_peaks(x, height=-4, distance = 4*60) #unit is seconds

plt.plot(x)
plt.plot(x.iloc[peaks].index, x.iloc[peaks], "x")
# plt.plot(np.zeros_like(x), "--", color="gray")
plt.show()

#TODO 1
#iterate through positions of flow meter to prepare a snapshot of flow profile at given point

#TODO 2
#iterate through peaks to change sign of the data beyond the peaks

#TODO 3
#iterate through values of pump change to provide time relative to switch
