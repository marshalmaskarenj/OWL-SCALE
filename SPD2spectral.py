"""
SPD to Spectral weightage for RGB Channels. This component converts 2nm-separated SPDs to weightage-per-channel for spectral Radiance simulations. 
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LOCI, UCLouvain.
    Inputs:
        Rel_comb_SPD: 2nm separated SPD from 380-730nm (176 values). Takes input from RelativeCombinedSPD component.
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
import math

SPD2=Rel_comb_SPD

B_ch=[[0] for i in range (60)]
G_ch=[[0] for i in range(44)]
R_ch=[[0] for i in range(72)]
for i in range (0,60,1):
    B_ch[i]=SPD2[i]
for j in range (0,44,1):
    jj=j+60
    G_ch[j]=SPD2[jj]
for k in range (0,72,1):
    kk=k+104
    R_ch[k]=SPD2[kk]

avg_R=sum(R_ch)/97
avg_G=sum(G_ch)/44
avg_B=sum(B_ch)/60

avg_channel=[round(avg_R,4),round(avg_G,4),round(avg_B,4)]
channel_output=avg_channel
