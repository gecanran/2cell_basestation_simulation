#Filename: basestation.py
import math

class Basestation:
    """Define the class to represent a basestation.

       This class contains all the parameters and functions that
       a basestation need and use as a whole in the main function.

       Attributes:
       TR_POWER: The transmit power of the attenna.
       LINE_LOSS: The loss of the power in transmitting.
       ANT_GAIN: Antenna gain.
       ANT_HEIGHT: Antenna height.
       NUM_CHANNEL: Numbers of channels per BS.
    """
    TR_POWER=10*math.log10(20*1000)
    LINE_LOSS=4
    ANT_GAIN=8
    ANT_HEIGHT=30
    NUM_CHANNEL=15

    def __init__(self,frequency=0,loc_x=0,loc_y=0,name=None):
        if(frequency==None or loc_x==None or loc_y==None):
            raise Exception('You should give the specific detail of the basestation')
        else:
            self.name=name
            self.frequency=frequency
            self.loc_x=loc_x
            self.loc_y=loc_y
            
            self.channel=0
            self.call_attempt=0
            self.callblock_lowsign=0
            self.callblock_lowcpt=0
            self.calldrop_lowsign=0
            self.handoff_fail=0
            self.handoff_success=0
            self.completed_call=0
            self.time_sum=0
            
    
    def modhandoff(self,condition=True,chn_down=True,chn_up=False):
        """change the parameters of the basestation when a handoff happens"""
        if condition:
            self.handoff_success+=1
        if not condition:
            self.handoff_fail+=1
        if chn_down:
            self.channel-=1
        if chn_up:
            self.channel+=1

    def updateCompletedcall(self):
        """change the status of the basestation when a mobile completed a call"""
        self.channel-=1
        self.completed_call+=1
    
    def get_channel(self):
        """get the number of occupied channels of the basestation"""
        return self.channel

    def get_call_attempt(self):
        """get the number of call attempts of the basestaion"""
        return self.call_attempt

    def get_locx(self):
        """get the horizotal location of the basestation"""
        return self.loc_x

    def get_locy(self):
        """get the vertical location of the basestation"""
        return self.loc_y
    
    def get_callblock_lowsign(self):
        """get the number of the call blocks due to low signal"""
        return self.callblock_lowsign

    def call_attempt(self):
        """increase the number of call attempts"""
        self.call_attempt+=1
        
    def low_signal_block(self):
        """increase the number of call blocks due to low signal"""
        self.callblock_lowsign+=1
            
            
            
            

