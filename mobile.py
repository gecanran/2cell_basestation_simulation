#Filename: mobile.py
import random
import math
import sys
sys.path.append("/656project")
import basestation
import numpy as np

class Mobile:
    """Define the class to represent a mobile phone.

       This class contains all the parameters and functions that
       a mobile need and use as a whole in the main function.

       Attributes:
       MOBILE_HEIGHT: The height of the mobile when in use.
       MOBILE_SPEED: The speed of the mobile.
       RSL_THRESH: The threshhold of RSL under which the mobile will drop the call.
       HANDOFF_HOm: Handoff margin.
       CALL_DUR: The time duration of a call.
    """
    MOBILE_HEIGHT=1.5
    MOBILE_SPEED=0.01
    RSL_THRESH=-102
    HANDOFF_HOm=3
    CALL_DUR=180
    
    def __init__(self):
        """Initializes the mobile's data."""
        self.call_status=False
        self.location=random.uniform(0,6)
        self.direction=random.choice([-1,1])
        self.serving_bs=None
        self.start_time=0
        self.time=0
        self.no_callup_next=False
        self.time_sum=0
        self.non_serving_bs=None
        

    def calc_RSL(self,bs=None):
        """Calculate the RSL"""
        f=bs.frequency
        d=math.sqrt((self.location-bs.loc_x)**2+bs.loc_y**2)
        EIRP = bs.TR_POWER+bs.ANT_GAIN-bs.LINE_LOSS
        Fading_list = []
        a = (1.1*math.log10(f)-0.7)*self.MOBILE_HEIGHT-(1.56*math.log10(f)-0.8)
        PL = 69.55+26.16*math.log10(f)-13.82*math.log10(bs.ANT_HEIGHT)+(44.9-6.55*math.log10(bs.ANT_HEIGHT))*math.log10(d)-a
        Shadow = random.normalvariate(0,2)
        for i in range(4):
            real = random.gauss(0,1)
            imag = random.gauss(0,1)
            Fading_list.append(20*math.log10(abs(real+1j*imag)))
        Fading_list.sort()
        Fading = Fading_list[1]      #drop the deepest fade value
        RSL = EIRP - PL + Shadow + Fading
        return RSL

    def get_time(self,endtime):
        """ get the exact time"""
        self.time=endtime-self.start_time
        return self.time

    def calc_loc(self):
        """calculate the location of the mobile"""
        self.location=self.location+self.direction*self.MOBILE_SPEED
        return self.location

    def get_loc(self):
        """get the location of the mobile"""
        return self.location

    def mob_call_over(self):
        """change the status of the mobile when the mobile drop a call"""
        self.call_status=False
        self.serving_bs=None
        self.no_callup_next=True

    def start_call(self,start_time):
        """change the status of the mobile when the mobile start to call"""
        self.call_status=True
        self.serving_bs.channel+=1
        self.start_time=start_time
        
    def complete_call(self):
        """change the status of the mobile and basestation when a mobile
           completed a call"""
        self.serving_bs.updateCompletedcall()
        self.time=0
        self.mob_call_over()

    def drop_low_signal(self):
        """change the status of the mobile and basestation when a mobile
           drops a call due to low signal"""
        self.serving_bs.channel-=1
        self.serving_bs.calldrop_lowsign+=1
        self.mob_call_over()

    def handoff_success(self):
        """change the status of the mobile and basestation when a successful
           handoff happens"""
        self.serving_bs.modhandoff()
        self.non_serving_bs.modhandoff(True,False,True)
        self.serving_bs=self.non_serving_bs      #change the serving basestation after successful handoff

    def block(self,reason=""):
        """change the status of the basestation when a call is blocked due
           to the reason"""
        if(reason=="low_signal"):
            self.serving_bs.callblock_lowsign+=1
        elif(reason=="low_capacity"):
            self.serving_bs.callblock_lowcpt+=1

    def handoff_fail(self,bs0=None,bs1=None):
        """change the status of the basestation when a handoff failure happens"""
        if(bs0==self.serving_bs):
            self.serving_bs.modhandoff(False,False)
        elif(bs0== self.non_serving_bs):
            self.non_serving_bs.modhandoff(False,False)
        if(bs1==self.serving_bs):
            self.serving_bs.modhandoff(False,False)
        elif(bs1== self.non_serving_bs):
            self.non_serving_bs.modhandoff(False,False)
        else: pass
        
