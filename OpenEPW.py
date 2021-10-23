"""
Helps deconstruct EPW file into required components.
--
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LOCI, UCLouvain.
    Inputs:
        epwFile: connect the epw file here
        output_index: connect panel to {index_list} to see list of indices [between 1 and 35].
        hour_of_year: define the hour of the year here [between 1 and 8760].
    Output:
        data: The output data, depending on output_index.
        dtype: What data is being fetched.
        index_list: connect panel to see possible indices."""
self=ghenv.Component
self.Name = "SCALE_OpenEPW"
self.NickName = 'OpenEPW'
self.Message = 'OWL 0.0.01\nOCT_15_2021'
self.IconDisplayMode = self.IconDisplayMode.application
self.Category = "SCALE"
self.SubCategory = "1 OWL::Common"
try: self.AdditionalHelpFromDocStrings = "3"
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

def main(hour_of_year,output_index):
    index_list = " 1. Year \n 2. Month \n 3. Day \n 4. Hour \n 5. Minute \n 6. Data Source and Uncertainty Flags \n 7. Dry Bulb Temp \n 8. Dew pt temp \n 9. Rel Humidity \n 10. Atmospheric Station Pressure\
    \n 11. Extraterrestial Horizontal Radiation \n 12. Extraterrestrial Direct Normal Radiation \n 13. Horizontal Infrared Radiation Intensity \n 14. Global Horizontal Radiation \n 15. Direct Normal Radiation\
    \n 16. Diffuse Horizontal Radiation \n 17. Global Horizontal Illuminance \n 18. Direct Normal Illuminance \n 19. Diffuse Horizontal Illuminance \n 20. Zenith Luminance \n 21. Wind Direction\
    \n 22. Wind Speed \n 23. Total Sky Cover \n 24. Opaque Sky Cover \n 25. Visibility \n 26. Ceiling Height \n 27. Present Weather Observation \n 28. Present Weather Codes \n 29. Precipitable Water\
    \n 30. Aerosol Optical Depth \n 31. Snow Depth \n 32. Days Since Last Snowfall \n 33. Albedo \n 34. Liquid Precipitation Depth \n 35. Liquid Precipitation Quantity"
    
    with open(epwFile, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            rows.append(row)
    for row in rows[hour_of_year:hour_of_year+1]:
        data = row[output_index]
    datalist=["Year","Month","Day","Hour","Minute","Data_Source_and_Uncertainty_Flags","Dry_Bulb_Temp","Dew_pt_temp","Rel_Humidity","Atmospheric_Station_Pressure",\
"Extraterrestial_Horizontal_Radiation","Extraterrestrial_Direct_Normal_Radiation","Horizontal_Infrared_Radiation_Intensity","Global_Horizontal_Radiation",\
"Direct_Normal_Radiation","Diffuse_Horizontal_Radiation","Global_Horizontal_Illuminance","Direct_Normal_Illuminance","Diffuse_Horizontal_Illuminance",\
"Zenith_Luminance","Wind_Direction","Wind_Speed","Total_Sky_Cover","Opaque_Sky_Cover","Visibility","Ceiling_Height","Present_Weather_Observation",\
"Present_Weather_Codes","Precipitable_Water","Aerosol_Optical_Depth","Snow_Depth","Days_Since_Last_Snowfall","Albedo","Liquid_Precipitation_Depth",\
"Liquid_Precipitation_Quantity"]
    dtype = datalist[output_index]
    return data, dtype, index_list
    
if True:
    output_index=1 if output_index is None else int(output_index)-1
    hour_of_year=0 if hour_of_year is None else int(hour_of_year)+7
    fields = []
    rows = []
#    print main(hour_of_year, output_index)
    result=main(hour_of_year,output_index)
    data,dtype,index_list=result
    ReadMe="INPUTS:\nepwFile: connect the epw file here.\noutput_index: connect panel to {index_list} to see list of indices [between 1 and 35].\nhour_of_year: define the hour of the "+ \
"year here [between 1 and 8760].\nOUTPUTS:\ndata: The output data, depending on output_index.\ndtype: What data is being fetched.\nindex_list: connect panel to see possible indices."