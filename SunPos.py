"""
Computes Solar altitudinal/azimuthal positions; tailored for OWL workflow.
--
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LOCI, UCLouvain.
    Inputs:
        latitude: Latitude in degrees (-90 to +90). Connects to SCALE_OpenEPW_loc component.
        longitude: Longitude in degrees (0 to 360). Connects to SCALE_OpenEPW_loc component.
        timeZone: Connects to SCALE_OpenEPW_loc component.
        hour: (Hour of Day) A number between 1 and 24, indicating the hour of day (1 to 24)
        DOY: (Day of Year) The date of the calendar year, starting with 1 Jan. Eg: 1 Feb is Day 32 (1 to 365). Connects to Ladybug_DOY_HOY component.
    Outputs:
        sunAltitude: Solar altitude angle in degrees
        sunAzimuth: Solar azimuth angle in degrees"""
self=ghenv.Component
self.Name = "SCALE_SunPos"
self.NickName = 'SunPos'
self.Message = 'OWL 0.0.01\nOCT_15_2021'
self.IconDisplayMode = self.IconDisplayMode.application
self.Category = "SCALE"
self.SubCategory = "1 OWL::Common"
try: self.AdditionalHelpFromDocStrings = "2"
except: pass

import rhinoscriptsyntax as rs
import math

phi=float(latitude)
longitude=float(longitude)
UTC=float(timeZone)
HOD=float(hour)
DOY=float(DOY)

delta=(-23.45)*math.cos(math.radians((360/365)*(DOY+10)))
delta_rad=math.radians(delta)
phi_rad=math.radians(phi)
B_val=math.radians((DOY-81)*(360/365))
EoT=(9.87*math.sin(2*B_val))-(7.53*math.cos(B_val))-(1.5*math.sin(B_val))
LSTM=15*(UTC)
TC_factor=4*(longitude-LSTM)+EoT
LST=float(HOD)+(TC_factor/60)
HRA=15*(LST-12)
HRA_rad=math.radians(HRA)
alpha=math.asin((math.sin(delta_rad)*math.sin(phi_rad))+(math.cos(delta_rad)*math.cos(phi_rad)*math.cos(HRA_rad)))
sunAltitude=math.degrees(alpha)
#print (sunAltitude)
azimuth=math.acos(((math.sin(delta_rad)*math.cos(phi_rad))-(math.cos(delta_rad)*math.sin(phi_rad)*math.cos(HRA_rad)))/(math.cos(alpha)))
az_deg=math.degrees(azimuth)
if HRA<0:
    sunAzimuth=az_deg
else:
    sunAzimuth=360-az_deg