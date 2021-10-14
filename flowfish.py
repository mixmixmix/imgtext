import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import numpy as np
import datetime

def getCloser(fcl, xx, yy, fs, fdir):
    mindist = 100
    cloc = 'x'
    for ind, val in fcl.iterrows():
        if val['flow_dir'] == fdir and val['fs'] == fs:
            dx = (val['loc_x']-xx)**2
            dy = (val['loc_y']-yy)**2
            dist = np.sqrt(dx+dy)
            if dist < mindist:
                mindist = dist
                cloc = val['loc_name']
    return cloc, mindist

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

##ADD FLOW VALUES AT LOCATIONS
for ind, val in fcl.iterrows():

    cf = alldf[val['loc_name']]
    fcl.loc[ind,'10prev']=cf.iloc[0:10].mean()
    fcl.loc[ind,'10after']=cf.iloc[-10:-1].mean()
    fcl.loc[ind,'10prev_v']=cf.iloc[0:10].std()
    fcl.loc[ind,'10after_v']=cf.iloc[-10:-1].std()

fcl['xcm']=fcl.apply(lambda x: x['loc_x']*60, axis=1)
fcl['ycm']=fcl.apply(lambda x: x['loc_y']*60, axis=1)

fcl[['loc_name','xcm','ycm','fs','10prev','10after','10prev_v','10after_v']].drop_duplicates().to_csv('./output/locval.csv',index=False)

#read fishloc
allfish = pd.read_csv('input/reactions_all.csv')
allfish['direction']=allfish['direction'].replace({'0':-1, '1':1})
allfish['direction']=allfish['direction'].replace({'Flow Counterclockwise (2)':-1, 'Flow Clockwise (1)':1})

allfish['fishtype'] = allfish.apply(lambda x: 'wild' if int(x.name) >= 113 else ('farmed_in' if x['fs']=='old' else 'farmed_loch'), axis=1)


oldfish = allfish[(allfish['fs']=='old') | (allfish['fs']=='highold') ]
fish = allfish[(allfish['fs']=='high') | (allfish['fs']=='low') ]


fishloc = pd.read_csv('output/fishlocs.csv')

fishloc['loc_x']=fishloc.apply(lambda x: x['loc_x'] if x['loc_x']>=0 else x['loc_x']+2.79, axis =1)

myf = fish[(fish['info']=='dir_change') | (fish['info']=='swim_off')]
rejectmyf = fish[(fish['info']!='dir_change') & (fish['info']!='swim_off')]

myfl = pd.merge(myf, fishloc, left_on='fishname', right_on='loc_name') # there are more locations than fish with criteria as some were deemed too unstable later on.


flocs = []
fdist = []
for ind, val in myfl.iterrows():
    fl, fd = getCloser(fcl, val['loc_x'],val['loc_y'], val['fs'], val['direction'])
    flocs.append(fl)
    fdist.append(fd)

myfl['flocs']=flocs
myfl['fdist']=fdist

stable10prev_v = []
stable10after_v = []
change10_v = []
change5 = []
change1 = []
change5_v = []

#get average flow values fucking finally
for ind, val in myfl.iterrows():

    cf = alldf[val['flocs']]
    myfl.loc[ind,'stable10prev']=cf.iloc[0:10].mean()
    myfl.loc[ind,'stable10after']=cf.iloc[-10:].mean()
    stable10prev_v.append(cf.iloc[0:10].std())
    stable10after_v.append(cf.iloc[-10:].std())
    sreac = (datetime.datetime.strptime(val['tdiff'], '%H:%M:%S') - datetime.datetime(1900,1,1,0,0,0)).seconds
    myfl.loc[ind,'change10']=cf.iloc[sreac-5:sreac+5].mean()
    change10_v.append(cf.iloc[sreac-5:sreac+5].std())
    change5.append(cf.iloc[sreac-2:sreac+3].mean())
    change5_v.append(cf.iloc[sreac-2:sreac+3].std())
    change1.append(cf.iloc[sreac-2:sreac+3].mean())

myfl['stable10prev_v']=stable10prev_v
myfl['stable10next_v']=stable10after_v
myfl['change10_v']=change10_v
myfl['change5']=change5
myfl['change5_v']=change5_v
myfl['change1']=change1

myfl['asfractprev5'] = myfl.apply(lambda x: x['change5']/x['stable10prev'],axis=1)
myfl['asfractprev10'] = myfl.apply(lambda x: x['change10']/x['stable10prev'],axis=1)

myfl.to_csv('./input/results21.csv',index=False)


## read in data from the first experiment

finres = pd.concat([rejectmyf,oldfish,myfl])



finres['tdiff'] = finres['tdiff'].astype(str)
finres['tsec'] = finres.apply(lambda x: (datetime.datetime.strptime(x['tdiff'], '%H:%M:%S') - datetime.datetime(1900,1,1,0,0,0)).seconds if len(x['tdiff'])==8 else np.nan, axis = 1)


finres['abs1']=abs(finres['change1'])
finres['abs5']=abs(finres['change5'])
finres['abs10']=abs(finres['change10'])

finres['fsdir'] = finres.apply(lambda x: x['fs']+str(x['direction']), axis = 1)

finres.to_csv('./input/finres.csv',index=False)

sns.histplot(data=finres, x='tsec', hue = 'fsdir',binwidth=10,kde=True)
plt.show()

sns.histplot(data=finres, x='abs1', hue = 'fsdir' ,binwidth=1,kde=True)
plt.show()

sns.histplot(data=finres, x='abs10', hue = 'fsdir' ,binwidth=1,kde=True)
plt.show()

sns.histplot(data=finres, x='abs5', hue = 'fsdir' ,binwidth=1,kde=True)
plt.show()

sns.countplot(data=finres, x='info', hue = 'fsdir' )
plt.show()
