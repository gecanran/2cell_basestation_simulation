 #!/usr/bin/python3.3

import cellsimulation as cs
import basestation as bs
import mobile as mb
import modulefuncs as mf
import math
import random

GOS_sum0=0       #sum of the GOS for basestation0
GOS_sum1=0       #sum of the GOS for basestation1
HO_sum0=0        #sum of the handoff failure rate for basestation0
HO_sum1=0
traffic_sum0=0   #sum of the traffic intensity for basestation0
traffic_sum1=0

for k in range(10):
    bs0=bs.Basestation(900,1.5,0.1,'bs0')      #basestation0
    bs1=bs.Basestation(905,4.5,0.1,'bs1')      #basestation1
    mobile_num=cs.run(bs0,bs1,1)
    
    ########################
    list_bs0=[bs0.call_attempt,bs0.callblock_lowsign,bs0.callblock_lowcpt,bs0.calldrop_lowsign,
            bs0.handoff_fail,bs0.handoff_success,bs0.completed_call,bs0.time_sum,bs0.channel]
    list_bs1=[bs1.call_attempt,bs1.callblock_lowsign,bs1.callblock_lowcpt,bs1.calldrop_lowsign,
              bs1.handoff_fail,bs1.handoff_success,bs1.completed_call,bs1.time_sum,bs1.channel]
    GOS_bs0=(list_bs0[1]+list_bs0[2]+list_bs0[3])/list_bs0[0]      #GOS for bs0
    GOS_bs1=(list_bs1[1]+list_bs1[2]+list_bs1[3])/list_bs1[0]      
    HO_fail_rate0=list_bs0[4]/(list_bs0[4]+list_bs0[5])            #handoff failure rate for bs0
    HO_fail_rate1=list_bs1[4]/(list_bs1[4]+list_bs1[5])
    traffic_intensity0=list_bs0[7]/3600                           #traffic intensity for bs0
    traffic_intensity1=list_bs1[7]/3600
    GOS_sum0=GOS_sum0+GOS_bs0
    GOS_sum1=GOS_sum1+GOS_bs1
    HO_sum0=HO_sum0+HO_fail_rate0
    HO_sum1=HO_sum1+HO_fail_rate1
    traffic_sum0=traffic_sum0+traffic_intensity0
    traffic_sum1=traffic_sum1+traffic_intensity1
    print('The number of call attempts:          [{0:d},{1:d}]'.format(bs0.call_attempt,bs1.call_attempt))
    print('Blocked for lack of signal strength:  [{0:d},{1:d}]'.format(bs0.callblock_lowsign,bs1.callblock_lowsign))
    print('Blocked for lack of capacity:         [{0:d},{1:d}]'.format(bs0.callblock_lowcpt,bs1.callblock_lowcpt))
    print('Dropped for lack of signal strength:  [{0:d},{1:d}]'.format(bs0.calldrop_lowsign,bs1.calldrop_lowsign))
    print('Experienced handoff failures:         [{0:d},{1:d}]'.format(bs0.handoff_fail,bs1.handoff_fail))
    print('Experienced successful handoffs:      [{0:d},{1:d}]'.format(bs0.handoff_success,bs1.handoff_success))
    print('Calls completed successfully:         [{0:d},{1:d}]'.format(bs0.completed_call,bs1.completed_call))
    print('Total time calls:                    [{0:d},{1:d}]'.format(bs0.time_sum,bs1.time_sum))
    print('Channels in use:                     [{0:d},{1:d}]'.format(bs0.channel,bs1.channel))
    print('Total number of remained mobiles:     {0:d}'.format(mobile_num))
    print('GOS:                                 [{0:f},{1:f}]'.format(GOS_bs0,GOS_bs1))
    print('Handoff failure rate:                 [{0:f},{0:f}]'.format(HO_fail_rate0,HO_fail_rate1))
    print('Traffic intensity in Erlangs:         [{0:f},{1:f}]'.format(traffic_intensity0,traffic_intensity1))
    print("\n=================================================\n")
GOS_avg0=GOS_sum0/10
GOS_avg1=GOS_sum1/10
HO_avg0=HO_sum0/10
HO_avg1=HO_sum1/10
traffic_avg0=traffic_sum0/10
traffic_avg1=traffic_sum1/10
print('Average GOS:              [{0:f},{1:f}]'.format(GOS_avg0,GOS_avg1))
print('Average Handoff fail rate: [{0:f},{1:f}]'.format(HO_avg0,HO_avg1))
print('Average traffic intensity: [{0:f},{1:f}]'.format(traffic_avg0,traffic_avg1))
