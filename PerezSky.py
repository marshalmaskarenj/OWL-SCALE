"""
Provides discrete luminance for each of the 145 tregenza patches as output, based on Perez all-weather sky-model.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LOCI, UCLouvain.
    Inputs:
        sunAltitude: Solar Altitude angle at the specific HOY (output from SCALE_SunPos) Default is 30 (from horizon)
        sunAzimuth: The azimuth angle of sun at the specific HOY (output from SCALE_SunPos); Default is 0 (south)
        Zen_Lum_Lz: Zenith Luminance in Cd/m2 (connect output 20 of SCALE_OpenEPW); Default is 10000.
        HorzDiffRad: Horizontal Diffuse Radiation (connect output 16 of SCALE_OpenEPW); Default is 300.
        DirNormRad: Direct Normal Radiation (connect output 15 of SCALE_OpenEPW); Default is 500.
        OptAirMass: Optical Air Mass (UNSURE connected to Turbidity? Aerosol Optical Depth maybe) (connect output 30 of SCALE_OpenEPW). Default is 2.
        NormExIrrad: Normal Incident Extraterrestrial Irradiance (connect output 12 of SCALE_OpenEPW); Default is 1300.
    Output:
        matrix_out: The generated luminance matrix. Flatten this for optima."""
self=ghenv.Component
self.Name = "SCALE_PerezSky"
self.NickName = 'PerezSky'
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

def fn_eps(Dh,I,Z): #sky clearness function, Dh (or E_ed) is Horizontal Diffuse Radiation, I (or E_es) is Direct Normal Radiation, Z is solar zenith angle (degrees)
    k=1.041
#    Z=math.radians(Z)
    clr=(((Dh+I)/Dh)+(k*Z*Z*Z))/(1+(k*Z*Z*Z))
    return clr

def fn_del(m,E_ed,E_es0): # Perez sky brightness, m is optical air mass, E_ed (or Dh) is Horizontal Difuse Radiation, and E_es0 is normal incident extraterrestrial irradiance
    delta=m*E_ed/E_es0
    return delta

def fn_a1(eps):
    if eps<1.065:
        a1=1.3525
    elif 1.065<eps<1.230:
        a1=-1.2219
    elif 1.230<eps<1.5:
        a1=-1.1
    elif 1.5<eps<1.95:
        a1=-0.5484
    elif 1.95<eps<2.8:
        a1=-0.6
    elif 2.8<eps<4.5:
        a1=-1.0156
    elif 4.5<eps<6.2:
        a1=-1
    else:
        a1=-1.05
    return a1

def fn_a2(eps):
    if eps<1.065:
        a2= -0.2576
    elif 1.065<eps<1.230:
        a2= -0.7730
    elif 1.230<eps<1.5:
        a2= -0.2515
    elif 1.5<eps<1.95:
        a2= -0.6654
    elif 1.95<eps<2.8:
        a2= -0.3566
    elif 2.8<eps<4.5:
        a2= -0.3670
    elif 4.5<eps<6.2:
        a2= 0.0211
    else:
        a2= 0.0289
    return a2

def fn_a3(eps):
    if eps<1.065:
        a3= -0.2690
    elif 1.065<eps<1.230:
        a3= 1.4148
    elif 1.230<eps<1.5:
        a3= 0.8952
    elif 1.5<eps<1.95:
        a3= -0.2672
    elif 1.95<eps<2.8:
        a3= -2.5000
    elif 2.8<eps<4.5:
        a3= 1.0078
    elif 4.5<eps<6.2:
        a3= 0.5025
    else:
        a3= 0.4260
    return a3

def fn_a4(eps):
    if eps<1.065:
        a4= -1.4366
    elif 1.065<eps<1.230:
        a4= 1.1016
    elif 1.230<eps<1.5:
        a4= 0.0156
    elif 1.5<eps<1.95:
        a4= 0.7117
    elif 1.95<eps<2.8:
        a4= 2.3250
    elif 2.8<eps<4.5:
        a4= 1.4051
    elif 4.5<eps<6.2:
        a4= -0.5119
    else:
        a4= 0.3590
    return a4

