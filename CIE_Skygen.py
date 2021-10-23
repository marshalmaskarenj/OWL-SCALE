"""
Provides the patch-luminance for the 145 tregenza patches as output, based on CIE sky-type defined.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LOCI, UCLouvain.
    Inputs:
        sunAltitude: Solar Altitude angle at the specific HOY (output from SCALE_SunPos) Default is 30 (from horizon)
        sunAzimuth: The azimuth angle of sun at the specific HOY (output from SCALE_SunPos); Default is 0 (south)
        Zen_Lum_Lz: Zenith Luminance in Cd/m2 (connect output 20 of SCALE_OpenEPW); Default is 100.
        CIEskyType: The CIE sky definition (between 1 to 15), where 1-5 are overcast, 11-15 are clear and 6-10 are intermediate. Default is 12 (CIE Clear).
    Output:
        matrix_out: The generated luminance matrix. FLATTEN the output for optima."""
self=ghenv.Component
self.Name = "SCALE_CIE_Skygen"
self.NickName = 'CIE_Skygen'
self.Message = 'OWL 0.0.01\nOCT_15_2021'
self.IconDisplayMode = self.IconDisplayMode.application
self.Category = "SCALE"
self.SubCategory = "1 OWL::Common"
try: self.AdditionalHelpFromDocStrings = "4"
except: pass

import math
import csv 
import System
import rhinoscriptsyntax as rs
import Rhino as rc
import scriptcontext as sc
import Grasshopper.Kernel as gh
from Grasshopper import DataTree
from Grasshopper.Kernel.Data import GH_Path

def main(alt_deg,az_deg,Lz,a,b,c,d,e): #alt_deg = Solar Altitude | az_deg = Solar Azimuth
    # patchpos[n][0] shows the altitude of the patch, patchpos[n][1] shows the azimuth of the patch. First 30 patches are at 6 degree alt (30P @ 6deg -- near horizon) followed by 30P @ 18deg, 24P @ 30deg, 24P @ 42deg, 18P @ 54deg, 12P @ 66 deg, 6P @ 78deg, and the final zenith patch
    patchpos=[[6,0],[6,12],[6,24],[6,36],[6,48],[6,60],[6,72],[6,84],[6,96],[6,108],[6,120],[6,132],[6,144],[6,156],[6,168],[6,180],[6,192],[6,204],[6,216],[6,228],[6,240],[6,252],[6,264],[6,276],[6,288],[6,300],[6,312],[6,324],[6,336],[6,348],[18,0],[18,12],[18,24],[18,36],[18,48],[18,60],[18,72],[18,84],[18,96],[18,108],[18,120],[18,132],[18,144],[18,156],[18,168],[18,180],[18,192],[18,204],[18,216],[18,228],[18,240],[18,252],[18,264],[18,276],[18,288],[18,300],[18,312],[18,324],[18,336],[18,348],[30,0],[30,15],[30,30],[30,45],[30,60],[30,75],[30,90],[30,105],[30,120],[30,135],[30,150],[30,165],[30,180],[30,195],[30,210],[30,225],[30,240],[30,255],[30,270],[30,285],[30,300],[30,315],[30,330],[30,345],[42,0],[42,15],[42,30],[42,45],[42,60],[42,75],[42,90],[42,105],[42,120],[42,135],[42,150],[42,165],[42,180],[42,195],[42,210],[42,225],[42,240],[42,255],[42,270],[42,285],[42,300],[42,315],[42,330],[42,345],[54,0],[54,20],[54,40],[54,60],[54,80],[54,100],[54,120],[54,140],[54,160],[54,180],[54,200],[54,220],[54,240],[54,260],[54,280],[54,300],[54,320],[54,340],[66,0],[66,30],[66,60],[66,90],[66,120],[66,150],[66,180],[66,210],[66,240],[66,270],[66,300],[66,330],[78,0],[78,60],[78,120],[78,180],[78,240],[78,300],[90,0]]
    patch_lum=[[0 for col in range(1)] for row in range(145)]
    az_s = math.radians(az_deg)
    Zsdeg=90-alt_deg
    Zs = math.radians(Zsdeg)
    for i in range (0,145,1):
        Z=math.radians(90-patchpos[i][0])
        az=math.radians(patchpos[i][1])
        Az_net = abs(az-az_s)
        kappa = math.acos((math.cos(Zs)*math.cos(Z))+(math.sin(Zs)*math.sin(Z)*math.cos(Az_net)))  # Skypatch Sun Distance
        phyZ = 1+a*math.exp(b/math.cos(math.radians(Z)))
        phy0 = 1+a*math.exp(b)
        fkappa = 1+(c*(math.exp(d*kappa)-math.exp(d*(math.pi)/2)))+(e*(math.cos(kappa))**2)
        fZs = 1+(c*(math.exp(d*Zs)-math.exp(d*(math.pi)/2)))+(e*(math.cos(Zs))**2)
        r_gradation = phyZ/phy0
        r_indicatrix = fkappa/fZs
        ratio = r_indicatrix*r_gradation
        Ldes = Lz * ratio
