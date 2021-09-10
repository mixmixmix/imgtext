import pandas as pd
import seaborne as sns
import matplotlib.pyplot as plt
fdir = pd.read_csv('input/152440flow.csv')
fval = pd.read_csv('input/152440out.csv')

fval['dtime'] = pd.to_datetime(fval['date'])

fval = fval[['dtime','flow_v']].set_index(['dtime'])
fval_sec = fval['flow_v'].resample('S').mean()
fval_believe = fval_sec.rolling(window=5).mean() #5 second rolling average
fval_sec.plot()
plt.show()
