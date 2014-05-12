import basestation as bs
import mobile as mb
import math
import random
import numpy as np


def rangeCheck(checklist=[],mindis=0,largedis=0):
    """check if the mobile is in the limited range"""
    for check_elem in checklist[:]:
        if not mindis<check_elem.get_loc()<largedis:
            if(check_elem.call_status):
                check_elem.serving_bs.modhandoff(True)
            checklist.remove(check_elem)
    return checklist

def calc_RSL(mob=None,base=None):
    """calculate the RSL of the mobile"""
    f=base.frequency
    d=math.sqrt((mob.get_loc()-base.get_locx())**2+base.get_locy()**2)
    EIRP = base.TR_POWER+base.ANT_GAIN-base.LINE_LOSS
    Fading_list = []
    a = (1.1*math.log10(f)-0.7)*mob.MOBILE_HEIGHT-(1.56*math.log10(f)-0.8)
    
    PL = 69.55+26.16*math.log10(f)-13.82*math.log10(base.ANT_HEIGHT)+(44.9-6.55*math.log10(base.ANT_HEIGHT))*math.log10(d)-a
    
    Shadow = random.normalvariate(0,2)
    for i in range(4):
        real = random.gauss(0,1)
        imag = random.gauss(0,1)
        Fading_list.append(20*math.log10(abs(real+1j*imag)))
    Fading_list.sort()
    Fading = Fading_list[1]
    RSL = EIRP - PL + Shadow + Fading
    return RSL

def elect_bs(mob=None,bs1=None,bs2=None):
    """choose the right basestation to be the serving basestation"""
    if(calc_RSL(mob,bs1)>=calc_RSL(mob,bs2)):
        return bs1
    return bs2

def elect_nonserving_bs(mob=None,bs1=None,bs2=None):
    """choose the nonserving basestation"""
    if mob.serving_bs==bs1:
        return bs2
    return bs1
