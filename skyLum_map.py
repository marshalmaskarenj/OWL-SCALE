# -*- coding: utf-8 -*-
""" 
Python Script
Created on  Saturday October 2021 07:36:43 
@author:  Marshal 

[desc]
SCALE_skyLum_map | skyLum_map
This component visualises sky-luminance distribution on the skydome, from the output matrices of CIE_Skygen or PerezSky components.
IMPORTANT: this component uses Python elements that are not supported by Grassshopper Python by default, and needs to use an external instance of Python 2.7. It is important to install Numpy, csv, scipy, os and matplotlib modules in the external python 2.7 using pip.
This also needs a region_mask file (such as tregenza_circular.mat) as input along with the matrix of 145 datapoints.
TOP indicates north, RIGHT indicates east
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LOCI, UCLouvain.
[/desc]

ARGUMENTS:
----------
<inp> 
    matrix_out : An array of 145 datapoints that represent luminance at the 145 Tregenza (continuous) patches. Takes input from CIE_Skygen or PerezSky components.
</inp>
<inp>
    region_mask: A file of <.mat> format that includes tregenza-discretised 145 mask layer data (such as tregenza_circular.mat). Must be provided with this module. Can also choose other custom masks.
</inp>
<inp>
    folder: Specify location where the simulated data needs to be stored. It is a folder/directory path.
</inp>
<inp>
    runIt: A Boolean toggle set to "True" to start the simulation.
</inp>
RETURN:
----------
    <out>
        sky_map : Location of the skymap file as PNG. Connect this to LB imageviewer for visualisation.
    </out>

"""

import numpy as np
np.seterr(divide='ignore', invalid='ignore')
import csv 
import scipy.io as sio
import os 
import matplotlib.pyplot as plt 
plt.style.use('seaborn-darkgrid')
import math

if runIt:
    regionfile=region_mask
    data_region = sio.loadmat(regionfile)
    mask_patch=data_region["mask_patch_all"]
    mask_patch=np.float32(mask_patch)
    matrixval=matrix_out
    
    region_data_all=np.zeros(shape=(300,300),dtype=np.float32)
    for i in range (0,145,1):
        mask_data=mask_patch[:,:,i]
        lumsumval=matrixval[i]
        region_data=lumsumval*mask_data
        region_data_all=region_data_all+region_data
    plt.imshow(region_data_all, cmap='inferno', alpha=0.95)
    plt.colorbar()
    plt.axis('off')
    plt.savefig(folder+'/sky_lumin_Map.png', bbox_inches='tight', pad_inches = 0)
    plt.close()
    sky_map=str(folder)+'\sky_lumin_Map.png'
else:
    print "Set runIt to True!"