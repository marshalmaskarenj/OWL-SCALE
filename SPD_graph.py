# -*- coding: utf-8 -*-
""" 
Python Script
Created on  Saturday October 2021 07:36:43 
@author:  Marshal 

[desc]
SCALE_SPD_graph | SPD_graph
A simple component to plot the SPD curve between 380-730nm with 2nm bins, from the output data of RelativeCombinedSPD component
IMPORTANT: this component uses Python elements that are not supported by Grassshopper Python by default, and needs to use an external instance of Python 2.7. It is important to install Numpy, csv, scipy, os and matplotlib modules in the external python 2.7 using pip.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LOCI, UCLouvain.
[/desc]

ARGUMENTS:
----------
<inp> 
    Rel_comb_SPD : Relative combined SPD between 380-730nm for the entire skydome on the horizontal plane, or for the viwedome on the foveal plane (176 values for 2nm bins). Connect to the output of RelativeCombinedSPD component.
</inp>
<inp>
    skyORview: A boolean, set to False for sky SPD and True for View SPD.
</inp>
<inp>
    folder: Specify location where the plot needs to be stored. It is a folder/directory path.
</inp>
<inp>
    runIt: A Boolean toggle set to "True" to start the simulation.
</inp>
RETURN:
----------
    <out>
        SPD_graph : Location of the SPD graph plot (for sky or for view) file as PNG. Connect this to LB imageviewer for visualisation.
    </out>

"""

import numpy as np
np.seterr(divide='ignore', invalid='ignore')
import matplotlib.pyplot as plt 
plt.style.use('dark_background')
import math

if runIt:
    if skyORview is True:
        titstr="ViewSPD"
    else:
        titstr="SkySPD"
    x_dim=np.linspace(380,730,176)
    y_dim=Rel_comb_SPD
    max_y=y_dim.index(max(y_dim))
    max_x=int(x_dim[max_y])
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(x_dim,y_dim, color='white', label='Sine wave')
    ax.set_title(str(titstr) +" (peak at "+str(max_x)+"nm)", fontsize=32)
    ax.set_xlabel('Wavelength', fontsize=32)
    ax.set_ylabel('Rel Comb SPD', fontsize=32)
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(20)
    plt.savefig(folder+str(titstr)+'_graph.png')
    plt.close()
    SPD_graph=str(folder)+str(titstr)+'_graph.png'
    print (titstr)
else:
    print "Set runIt to True!"