def fn_b1(eps):
    if eps<1.065:
        b1= -0.7670
    elif 1.065<eps<1.230:
        b1= -0.2054
    elif 1.230<eps<1.5:
        b1= 0.2782
    elif 1.5<eps<1.95:
        b1= 0.7234
    elif 1.95<eps<2.8:
        b1= 0.2937
    elif 2.8<eps<4.5:
        b1= 0.2875
    elif 4.5<eps<6.2:
        b1= -0.3000
    else:
        b1= -0.3250
    return b1

def fn_b2(eps):
    if eps<1.065:
        b2= 0.0007
    elif 1.065<eps<1.230:
        b2= 0.0367
    elif 1.230<eps<1.5:
        b2= -0.1812
    elif 1.5<eps<1.95:
        b2= -0.6219
    elif 1.95<eps<2.8:
        b2= 0.0496
    elif 2.8<eps<4.5:
        b2= -0.5328
    elif 4.5<eps<6.2:
        b2= 0.1922
    else:
        b2= 0.1156
    return b2

def fn_b3(eps):
    if eps<1.065:
        b3= 1.2734
    elif 1.065<eps<1.230:
        b3= -3.9128
    elif 1.230<eps<1.5:
        b3= -4.5000
    elif 1.5<eps<1.95:
        b3= -5.6812
    elif 1.95<eps<2.8:
        b3= -5.6812
    elif 2.8<eps<4.5:
        b3= -3.8500
    elif 4.5<eps<6.2:
        b3= 0.7023
    else:
        b3= 0.7781
    return b3

def fn_b4(eps):
    if eps<1.065:
        b4= -0.1233
    elif 1.065<eps<1.230:
        b4= 0.9156
    elif 1.230<eps<1.5:
        b4= 1.1766
    elif 1.5<eps<1.95:
        b4= 2.6297
    elif 1.95<eps<2.8:
        b4= 1.8415
    elif 2.8<eps<4.5:
        b4= 3.3750
    elif 4.5<eps<6.2:
        b4= -1.6317
    else:
        b4= 0.0025
    return b4

def fn_c1(eps):
    if eps<1.065:
        c1= 2.8000
    elif 1.065<eps<1.230:
        c1= 6.9750
    elif 1.230<eps<1.5:
        c1= 24.7219
    elif 1.5<eps<1.95:
        c1= 33.3389
    elif 1.95<eps<2.8:
        c1= 21.0000
    elif 2.8<eps<4.5:
        c1= 14.0000
    elif 4.5<eps<6.2:
        c1= 19.0000
    else:
        c1= 31.0625
    return c1

def fn_c2(eps):
    if eps<1.065:
        c2= 0.6004
    elif 1.065<eps<1.230:
        c2= 0.1774
    elif 1.230<eps<1.5:
        c2= -13.0812
    elif 1.5<eps<1.95:
        c2= -18.3000
    elif 1.95<eps<2.8:
        c2= -4.7656
    elif 2.8<eps<4.5:
        c2= -0.9999
    elif 4.5<eps<6.2:
        c2= -5.0000
    else:
        c2= -14.5000
    return c2

def fn_c3(eps):
    if eps<1.065:
        c3= 1.2375
    elif 1.065<eps<1.230:
        c3= 6.4477
    elif 1.230<eps<1.5:
        c3= -37.7000
    elif 1.5<eps<1.95:
        c3= -62.2500
    elif 1.95<eps<2.8:
        c3= -21.5906
    elif 2.8<eps<4.5:
        c3= -7.1406
    elif 4.5<eps<6.2:
        c3= 1.2438
    else:
        c3= -46.1148
    return c3

def fn_c4(eps):
    if eps<1.065:
        c4= 1.0000
    elif 1.065<eps<1.230:
        c4= -0.1239
    elif 1.230<eps<1.5:
        c4= 34.8438
    elif 1.5<eps<1.95:
        c4= 52.0781
    elif 1.95<eps<2.8:
        c4= 7.2492
    elif 2.8<eps<4.5:
        c4= 7.5469
    elif 4.5<eps<6.2:
        c4= -1.9094
    else:
        c4= 55.3750
    return c4

