import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import numpy as np
import datetime

fval = pd.read_csv('input/flowvalchange.csv')
fval['date'] = pd.to_datetime(fval['date'])

fval = fval.set_index(['date'])
fval = fval.sort_index()

fval_sec = fval['flow_v'].resample('S').median() # often we'd have a reading with wrong first digit popping up, but it is unlikely to be the most commond reading in a given second

fcl = pd.read_csv('input/switchcross.csv')
fcl['switch_time'] = pd.to_datetime(fcl['switch_time'])
fcl['cross_time'] = pd.to_datetime(fcl['cross_time'])

alldf = dict()

for ind, val in fcl.iterrows():
    cti = fval_sec.loc[pd.date_range(start=(val['switch_time'] - datetime.timedelta(0,10)),end=(val['switch_time']+datetime.timedelta(0,150)), freq='1S')]

    cttrue = cti.reset_index().apply(lambda x: -1*x['flow_v']*val['flow_dir'] if x['index'] < val['cross_time'] else x['flow_v']*val['flow_dir'],axis=1)

    alldf[val['loc_name']]=cttrue
    # cti = flocs[ind]

#read fishloc
fish = pd.read_csv('input/reaction21.csv')
fish['direction']=fish['direction'].replace({'Flow Counterclockwise (2)':-1, 'Flow Clockwise (1)':1})


fishloc = pd.read_csv('output/fishlocs.csv')

fishloc['loc_x']=fishloc.apply(lambda x: x['loc_x'] if x['loc_x']>=0 else x['loc_x']+2.79, axis =1)

myf = fish[(fish['info']=='dir_change') | (fish['info']=='swim_off')]

myfl = pd.merge(myf, fishloc, left_on='fishname', right_on='loc_name') # there are more locations than fish with criteria as some were deemed too unstable later on.

def getCloser(fcl, xx, yy, fs, fdir):
    mindist = 100
    closesetloc = 'x'
    for ind, val in fcl.iterrows():
        if val['flow_dir'] == fdir and val['fs'] == fs:
            dx = (val['loc_x']-xx)**2
            dy = (val['loc_y']-yy)**2
            dist = np.sqrt(dx+dy)
            if dist < mindist:
                mindist = dist
                cloc = val['loc_name']
    return cloc, mindist

flocs = []
fdist = []
for ind, val in myfl.iterrows():
    fl, fd = getCloser(fcl, val['loc_x'],val['loc_y'], val['fs'], val['direction'])
    flocs.append(fl)
    fdist.append(fd)

myfl['flocs']=flocs
myfl['fdist']=fdist


stableprev = []
stablenext = []
changeval = []
stableprev_v = []
stablenext_v = []
changeval_v = []
change5 = []
change5_v = []

#get average flow values fucking finally
for ind, val in myfl.iterrows():

    cf = alldf[val['flocs']]
    stableprev.append(abs(cf.iloc[0:10].mean()))
    stablenext.append(abs(cf.iloc[-10:].mean()))
    stableprev_v.append(cf.iloc[0:10].std())
    stablenext_v.append(cf.iloc[-10:].std())
    sreac = (datetime.datetime.strptime(val['tdiff'], '%H:%M:%S') - datetime.datetime(1900,1,1,0,0,0)).seconds
    changeval.append(abs(cf.iloc[sreac-5:sreac+5].mean()))
    changeval_v.append(cf.iloc[sreac-5:sreac+5].std())
    change5.append(abs(cf.iloc[sreac-2:sreac+3].mean()))
    change5_v.append(cf.iloc[sreac-2:sreac+3].std())

myfl['stableprev']=stableprev
myfl['stableprev_v']=stableprev_v
myfl['stablenext']=stablenext
myfl['stablenext_v']=stablenext_v
myfl['changeval']=changeval
myfl['changeval_v']=changeval_v
myfl['change5']=change5
myfl['change5_v']=change5_v

myfl['asfractprev5'] = myfl.apply(lambda x: x['change5']/x['stableprev'],axis=1)
myfl['asfractprev10'] = myfl.apply(lambda x: x['changeval']/x['stableprev'],axis=1)

myfl.to_csv('./input/results21.csv',index=False)

sns.histplot(data=myfl, x='changeval',binwidth=1,kde=True)
plt.show()
sns.histplot(data=myfl, x='change5',binwidth=1,kde=True)
plt.show()
