"""
This component follows the LRC circadian light combined calculator (REFER TO https://www.lrc.rpi.edu/programs/lightHealth/index.asp )
The illuminance from each patch is identified by multiplying the luminance data (input) for each source (or patch of sky) with sine factor of its altitudinal/foveal angle [6...,18...,30...,.,.90], and with 0.0433 steradians (size of each tregenza patch.) 
Emulating the LRC spreadsheet, the relative SPD (input) and respective illuminance (from input lum) combines to give RELATIVE COMBINED SPD.
The cumulative [relative combined] SPD of the Skydome or of the Viewdome, from 380 to 730nm is evaluated.
Works in conjunction with CCT2SPD or ViewCCT2SPD. 145 CCT values from either of these components is taken as input, and the generated 15515 values are the expected input for this component.
--
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LOCI, UCLouvain.
    Inputs:
        SPD_5: The SPD values between 300-830nm for all 145 patches (15515 values for bins of 5nm).
        luminance: The patch luminance for the 145 patches (from CIE_Skygen or PerezSky or HDR2DiscreteLum components).
    Output:
        Rel_comb_SPD: Relative combined SPD between 380-730nm for the entire skydome on the horizontal plane, or for the viwedome on the foveal plane (176 values for 2nm bins). 
        patch_illum: Individual illuminance contributions on the horizontal or foveal plane due to all patches at various positions.
        net_illum: Net illuminance on the horizontal plane or at the eye due to all patches. """

from __future__ import division 
from __future__ import print_function
import rhinoscriptsyntax as rs
import operator
self=ghenv.Component
self.Name = "SCALE_RelativeCombinedSPD"
self.NickName = 'RelativeCombinedSPD'
self.Message = 'OWL 0.0.01\nOCT_15_2021'
self.IconDisplayMode = self.IconDisplayMode.application
self.Category = "SCALE"
self.SubCategory = "3 OWL::Spectral"
try: self.AdditionalHelpFromDocStrings = "1"
except: pass

def dotproduct(vec1, vec2, vec3):
    return sum(map(operator.mul, vec1, vec2, vec3))