def fn_d1(eps):
    if eps<1.065:
        d1= 1.8734
    elif 1.065<eps<1.230:
        d1= -1.5798
    elif 1.230<eps<1.5:
        d1= -5.0000
    elif 1.5<eps<1.95:
        d1= -3.5000
    elif 1.95<eps<2.8:
        d1= -3.5000
    elif 2.8<eps<4.5:
        d1= -3.4000
    elif 4.5<eps<6.2:
        d1= -4.0000
    else:
        d1= -7.2312
    return d1

def fn_d2(eps):
    if eps<1.065:
        d2= 0.6297
    elif 1.065<eps<1.230:
        d2= -0.5081
    elif 1.230<eps<1.5:
        d2= 1.5218
    elif 1.5<eps<1.95:
        d2= 0.0016
    elif 1.95<eps<2.8:
        d2= -0.1554
    elif 2.8<eps<4.5:
        d2= -0.1078
    elif 4.5<eps<6.2:
        d2= 0.0250
    else:
        d2= 0.4050
    return d2

def fn_d3(eps):
    if eps<1.065:
        d3= 0.9738
    elif 1.065<eps<1.230:
        d3= -1.7812
    elif 1.230<eps<1.5:
        d3= 3.9229
    elif 1.5<eps<1.95:
        d3= 1.1477
    elif 1.95<eps<2.8:
        d3= 1.4062
    elif 2.8<eps<4.5:
        d3= -1.0750
    elif 4.5<eps<6.2:
        d3= 0.3844
    else:
        d3= 13.3500
    return d3

def fn_d4(eps):
    if eps<1.065:
        d4= 0.2809
    elif 1.065<eps<1.230:
        d4= 0.1080
    elif 1.230<eps<1.5:
        d4= -2.6204
    elif 1.5<eps<1.95:
        d4= 0.1062
    elif 1.95<eps<2.8:
        d4= 0.3988
    elif 2.8<eps<4.5:
        d4= 1.5702
    elif 4.5<eps<6.2:
        d4= 0.2656
    else:
        d4= 0.6234
    return d4

def fn_e1(eps):
    if eps<1.065:
        e1= 0.0356
    elif 1.065<eps<1.230:
        e1= 0.2624
    elif 1.230<eps<1.5:
        e1= -0.0156
    elif 1.5<eps<1.95:
        e1= 0.4659
    elif 1.95<eps<2.8:
        e1= 0.0032
    elif 2.8<eps<4.5:
        e1= -0.0672
    elif 4.5<eps<6.2:
        e1= 1.0468
    else:
        e1= 1.5000
    return e1

def fn_e2(eps):
    if eps<1.065:
        e2= -0.1246
    elif 1.065<eps<1.230:
        e2= 0.0672
    elif 1.230<eps<1.5:
        e2= 0.1597
    elif 1.5<eps<1.95:
        e2= -0.3296
    elif 1.95<eps<2.8:
        e2= 0.0766
    elif 2.8<eps<4.5:
        e2= 0.4016
    elif 4.5<eps<6.2:
        e2= -0.3788
    else:
        e2= -0.6426
    return e2

def fn_e3(eps):
    if eps<1.065:
        e3= -0.5718
    elif 1.065<eps<1.230:
        e3= -0.2190
    elif 1.230<eps<1.5:
        e3= 0.4199
    elif 1.5<eps<1.95:
        e3= -0.0876
    elif 1.95<eps<2.8:
        e3= -0.0656
    elif 2.8<eps<4.5:
        e3= 0.3017
    elif 4.5<eps<6.2:
        e3= -2.4517
    else:
        e3= 1.8564
    return e3

def fn_e4(eps):
    if eps<1.065:
        e4= 0.9938
    elif 1.065<eps<1.230:
        e4= -0.4285
    elif 1.230<eps<1.5:
        e4= -0.5562
    elif 1.5<eps<1.95:
        e4= -0.0329
    elif 1.95<eps<2.8:
        e4= -0.1294
    elif 2.8<eps<4.5:
        e4= -0.4844
    elif 4.5<eps<6.2:
        e4= 1.4656
    else:
        e4= 0.5636
    return e4

