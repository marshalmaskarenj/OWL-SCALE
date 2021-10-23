"""
SPD to Spectral weightage for RGB Channels. This converts interval-separated SPDs to weightage-per-channel for spectral Radiance simulations. 
This component's code a modified version of LARK "Convert SPD - Write Spectral Radiance Materials" component, and is aimed for source (sky) only.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LOCI, UCLouvain.
    Inputs:
        spd_input: 54 x 2 array of SPDs from 300 to 830 nms, separated by 10nm interval.
        channel: 0 for 3-channel (380/498/586/780); 1 for 9-channel (380/422/460/498/524/550/586/650/714/780)
    Output:
        channel_output: Average SPD per channel"""

self=ghenv.Component
self.Name = "SCALE_SPD2spectral"
self.NickName = 'SPD2spectral'
self.Message = 'OWL 0.0.01\nOCT_15_2021'
self.IconDisplayMode = self.IconDisplayMode.application
self.Category = "SCALE"
self.SubCategory = "3 OWL::Spectral"
try: self.AdditionalHelpFromDocStrings = "3"
except: pass

import rhinoscriptsyntax as rs
import re
import os
from subprocess import Popen
import math
from collections import OrderedDict
from decimal import Decimal

def interpolate(value1,value2,key1,key2,increment): 
    slope = (value2-value1)/(key2-key1)
    value = value1 + (slope*increment)
    return float(value)

#run interpolate function on spectral power distribution
def run_interpolate (dict, bin, interval):   # nanometer bins from source file, interval to interpolate
    for x in dict.keys():  # x = keys
        if x >= 380 and x <=780 and x % source_interval == 0:  #filter dictionary for interpolation
            dict[float(x + interval)] = interpolate (dict[x],dict[x+bin],x,x+bin,interval) #define key and value from interpolate function

#use avg_count function on each bin to generate a list of averages
def avg_list(dict):
    for binX in xrange (len(binType)): #iterates to 3 or 9
#        print dict
        avg_channel.append(avg_count(dict,binX)) #iterate avg_count over all channels
    return avg_channel

#avg_count iterates within wavelength bin to return average
def avg_count(dict, channel):  #9 channels to choose from
    sum = 0
    count = 0
    for key in dict:
       if key >= binType[channel][0] and key  <= binType[channel][1]: #cull array by channel lowest and highest key 
           sum += dict[key] #sum values in channel
           count += 1
    avg = sum/count
    return round (avg,3) #round 3 places

if True:
    channel = 0 if channel is None else channel
    avg_channel = []   #output average color per channel
    bin3 = [586,780],[498,586],[380,498]
    bin9 = [380,422],[422,460],[460,498],[498,524],[524,550],[550,586],[586,650],[650,714],[714,780]
    if channel==0:
        binType = bin3
    elif channel==1:
        binType = bin9
    b=spd_input
    print b
    data = [] #create list
    for line in b:
        if not line.startswith('{'): #cull the Optics header
                data.append(line.split())
#    print data
    data2 = filter(None, data)  #filter blank lines in data list
    spd = OrderedDict() #create a dictionary in order of wavelength
    for line in data2:
        (wave, val) =  line[0], line[1] #assign first 2 columns of data
        spd[float(wave)] = float(val)  #assign values to dictionary keys
    for keyA in spd.keys():
        if keyA < 10:  #true for Optics6 export which measures wavelenth in microns 
            spd[keyA*1000] = spd.pop(keyA)  #replace old dict key with new key
        else:
            pass
#    print spd
    maxkey = max(spd, key=lambda i: spd[i])
    maxvalue = spd[maxkey]
    factor = 1/maxvalue
    for keyB in spd:
        spd[keyB] = spd[keyB]*factor
    else:
        pass
#    print spd
    source_interval=10
    for iteration in xrange (1,source_interval): # iterate run_interpolate function at 1 nm intervals over source_interval
        run_interpolate (spd,source_interval,iteration)
    avg_channel=avg_list(spd)
    avg_channel=[round(i,3) for i in avg_channel]
#    print type(avg_channel)
    channel_output = avg_channel