def interpolate(inp, fi):
    i, f = int(fi // 1), fi % 1  # Split floating-point index into whole & fractional parts.
    j = i+1 if f > 0 else i  # Avoid index error.
    return (1-f) * inp[i] + f * inp[j]

SPD=SPD_5
num_streams=int(len(SPD)/107)
luminance = (1) if luminance is None else luminance
lum_d=luminance
strdn= 0.0433 #0.0433 steradians per division (cone with 13.5° apex angle): https://escholarship.org/content/qt7079393t/qt7079393t.pdf
sine_array=[0.104528463,0.104528463,0.104528463,0.104528463,0.104528463,0.104528463,0.104528463,0.104528463,0.104528463,0.104528463,0.104528463,0.104528463,0.104528463,0.104528463,0.104528463,0.104528463,0.104528463,0.104528463,0.104528463,0.104528463,0.104528463,0.104528463,0.104528463,0.104528463,0.104528463,0.104528463,0.104528463,0.104528463,0.104528463,0.104528463,0.309016994,0.309016994,0.309016994,0.309016994,0.309016994,0.309016994,0.309016994,0.309016994,0.309016994,0.309016994,0.309016994,0.309016994,0.309016994,0.309016994,0.309016994,0.309016994,0.309016994,0.309016994,0.309016994,0.309016994,0.309016994,0.309016994,0.309016994,0.309016994,0.309016994,0.309016994,0.309016994,0.309016994,0.309016994,0.309016994,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.669130606,0.669130606,0.669130606,0.669130606,0.669130606,0.669130606,0.669130606,0.669130606,0.669130606,0.669130606,0.669130606,0.669130606,0.669130606,0.669130606,0.669130606,0.669130606,0.669130606,0.669130606,0.669130606,0.669130606,0.669130606,0.669130606,0.669130606,0.669130606,0.809016994,0.809016994,0.809016994,0.809016994,0.809016994,0.809016994,0.809016994,0.809016994,0.809016994,0.809016994,0.809016994,0.809016994,0.809016994,0.809016994,0.809016994,0.809016994,0.809016994,0.809016994,0.913545458,0.913545458,0.913545458,0.913545458,0.913545458,0.913545458,0.913545458,0.913545458,0.913545458,0.913545458,0.913545458,0.913545458,0.978147601,0.978147601,0.978147601,0.978147601,0.978147601,0.978147601,1]
illumin_d=[(0) for i in range(num_streams)]
for i in range (0,num_streams,1):
    illumin_d[i]=lum_d[i]*sine_array[i]*strdn
patch_illum=illumin_d
total_illum=sum(illumin_d)
net_illum=total_illum

SPD_5b = [([0]*num_streams) for i in range(71)]
for i in range (0,71,1):
    for j in range (0, num_streams,1):
        SPD_5b[i][j]=SPD_5[i+16+(107*j)] # truncated between 380-730 from 300-830, thus reduced to 70+1 from 106+1 values.
inp = [[float(y) for y in x] for x in SPD_5b]
new_len=176
delta = (len(inp)-1) / (new_len-1)
outpt=[([0]*176) for i in range(num_streams)]
inpt=[([0]*71) for i in range(num_streams)]
for nn in range (0,71,1):
    for ni in range (0,num_streams,1):
        inpt[ni][nn]=inp[nn][ni]
for mm in range (0,num_streams,1):
    outpt[mm] = [interpolate(inpt[:][mm], i*delta) for i in range(new_len)]
SPD_2=outpt  # interpolated data between 380-730nm; from 5nm (70+1 values) to 2nm (175+1 values)
photopic_obs_arr=[0.000039,0.000046915,0.000057176,0.000072344,0.000093508,0.00012,0.00015149,0.00019182,0.00024691,0.00031852,0.000396,0.00047302,0.00057222,0.00072456,0.00094116,0.00121,0.0015308,0.0019353,0.0024548,0.0031178,0.004,0.0051593,0.0065462,0.0080865,0.0097677,0.0116,0.013583,0.015715,0.018007,0.020454,0.023,0.02561,0.028351,0.031311,0.034521,0.038,0.041768,0.045843,0.050244,0.054981,0.06,0.065278,0.070911,0.077016,0.083667,0.09098,0.099046,0.10788,0.11753,0.12799,0.13902,0.15047,0.16272,0.17624,0.19127,0.20802,0.22673,0.24748,0.27018,0.29505,0.323,0.35469,0.38929,0.42563,0.46339,0.503,0.54451,0.58697,0.62935,0.67088,0.71,0.74546,0.77784,0.80811,0.83631,0.862,0.88496,0.90544,0.92373,0.93992,0.954,0.96601,0.97602,0.98409,0.99031,0.99495,0.9981,0.99975,0.99986,0.99833,0.995,0.98974,0.98272,0.97408,0.96386,0.952,0.9385,0.92346,0.90701,0.8892,0.87,0.84939,0.82758,0.80479,0.78119,0.757,0.73242,0.7075,0.68222,0.65667,0.631,0.60531,0.57964,0.55396,0.52835,0.503,0.47803,0.4534,0.42908,0.40503,0.381,0.35683,0.33282,0.30934,0.28659,0.265,0.24489,0.22605,0.20816,0.19116,0.175,0.15965,0.14513,0.1315,0.11878,0.107,0.096189,0.086265,0.077121,0.06871,0.061,0.053955,0.04755,0.041759,0.036564,0.032,0.028077,0.024708,0.021801,0.019281,0.017,0.014837,0.012835,0.011068,0.0095333,0.00821,0.0070854,0.0061385,0.0053431,0.0046764,0.004102,0.0035891,0.0031341,0.0027381,0.0023932,0.002091,0.0018246,0.0015902,0.0013845,0.0012041,0.001047,0.00091111,0.00079324,0.00069008,0.0005995,0.00052]
delta_wavelength=[1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1]
SPD_2x=[[float(y) for y in x] for x in SPD_2]
array_product=[([0]*176) for i in range(num_streams)]
outpt=[([0]*176) for i in range(num_streams)]
for ij in range(0,num_streams,1):
    for ii in range(0,len(SPD_2x[0]),1):
        array_product[ij][ii]=SPD_2x[ij][ii]*photopic_obs_arr[ii]*delta_wavelength[ii]
sumproduct=[([0]*1) for i in range(num_streams)]
for i in range(0,num_streams,1):
    sumproduct[i]=sum(array_product[i])
avdata=[([0]*176) for i in range(num_streams)]
for nn in range (0, num_streams,1):
    avdata[nn]=[i * ((illumin_d[nn])/(683*(sumproduct[nn]+0.000000001))) for i in SPD_2x[nn]] # factor of 0.0000...1 added to avoid 'divide by zero' exception
sum_avdata=[sum(x) for x in zip(*avdata)]
maxval=max(sum_avdata)
norm_avdata = [x / maxval for x in sum_avdata]
Rel_comb_SPD=norm_avdata