def variableselect(E_ed,E_Es,Z,m,E_es0):
    Z=math.radians(Z)
    eps=fn_eps(E_ed,E_es,Z)
    delta=fn_del(m,E_ed,E_es0)
    a=(fn_a1(eps)+(fn_a2(eps)*Z)+delta*(fn_a3(eps)+(fn_a4(eps)*Z)))
    b=(fn_b1(eps)+(fn_b2(eps)*Z)+delta*(fn_b3(eps)+(fn_b4(eps)*Z)))
    if eps<1.065:
        c=math.exp((delta*(2.8+(0.6004*Z)))**(1.2375))-1
        d=(-1*math.exp(delta*(1.8734+(0.6297*Z))))+0.9738+(delta*0.2809)
    else:
        c=(fn_c1(eps)+(fn_c2(eps)*Z)+delta*(fn_c3(eps)+(fn_c4(eps)*Z)))
        d=(fn_d1(eps)+(fn_d2(eps)*Z)+delta*(fn_d3(eps)+(fn_d4(eps)*Z)))
    e=(fn_e1(eps)+(fn_e2(eps)*Z)+delta*(fn_e3(eps)+(fn_e4(eps)*Z)))
    return a,b,c,d,e


def main(alt_deg,az_deg,Lz,a,b,c,d,e): #alt_deg = Solar Altitude | az1_deg = Solar Azimuth
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
        fkappa = 1+(c*(math.exp(d*kappa)))+(e*(math.cos(kappa))**2)
        fZs = 1+(c*(math.exp(d*Zs)))+(e*(math.cos(Zs))**2)
        r_gradation = phyZ/phy0
        r_indicatrix = fkappa/fZs
        ratio = r_indicatrix*r_gradation
        Ldes = Lz * ratio
#        print Ldes
        patch_lum[i]=Ldes
#    print patch_lum
    return patch_lum

if True:
#Dh (or E_ed) is Horizontal Diffuse Radiation, I (or E_es) is Direct Normal Radiation, Z is solar zenith angle (degrees)
#m is optical air mass, E_ed (or Dh) is Horizontal Difuse Radiation, and E_es0 is normal incident extraterrestrial irradiance
    sunAltitude = 30 if sunAltitude is None else float(sunAltitude)
    sunAzimuth = 0 if sunAzimuth is None else float(sunAzimuth)
    Zen_Lum_Lz = 10000 if Zen_Lum_Lz is None else float(Zen_Lum_Lz)
    HorzDiffRad = 300 if HorzDiffRad is None else float(HorzDiffRad)
    DirNormRad = 500 if DirNormRad is None else float(DirNormRad)
    OptAirMass=2 if OptAirMass is None else float(OptAirMass)
    NormExIrrad=1300 if NormExIrrad is None else float(NormExIrrad)
    E_ed=float(HorzDiffRad)
    E_es=float(DirNormRad)
    Z=math.radians(90-sunAltitude)
    m=float(OptAirMass)
    E_es0=float(NormExIrrad)
    a,b,c,d,e=variableselect(E_ed,E_es,Z,m,E_es0)
    result=main(sunAltitude,sunAzimuth,Zen_Lum_Lz,a,b,c,d,e)
    matrix_out=result
#    print a,b,c,d,e
#    result=imac(my_file,category,hourly,DOY)
#    out_type,band,plus,minus=result
ReadMe="INPUTS:\nsunAltitude: Solar Altitude angle at the specific HOY (output from SCALE_SunPos) "+ \
"Default is 30 (from horizon)\nsunAzimuth: The azimuth angle of sun at the specific HOY (output from SCALE_SunPos); Default is 0 (south)\n"+ \
"Zen_Lum_Lz: Zenith Luminance in Cd/m2 (connect output 20 of SCALE_OpenEPW); Default is 10000.\nHorzDiffRad: Horizontal Difuse Radiation (connect output 16 of SCALE_OpenEPW); Default is 300\n"+ \
"DirNormRad: Direct Normal Radiation (connect output 15 of SCALE_OpenEPW); Default is 500.\nOptAirMass: Optical Air Mass [Turbidity -1](Aerosol Optical Depth is output 15 of SCALE_OpenEPW); Default is 2.\n"+ \
"NormExIrrad: normal incident extraterrestrial irradiance (connect output 12 of SCALE_OpenEPW); Default is 1300.\n"+ \
"OUTPUT:\nmatrix_out: The generated luminance matrix. FLATTEN this output for optima."
