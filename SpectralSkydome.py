"""
Spectral skydome: this converts the luminance output from direct sky (145 datapoints corresponding to each discretized patch) into respective CCT value and model selection.
Luminance data can be either from CIE_Skygen, or PerezSky components. 
For connecting the direct sky luminance output from simulated data using HDR2DiscreteLumEx, use SpectralViewdome.
Refer to https://doi.org/10.1177%2F1477153520982265 by Diakite-Kortlever and Knoop 2021 for more about this component.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LOCI, UCLouvain.
    Inputs:
        matrix_out: output from CIE_skygen component (an array of 145 values). (If lm<250: lm=250). 
    Output:
        m_out: The array of sky-lum data.
        m_CCT: The array of spectal data.
        m_model: The array of model selected each patch (1 = Chain 1999, 2 = rusnak 2014 CIE12, 3=chain 2004"""

import rhinoscriptsyntax as rs
import math
self=ghenv.Component
self.Name = "SCALE_Spectral_Skydome"
self.NickName = 'SpectralSkydome'
self.Message = 'OWL 0.0.01\nOCT_15_2021'
self.IconDisplayMode = self.IconDisplayMode.application
self.Category = "SCALE"
self.SubCategory = "2a OWL::Sky"
try: self.AdditionalHelpFromDocStrings = "1"
except: pass

def main(matrix_out):
    matrix_out=[float(i) for i in matrix_out]
    matrix_out=[int(i) for i in matrix_out]
    m_out=[(0*1) for i in range(145)]
    matCCT=[(0*1) for i in range(145)]
    selectmodel=[(0*1) for i in range(145)]
    for i in range (0,145,1):
        if float(matrix_out[i])<250:
            mval=250
            CCT=mchain99(mval)
            mdl=1
        elif 250<float(matrix_out[i])<3172:
            mval=float(matrix_out[i])
            CCT=mchain99(float(matrix_out[i]))
            mdl=1
        elif 3172<float(matrix_out[i])<5200:
            mval=float(matrix_out[i])
            CCT=mrusnak(float(matrix_out[i]))
            mdl=2
        elif float(matrix_out[i])>5200:
            mval=float(matrix_out[i])
            CCT=mchain04(float(matrix_out[i]))
            mdl=3
        else:
            mval=float(matrix_out[i])
            CCT=5000
            mdl=0
        m_out[i]=int(mval)
        matCCT[i]= int(CCT)
        selectmodel[i]=int(mdl)
    return m_out, matCCT, selectmodel

def mtakagi(lum):
    CCT=6500+((1.1985*10**8)/(lum**1.2))
    return CCT

def mchain99(lum):
    CCT=(10**6)/(-132.1+59.77*math.log10(lum))
    return CCT

def mchain04(lum):
    LCF=120
    CCT=(10**6)/(181.35233+LCF*(-4.22630+math.log10(lum)))
    return CCT

def mrusnak(lum):
    p=10.2
    q=0.26
    CCT=(10**6)/(p*(lum**q))
    return CCT

if True:
    matrix_out=[] if matrix_out is None else matrix_out
    m_out,m_CCT,m_model=main(matrix_out)