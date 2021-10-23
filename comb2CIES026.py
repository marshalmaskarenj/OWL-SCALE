"""
This component converts 2nm-binned relative-combined SPD data to bins of 10nm.
Works in conjunction with SCALE_RelativeCombinedSPD and SCALE_CIES026_aopic components.
--
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LOCI, UCLouvain.
    Inputs:
        Rel_Comb_SPD2: Output from SCALE_RelativeCombinedSPD component: 176 values for 2nm bins between 380-730nms.
    Output:
        Rel_Comb_SPD10: 10nm binned data for wavelength and respective SPD as input for alpha-opic (CIES026) components."""

self=ghenv.Component
self.Name = "SCALE_comb2CIES026"
self.NickName = 'comb2CIES026'
self.Message = 'OWL 0.0.01\nOCT_15_2021'
self.IconDisplayMode = self.IconDisplayMode.application
self.Category = "SCALE"
self.SubCategory = "3 OWL::Spectral"
try: self.AdditionalHelpFromDocStrings = "2"
except: pass

import rhinoscriptsyntax as rs
import math
SPD_arr=Rel_Comb_SPD2
SPD_half_arr=[([None]*1) for xx in range(36)]
#print SPD_half_arr
wav_arr=[300,310,320,330,340,350,360,370,380,390,400,410,420,430,440,450,460,470,480,490,500,510,520,530,540,550,560,570,580,590,600,610,620,630,640,650,660,670,680,690,700,710,720,730,740,750,760,770,780,790,800,810,820,830]
for i in range (0,176,1):
    j=int(math.ceil(i/5))
    matval=float(SPD_arr[i])
    matval=round(matval,6)
    SPD_half_arr[j]=str(wav_arr[j+8])+"\t"+str(matval)
prev_arr=[([None]*1) for xx in range(8)]
late_arr=[([None]*1) for xx in range(10)]
for i in range (0,8,1):
    zval=0
    prev_arr[i]=str(wav_arr[i])+"\t"+str(zval)
for i in range (0,10,1):
    zval=0
    late_arr[i]=str(wav_arr[i+44])+"\t"+str(zval)
Rel_Comb_SPD10=prev_arr+SPD_half_arr+late_arr