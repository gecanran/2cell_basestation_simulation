 #!/usr/bin/python3.3

import cellsimulation as cs
import basestation as bs
import mobile as mb
import modulefuncs as mf
import math
import random
import numpy as np
import matplotlib.pyplot as plt

numda=1
GOS0=[]
GOS1=[]
Drops_lowsig0=[]
Drops_lowsig1=[]
Blocks_lowsig0=[]
Blocks_lowsig1=[]
Blocks_lowcap0=[]
Blocks_lowcap1=[]

for k in range(19):
    bs0=bs.Basestation(900,1.5,0.1,'bs0')      #basestation0
    bs1=bs.Basestation(905,4.5,0.1,'bs1')      #basestation1
    mobile_num=cs.run(bs0,bs1,numda)
    numda+=0.5
    
    ########################
    list_bs0=[bs0.call_attempt,bs0.callblock_lowsign,bs0.callblock_lowcpt,bs0.calldrop_lowsign,
            bs0.handoff_fail,bs0.handoff_success,bs0.completed_call,bs0.time_sum,bs0.channel]
    list_bs1=[bs1.call_attempt,bs1.callblock_lowsign,bs1.callblock_lowcpt,bs1.calldrop_lowsign,
              bs1.handoff_fail,bs1.handoff_success,bs1.completed_call,bs1.time_sum,bs1.channel]
 
    GOS_bs0=(list_bs0[1]+list_bs0[2]+list_bs0[3])/list_bs0[0]
    GOS_bs1=(list_bs1[1]+list_bs1[2]+list_bs1[3])/list_bs1[0]
    HO_fail_rate0=list_bs0[4]/(list_bs0[4]+list_bs0[5])
    HO_fail_rate1=list_bs1[4]/(list_bs1[4]+list_bs1[5])
    traffic_intensity0=list_bs0[7]/3600
    traffic_intensity1=list_bs1[7]/3600
    GOS0.append(GOS_bs0)
    GOS1.append(GOS_bs1)
    Drops_lowsig0.append(bs0.calldrop_lowsign)
    Drops_lowsig1.append(bs1.calldrop_lowsign)
    Blocks_lowsig0.append(bs0.callblock_lowsign)
    Blocks_lowsig1.append(bs1.callblock_lowsign)
    Blocks_lowcap0.append(bs0.callblock_lowcpt)
    Blocks_lowcap1.append(bs1.callblock_lowcpt)
    '''print('The number of call attempts:          [{0:d},{1:d}]'.format(bs0.call_attempt,bs1.call_attempt))
    print('Blocked for lack of signal strength:  [{0:d},{1:d}]'.format(bs0.callblock_lowsign,bs1.callblock_lowsign))
    print('Blocked for lack of capacity:         [{0:d},{1:d}]'.format(bs0.callblock_lowcpt,bs1.callblock_lowcpt))
    print('Dropped for lack of signal strength:  [{0:d},{1:d}]'.format(bs0.calldrop_lowsign,bs1.calldrop_lowsign))
    print('Experienced handoff failures:         [{0:d},{1:d}]'.format(bs0.handoff_fail,bs1.handoff_fail))
    print('Experienced successful handoffs:      [{0:d},{1:d}]'.format(bs0.handoff_success,bs1.handoff_success))
    print('Calls completed successfully:         [{0:d},{1:d}]'.format(bs0.completed_call,bs1.completed_call))
    print('Total time calls:                    [{0:d},{1:d}]'.format(bs0.time_sum,bs1.time_sum))
    print('Channels in use:                     [{0:d},{1:d}]'.format(bs0.channel,bs1.channel))
    print('Total number of remained mobiles:     {0:d}'.format(len(mobilelist)))
    print('GOS:                                 [{0:f},{1:f}]'.format(GOS_bs0,GOS_bs1))
    print('Handoff failure rate:                 [{0:f},{0:f}]'.format(HO_fail_rate0,HO_fail_rate1))
    print('Traffic intensity in Erlangs:         [{0:f},{1:f}]'.format(traffic_intensity0,traffic_intensity1))
    print("\n=================================================\n")
    '''
    numda=numda+0.5

x=np.arange(1.,10.5,0.5)
array_GOS0=np.array(GOS0)
array_GOS1=np.array(GOS1)
array_Drops_lowsig0=np.array(Drops_lowsig0)
array_Drops_lowsig1=np.array(Drops_lowsig1)
array_Blocks_lowsig0=np.array(Blocks_lowsig0)
array_Blocks_lowsig1=np.array(Blocks_lowsig1)
array_Blocks_lowcap0=np.array(Blocks_lowcap0)
array_Blocks_lowcap1=np.array(Blocks_lowcap1)
plt.plot(x,array_GOS0,'b--',x,array_GOS1,'r-')
plt.subplot(221)
plt.plot(x,array_GOS0,"b-")
plt.title("GOS with the increase of call rate for bs0",fontsize=13)
plt.xlabel("Call rate",fontsize=10)
plt.ylabel("Rate")
plt.grid(True)
#plt.axis([1,10,0,0.7])
plt.legend(["GOS"],loc='upper left')

plt.subplot(223)
plt.plot(x,array_GOS1,"b-")
plt.title("GOS with the increase of call rate for bs1",fontsize=13)
plt.xlabel("Call rate",fontsize=10)
plt.ylabel("Rate")
plt.grid(True)
plt.legend(["GOS"],loc='upper left')

plt.subplot(222)
plt.plot(x,array_Blocks_lowcap0,"b-",x,array_Drops_lowsig0,'r--',x,array_Blocks_lowsig0,'y^')
plt.title("Rate with the increase of call rate for bs0",fontsize=13)
plt.xlabel("Call rate",fontsize=10)
plt.ylabel("Rate")
plt.grid(True)
plt.legend(["Bcap","Dsig",'Bsig'],loc='upper left')

plt.subplot(224)
plt.plot(x,array_Blocks_lowcap0,"b-",x,array_Drops_lowsig0,'r--',x,array_Blocks_lowsig1,'y^')
plt.title("Rate with the increase of call rate for bs1",fontsize=13)
plt.xlabel("Call rate",fontsize=10)
plt.ylabel("Rate")
plt.grid(True)
plt.legend(["Bcap","Dsig",'Bsig'],loc='upper left')
plt.show()
