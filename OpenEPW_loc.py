"""
Extract location, latitude, longitude, timezone and elevation data from EPW files.
--
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LOCI, UCLouvain.
    Inputs:
        epwFile: connect the epw file here
    Output:
        name: Name of the recording station/City.
        latitude: Latitude of the location.
        longitude: Longitude of the location.
        timeZone: What timezone the location lies on, with respect to UTC
        elevation: Location's elevation above mean sea level."""
self=ghenv.Component
self.Name = "SCALE_OpenEPW_loc"
self.NickName = 'OpenEPW_loc'
self.Message = 'OWL 0.0.01\nOct_15_2021'
self.IconDisplayMode = self.IconDisplayMode.application
self.Category = "SCALE"
self.SubCategory = "1 OWL::Common"
try: self.AdditionalHelpFromDocStrings = "1"
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

def main():
    with open(epwFile, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            rows.append(row)
    for row in rows[0:1]:
        name = row[1]
        latitude = row[6]
        longitude=row[7]
        timeZone=row[8]
        elevation=row[9]
    return name, latitude, longitude, timeZone, elevation
    
if True:
    fields = []
    rows = []
    result=main()
    name, latitude, longitude, timeZone, elevation=result