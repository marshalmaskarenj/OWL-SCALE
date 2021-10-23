"""
Build a spectral sky Radiance definition, by taking 3-channel RGB weightage from SPD2Spectral, in addition to other data values. 
This component works similar to {LARK Spectral Sky} component, but is adapted for OWL workflow.
--
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LOCI, UCLouvain.
    Inputs:
        channel_input: Connect SCALE_SPD2spectral. Default is {0.5,0.5,0.5}
        latitude: From location; in Degrees. Default is 15.
        longitude: From Location; in Degrees. Default is 15.
        timeZone: Positive for East of UTC, negative for west. Default is 0.
        sky_type: Radiance sky definition (between 0 to 5) specifying {[-s +s -c -i +i -u]}. Default is 0.
        month: Month (between 1 to 12). Default is 1.
        day: Day of Month (between 1 and 31). Default is 1.
        hour: Hour of Day (between 1 and 24). Default is 12.
        dir_norm_rad: Direct Normal Radiation at the HOY (connect output 15 of SCALE_OpenEPW). Default is 500.
        horz_diff_rad: Diffuse Horizontal Radiation at HOY (connect output 16 of SCALE_OpenEPW). Default is 200.
        sunAltitude: The solar angle above Horizon. From SCALE_SunPos. Default is 45.
    Output:
        sky_material: 3 channel sky definition: the output for LB Radiance simulation.
        skyDef: which sky-type is being generated (Sunny [-/+], Cloudy, Intermediate [-/+], Uniform)
        skyContent: The description of sky created by the command.
        skyFilePath: The location of the gensky generated File. """

self=ghenv.Component
self.Name = "SCALE_3CspectralSky"
self.NickName = '3CspectralSky'
self.Message = 'OWL 0.0.01\nOCT_15_2021'
self.IconDisplayMode = self.IconDisplayMode.application
self.Category = "SCALE"
self.SubCategory = "1 OWL::Common"
try: self.AdditionalHelpFromDocStrings = "6"
except: pass

import rhinoscriptsyntax as rs
import math
import os
import sys

def RADDaylightingSky(sky, r, g, b):
    return  "!gensky " + sky + "\n\n" + \
            "skyfunc glow sky_mat\n" + \
            "0\n" + \
            "0\n" + \
            "4\n" + \
            str(r)+" "+str(g)+" "+str(b)+"  0\n\n" + \
            "sky_mat source sky\n" + \
            "0\n" + \
            "0\n" + \
            "4\n" + \
            "0 0 1 180\n\n" + \
            "skyfunc glow ground_glow\n" + \
            "0\n" + \
            "0\n" + \
            "4\n" + \
            "1 0.8 0.5 0\n\n" + \
            "ground_glow source ground\n" + \
            "0\n" + \
            "0\n" + \
            "4\n" + \
            "0 0 -1 180\n\n"
                    
def fngensky(mm,dd,hh,Fn1,Fn2,Fn3,Fn4,diffuse,direct,lat,long,mer):
    return str(mm)+" "+str(dd)+" "+str(round(hh,1))+" "+str(Fn1)+str(Fn2)+str(Fn3)+str(Fn4)+" -B "+str(round(diffuse,2))+" -R "+str(round(direct,2))+" -a "+str(round(lat,2))+" -o "+str(round(long,2))+" -m "+str(int(mer))


def fndiffuse(horz_diff_rad,r,g,b):
#    print r,g,b
    v_r = 0.2686  #.275
    v_g = 0.6693  #.670
    v_b = 0.0621  #.065  
    sum3 = r*v_r + g*v_g + b*v_b
#    print sum3
    diffuse_val = round((horz_diff_rad/sum3),2)
    return diffuse_val

def fnskydef(skytype): # {-s} {+s} {-c} {-i} {+i} {-u}
    if skytype==1:
        Fn1=" +s "
        Fn2=""
        Fn3=""
        Fn4=""
        defn="Sunny sky with sun. In addition to the sky distribution function, a source description of the sun is generated."
    elif skytype==2:
        Fn1=""
        Fn2=" -c "
        Fn3=""
        Fn4=""
        defn="Cloudy sky. The sky distribution will correspond to a standard CIE overcast day."
    elif skytype==3:
        Fn1=""
        Fn2=""
        Fn3=" -i "
        Fn4=""
        defn="Intermediate sky without sun. The sky will correspond to a standard CIE intermediate day."
    elif skytype==4:
        Fn1=""
        Fn2=""
        Fn3=" +i "
        Fn4=""
        defn="Intermediate sky with sun. In addition to the sky distribution, a (somewhat subdued) sun is generated."
    elif skytype==5:
        Fn1=""
        Fn2=""
        Fn3=""
        Fn4=" -u "
        defn="Uniform cloudy sky. The sky distribution will be completely uniform."
    else:
        Fn1=" -s "
        Fn2=""
        Fn3=""
        Fn4=""
        defn="Sunny sky without sun. The sky distribution will correspond to a standard CIE clear day"
    return Fn1,Fn2,Fn3,Fn4,defn

#skydef=fnskydef(sky_type)
def main(sky,r,g,b):
    try: 
        os.makedirs(specify_folder)
    except OSError, e:
        if not os.path.exists(specify_folder):
            sys.exit("Error creating Directory. Check permissions.")
    outputFile=specify_folder + "\spectralSky_"+ str(sky_name) +".sky"
    skyStr = RADDaylightingSky(sky,r,g,b)
    skyFile = open(outputFile, 'w')
    skyFile.write(skyStr)
    skyFile.close()
    return sky, skyStr, outputFile

if True:
    specify_folder = "C:\Users\Public\SCALE\SPD" if specify_folder is None else str(specify_folder)
    sky_name="Mumbai-Clear" if sky_name is None else sky_name
    r=0.5 if channel_input is None else float(channel_input[0])
    g=0.5 if channel_input is None else float(channel_input[1])
    b=0.5 if channel_input is None else float(channel_input[2])
    latitude=15 if latitude is None else round(float(latitude),2)
    longitude=15 if longitude is None else round(float(longitude),2)
    timeZone=0 if timeZone is None else float(timeZone)
    sky_type=0 if sky_type is None else int(sky_type)
    month=1 if month is None else int(month)
    day=1 if day is None else int(day)
    hour=12 if hour is None else float(hour)
    dir_norm_rad=500 if dir_norm_rad is None else float(dir_norm_rad)
    horz_diff_rad=200 if horz_diff_rad is None else float(horz_diff_rad)
    sunAltitude=45 if sunAltitude is None else float(sunAltitude)
#    sky=" 3 21 12.0 +i -B 111.87 -R 2.64 -a 51.15 -o 0.18 -m -45"
    mer=int(-15*(float(timeZone)))
#    diffuse=float(horz_diff_rad)
    diffuse=fndiffuse(horz_diff_rad,r,g,b)
    direct=math.cos(math.radians(90-int(sunAltitude)))*dir_norm_rad
    Fn1,Fn2,Fn3,Fn4,defn=fnskydef(sky_type)
    sky=fngensky(month,day,hour,Fn1,Fn2,Fn3,Fn4,diffuse,direct,latitude,longitude,mer)
#    xx=RADDaylightingSky(sky, r, g, b)
    result=main(sky,r,g,b)
#    print xx, channel_input
#    sky_material = result
    if result!= -1:
        sky_material, skyContent, skyFilePath = result
        skyDef=defn