#        print Ldes
        patch_lum[i]=Ldes
#    print patch_lum
    return patch_lum

def setParameters(Set):
    if Set==1:
        a=4; b=-0.7; c=0; d=-1; e=0
    elif Set==2:
        a=4; b=-0.7; c=2; d=-1.5; e=0.15
    elif Set==3:
        a=1.1; b=-0.8; c=0; d=-1; e=0
    elif Set==4:
        a=1.1; b=-0.8; c=2; d=-1.5; e=0.15
    elif Set==5:
        a=0; b=-1; c=0; d=-1; e=0
    elif Set==6:
        a=0; b=-1; c=2; d=-1.5; e=0.15
    elif Set==7:
        a=0; b=-1; c=5; d=-2.5; e=0.3
    elif Set==8:
        a=0; b=-1; c=10; d=-3; e=0.45
    elif Set==9:
        a=-1; b=-0.55; c=2; d=-1.5; e=0.15
    elif Set==10:
        a=-1; b=-0.55; c=5; d=-2.5; e=0.3
    elif Set==11:
        a=-1; b=-0.55; c=10; d=-3; e=0.45
    elif Set==12:
        a=-1; b=-0.32; c=10; d=-3; e=0.45
    elif Set==13:
        a=-1; b=-0.32; c=16; d=-3; e=0.3
    elif Set==14:
        a=-1; b=-0.15; c=16; d=-3; e=0.3
    elif Set==15:
        a=-1; b=-0.15; c=24; d=-2.8; e=0.15
    else:
        a=0;b=0;c=0;d=0;e=0
    return a,b,c,d,e

if True:
    sunAltitude = 30 if sunAltitude is None else float(sunAltitude)
    sunAzimuth = 0 if sunAzimuth is None else float(sunAzimuth)
    Zen_Lum_Lz = 100 if Zen_Lum_Lz is None else float(Zen_Lum_Lz)
    CIEskyType=12 if CIEskyType is None else int(CIEskyType)
    a,b,c,d,e=setParameters(CIEskyType)
    result=main(sunAltitude,sunAzimuth,Zen_Lum_Lz,a,b,c,d,e)
    matrix_out=result
#    print a,b,c,d,e
#    result=imac(my_file,category,hourly,DOY)
#    out_type,band,plus,minus=result
ReadMe="INPUTS:\nsunAltitude: Solar Altitude angle at the specific HOY (output from SCALE_SunPos) "+ \
"Default is 30 (from horizon)\nsunAzimuth: The azimuth angle of sun at the specific HOY (output from SCALE_SunPos); Default is 0 (south)\n"+ \
"Zen_Lum_Lz: Zenith Luminance in Cd/m2 (connect output 20 of SCALE_OpenEPW); Default is 100.\n"+ \
"CIEskyType: The CIE sky definition (between 1 to 15), where 1-5 are overcast, 11-15"+ \
" are clear and 6-10 are intermediate. Default is 12 (CIE Clear).\nOUTPUT:\nmatrix_out: The generated luminance matrix. FLATTEN this datatype for optima."