import basestation as bs
import mobile as mb
import modulefuncs as mf
import math
import random

num=150      #the number of mobiles when initiating

def run(bs0,bs1,numda):
    callprob=float(numda/3600)
    mobilelist=[]
    for i in range(num):
        mobilelist.append(mb.Mobile())         #initiate num mobiles
    for timeindex in range(3600):              #run 3600 times to simulate 1 hour
        mobilelist=mf.rangeCheck(mobilelist,0,6)  #check whether mobile is out of the range
        for mobile in mobilelist:
            if not mobile.call_status:
                no_call_process(mobile,bs0,bs1,timeindex,numda)
            else:
                call_process(mobile,bs0,bs1)
            mobile.location=mobile.calc_loc()    #update the location of mobiles
        if(random.random()<0.5):
            #increase a mobile randomly every 2 seconds
            mobilelist.append(mb.Mobile())
    return(len(mobilelist))
                

def no_call_process(mobile,bs0,bs1,timeindex,numda):
    """process when the mobile does not have a call up"""
    callprob=float(numda/3600)
    if not mobile.no_callup_next:
        if random.random()<callprob:
        #for mobiles that request a call
            mobile.serving_bs=mf.elect_bs(mobile,bs0,bs1)
            mobile.serving_bs.call_attempt+=1
            if(mf.calc_RSL(mobile,mobile.serving_bs)<mobile.RSL_THRESH):
                mobile.block("low_signal")
            else:
                if(mobile.serving_bs.channel>=mobile.serving_bs.NUM_CHANNEL):
                    mobile.block("low_capacity")
                else:
                #for mobiles that request a call successfully
                    mobile.start_call(timeindex)
    else:
        mobile.no_callup_next=False


def call_process(mobile,bs0,bs1):
    """process when the mobie has a call up"""
    mobile.time+=1
    mobile.serving_bs.time_sum+=1
    mobile.non_serving_bs=mf.elect_nonserving_bs(mobile,bs0,bs1)
    if(mobile.time>= mobile.CALL_DUR):
        #for moibles that successfully complete the call
        mobile.complete_call()
    else:
        #for mobiles that have a call up but not complete the call
        RSL=mf.calc_RSL(mobile,mobile.serving_bs)
        RSL2=mf.calc_RSL(mobile,mobile.non_serving_bs)

        if(RSL < mobile.RSL_THRESH):
            #for mobiles that drop the call due to low signal strength
            if( RSL2 >= RSL + mobile.HANDOFF_HOm and RSL2 >= mobile.RSL_THRESH):
                mobile.handoff_fail(mobile.serving_bs,mobile.non_serving_bs)
            mobile.drop_low_signal()
        if(RSL >= mobile.RSL_THRESH and RSL2 >= RSL + mobile.HANDOFF_HOm):
            if(mobile.non_serving_bs.channel >= mobile.non_serving_bs.NUM_CHANNEL):
                #for mobiles that fail to handoff
                mobile.handoff_fail(mobile.non_serving_bs)
            else:
                #for mobiles that handoff successfully
                mobile.handoff_success()
