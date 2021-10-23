# -*- coding: utf-8 -*-
""" 
Python Script
Created on  Wednesday September 2021 12:56:51 
@author:  Marshal 

[desc]
SCALE_HDR2DiscreteLumEx | HDR2DiscreteLumEx
This component breaks down luminance to 145 components in the view of the observer.
The HDR luminance image generated by the image-based simulation needs to be attached to the input, along with the .mat file of masks for each of the discretised view patches (must be provided) and the mask file for view-field: fisheye/binocular/human-vision (must be provided).
The generated outputs includes the masked HDR image, and a matrix of 145 averaged luminance values to be used for the "alpha-opic metric recipe" ( <SpectralSky> + <CCT2SPD> + <cumulativeSPD> + <cumulative2spectral> + <CIE026_(alpha)opic-(ir)rad> ).
IMPORTANT: this component uses Python elements that are not supported by Grassshopper Python by default, and needs use an external instance of Python 2.7. It is important to install Numpy, csv, scipy, os and matplotlib modules in the external python 2.7 using pip.
Radiance needs to be installed on system with Path defined, so it is accessible via Command Prompt (CMD). Test the pvalue command <<"pvalue -o +u -h -H HDR_file > output.txt">> on CMD prior to this component, since this uses os to call Radiance pvalue for converting HDR to <luminance/179> data.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LOCI, UCLouvain.
[/desc]

ARGUMENTS:
----------
<inp> 
    HDR_file: The "luminance_file" generated from HoneyBee runDaylightAnalysis: an HDR file that includes luminance data from the view position.
</inp>
<inp>
    region_mask: A file of <.mat> format that includes tregenza-discretised 145 mask layer data. Must be provided with this module. Can also choose tregenza-continuous or other masks.
</inp>
<inp>
    view_mask: Viewing regions, an option between binocular/human-vision/fisheye. A file of <.mat> format. Must be provided with this module.
</inp>
<inp>
    folder: Specify location whre the simulated data neesd to be stored. It is a folder/directory path.
</inp>
<inp>
    runIt: A Boolean toggle set to "True" to start the simulation.
</inp>

RETURN:
----------
    <out>
        matrix_out : Averaged luminance data of the 145 view angles. This goes to the alpha-opic metrics-recipe.
    </out>
    <out>
        masked_image: A masked HDR image.
    </out>
    <out>
        region_lum: averaged-luminance for each view region.
    </out>


"""

import numpy as np #=sc.sticky['numpy']
np.seterr(divide='ignore', invalid='ignore')
import csv #=sc.sticky['csv']
import scipy.io as sio#=sc.sticky['scipy.io']
import os #=sc.sticky['os']
import matplotlib.pyplot as plt #=sc.sticky['matplotlib.pyplot']
plt.style.use('seaborn-darkgrid')
import math

if runIt:
    regionfile=region_mask
    viewfile=view_mask 
    data_region = sio.loadmat(regionfile)
    mask_patch=data_region["mask_patch_all"]
    mask_patch=np.float32(mask_patch)
    data_view = sio.loadmat(viewfile)
    mask_view=data_view['maskdata']
    mask_view=np.float32(mask_view)
    folder=folder
    
    os.system("pvalue -pR -d -o +u -h -H "+HDR_file+" >"+folder+"output_r.txt")
    os.system("pvalue -pG -d -o +u -h -H "+HDR_file+" >"+folder+"output_g.txt")
    os.system("pvalue -pB -d -o +u -h -H "+HDR_file+" >"+folder+"output_b.txt")
    file_r=folder+"output_r.txt"
    file_g=folder+"output_g.txt"
    file_b=folder+"output_b.txt"
    with open(file_r, 'r') as file:
        data_r1 = file.read()
        data_r2=data_r1.replace(' ','')
        data_r=data_r2.split('\n')
    with open(file_g, 'r') as file:
        data_g1 = file.read()
        data_g2=data_g1.replace(' ','')
        data_g=data_g2.split('\n')
    with open(file_b, 'r') as file:
        data_b1 = file.read()
        data_b2=data_b1.replace(' ','')
        data_b=data_b2.split('\n')
    data_r.pop()
    data_g.pop()
    data_b.pop()
    r_arr2=[data_r[i:i+300] for i in range(0, len(data_r), 300)]
    g_arr2=[data_g[i:i+300] for i in range(0, len(data_g), 300)]
    b_arr2=[data_b[i:i+300] for i in range(0, len(data_b), 300)]
    arr_pic_2 = [(([0]*300) for i in range(300))for j in range(3)]
    r_arr3=[[0.299*179*float(i) for i in j] for j in r_arr2]
    g_arr3=[[0.587*179*float(i) for i in j] for j in g_arr2]
    b_arr3=[[0.114*179*float(i) for i in j] for j in b_arr2]
    gray_img=[[a+b+c for a,b,c in zip(i,j,k)] for i,j,k in zip(r_arr3,g_arr3,b_arr3)]
    gray_image=np.asarray(gray_img)
    xxa = np.linspace(0, 1, 300)
    yya = np.linspace(0, 1, 300)
    Xa, Ya = np.meshgrid(xxa, yya)
    contours = plt.contour(Xa, -Ya, gray_img, colors='black')
    plt.contourf(Xa, -Ya, gray_image, 1000, cmap='inferno', alpha=0.5)
    plt.clabel(contours, inline=True, fontsize=8)
    plt.colorbar()
    plt.axis('off')
    plt.savefig(folder+'/gray-luminanceMap.png', bbox_inches='tight', pad_inches = 0)
    plt.close()
    
    lum_data_all=np.zeros(shape=(300,300),dtype=np.float32)
    region_data_all=np.zeros(shape=(300,300),dtype=np.float32)
    lldata=[]
    for i in range (0,145,1):
        mask_data=mask_patch[:,:,i]
        fnm=str(i+1)
        lum_data_temp=np.multiply(gray_image,mask_data)
        lum_data=np.multiply(lum_data_temp,mask_view)
        lum_data_all=lum_data_all+lum_data
        lum_sum=np.sum(np.sum(lum_data))
        lumsum=(lum_sum/295) # 295 because there are ~295 pixels per masked region of tregenza 
        region_data=lumsum*mask_data
        region_data_all=region_data_all+region_data
        lldata.append(lumsum)
    plt.imshow(lum_data_all, cmap='inferno', alpha=0.95)
    plt.colorbar()
    plt.axis('off')
    plt.savefig(folder+'/masked-luminanceMap.png', bbox_inches='tight', pad_inches = 0)
    plt.close()
    plt.imshow(region_data_all, cmap='inferno', alpha=0.95)
    plt.colorbar()
    plt.axis('off')
    plt.savefig(folder+'/zone_averaged-luminanceMap.png', bbox_inches='tight', pad_inches = 0)
    plt.close()
    lumin_map=str(folder)+'\gray-luminanceMap.png'
    masked_image=str(folder)+'\masked-luminanceMap.png'
    region_lum=str(folder)+'\zone_averaged-luminanceMap.png'
    #print(lldata)
    matrix_out=lldata
else:
    print "Set runIt to True!"