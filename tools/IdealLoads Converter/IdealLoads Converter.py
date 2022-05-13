"""
Functions to convert IDFs with complex HVAC systems to create IDF versions with Ideal Loads Systems.

Use these functions:
to delete complex HVAC objects in IDF files,
to delete complex HVAC objects in IDF files without intervening the DHW connections,
to create new Ideal Loads objects,
to fill out missing fields in new Ideal Loads objects with the values from the original complex HVAC IDFs

Copyright: Sahin AKIN, 2022
Version 2.0
"""

import os
from eppy.modeleditor import IDF
from functools import reduce

# Make sure that you have selected the correct working directory (BUILDME)
# Standalone Run Requirements
ep_version = '9.2.0'
path_parent = os.path.dirname(os.getcwd())
os.chdir(path_parent)
basepath = os.path.abspath('..')
ep_path = os.path.abspath("..\\bin\\EnergyPlus-9-2-0")
ep_idd = os.path.abspath("..\\bin\\EnergyPlus-9-2-0\\Energy+.idd")
IDF.setiddname(ep_idd)


def delete_cmplx_HVAC(originalidf_path,savefolder_path):
    """
    Deletes All HVAC fields
    It is useful if there is no DHW system modeled in the IDF file

    :param originalidf_path: Path for the original IDF with a complex HVAC data
    :return: savefolder_path: Path to use where all converted files will be saved
    """
    # Backup
    originalidf = IDF(originalidf_path)
    building=originalidf.idfobjects["Building".upper()][0].Name
    originalidf.saveas(f"{savefolder_path}\\{building}_BuildME_interim.idf")
    idf=IDF(f"{savefolder_path}\\{building}_BuildME_interim.idf")

    # Lets find out all available keys in the IDF file
    allkeys = idfobjectkeys(idf)

    # Getting all possible HVAC-related keys by filtering...
    HVAC_related_list= allkeys[allkeys.index('HVACTEMPLATE:THERMOSTAT'):]
    HVAC_related_list = HVAC_related_list[:HVAC_related_list.index('MATRIX:TWODIMENSION')]

    # Deleting all HVAC and DHW objects in our filtered list
    for HVAC_obj in HVAC_related_list:
        idf.removeallidfobjects(HVAC_obj)

    idf.saveas(f"{savefolder_path}\\{building}_BuildME_cleaned.idf")
    editedidf=idf

    return editedidf


def idfobjectkeys(idf):
    """
    Returns the object keys in the order they were in the IDD file
    It is an ordered list
    :param: idf: idf file"""
    return idf.model.dtls

def colored(r, g, b, text):
    """
    Assigns color to terminal text based on given rgb values
    :param r:
    :param g:
    :param b:
    :param text:
    :return:
    """
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)

def delete_cmplx_HVAC_keep_DHW(originalidf_path,savefolder_path):
    """
    An advanced automatic version of the delete_cmplx_HVAC() in version 1.0.
    Now it is possible to seperate DHW and HVAC systems without manual intervention
    The only requirement is that DHW elements should have an identifier, or common string throughout.
    This could be "DHW" or "SHW" or any other string portion that is used repeatedly in all DHW objects.

    Run Order:
    1) Identify HVAC keys in IDF
    2) Getting objects from the HVAC keys
    3) Searching for DHW objects
    4) Deleting all HVAC keys
    5) Recreating DHW objects and defining into the IDF

    :param originalidf_path: Path for the original IDF with a complex HVAC data
    :param savefolder_path: Path to use where all converted files will be saved
    :return:
    """

    # Backup
    originalidf = IDF(originalidf_path)
    building=originalidf.idfobjects["Building".upper()][0].Name
    originalidf.saveas(f"{savefolder_path}\\{building}_BuildME_interim.idf")
    idf=IDF(f"{savefolder_path}\\{building}_BuildME_interim.idf")

    name=input(colored(0, 255, 255, "Please enter str value for the common DHW naming used in your IDF file:"))

    # Lets find out all available keys in the IDF file
    allkeys = idfobjectkeys(idf)

    # Getting all possible HVAC-related keys by filtering...
    HVAC_related_list= allkeys[allkeys.index('HVACTEMPLATE:THERMOSTAT'):]
    HVAC_related_list = HVAC_related_list[:HVAC_related_list.index('MATRIX:TWODIMENSION')]

    findDHWlist=HVAC_related_list

    # Gathering all objects individually in our HVAC list and creating a homogenous list
    list=[]
    for items in findDHWlist:
        HVACobjects=idf.idfobjects[items.upper()]
        for obj in HVACobjects:
            list.append(obj)

    # Finding all DHW fields and their corresponding overarching objects
    objectswithDHW = []
    allparameterfields=[]
    for newobj in list:
        for fields in newobj.fieldnames:
            if newobj[fields]!="":
                if type(newobj[fields])==str:
                    if name in newobj[fields]:
                        allparameterfields.append(newobj[fields])
                        objectswithDHW.append(newobj)

    # Deleting all HVAC and DHW objects in our filtered list
    for HVAC_obj in HVAC_related_list:
        idf.removeallidfobjects(HVAC_obj)
    # Recreating DHW elements
    objectswithDHW_reduced=reduce(lambda l, x: l.append(x) or l if x not in l else l, objectswithDHW, [])
    for newobjects in objectswithDHW_reduced:
        idf.copyidfobject(newobjects)

    idf.saveas(f"{savefolder_path}\\{building}_BuildME_cleaned.idf")
    editedidf=idf

    return editedidf


def create_IdealLoads_objects(originalidf_path,savefolder_path):
    """
    Function to get inputs from the interim file and using them to create new IdealLoads objects

    :param originalidf_path: Path for the original IDF with a complex HVAC data
    :param savefolder_path: Path to use where all converted files will be saved
    :return:
    """

    # Backup
    originalidf = IDF(originalidf_path)
    building=originalidf.idfobjects["Building".upper()][0].Name
    interimidf = IDF(f"{savefolder_path}\\{building}_BuildME_interim.idf")
    editedidf= IDF(f"{savefolder_path}\\{building}_BuildME_cleaned.idf")

    zone_names = editedidf.idfobjects["Zone".upper()]

    for zone in zone_names:
        # Generic Parameter Definition
        newzone = editedidf.newidfobject("HVACTemplate:Zone:IdealLoadsAirSystem")
        newthermos = editedidf.newidfobject("HVACTemplate:Thermostat")

        newzone.Zone_Name = zone.Name
        newthermos.Name = "dual_thermostat_" + zone.Name
        newzone.Template_Thermostat_Name = newthermos.Name
        newzone.System_Availability_Schedule_Name = "ALWAYS_ON"
        newzone.Heating_Availability_Schedule_Name = "ALWAYS_ON"
        newzone.Cooling_Availability_Schedule_Name = "ALWAYS_ON"
        newzone.Maximum_Heating_Air_Flow_Rate = "autosize"
        newzone.Maximum_Sensible_Heating_Capacity = "autosize"
        newzone.Maximum_Total_Cooling_Capacity = "autosize"
        newzone.Maximum_Cooling_Air_Flow_Rate = "autosize"
        newzone.Humidification_Setpoint = "65"
        newzone.Dehumidification_Setpoint = ""
        newzone.Heating_Limit = "LimitFlowRateAndCapacity"
        newzone.Cooling_Limit = "LimitFlowRateAndCapacity"

        # Customization Part: Getting the approximate values from the complex HVAC version of the IDF
        for items in interimidf.idfobjects["DesignSpecification:OutdoorAir".upper()]:
            if newzone.Zone_Name in items.Name:
                newzone.Outdoor_Air_Flow_Rate_per_Zone_Floor_Area = items.Outdoor_Air_Flow_per_Zone_Floor_Area
                newzone.Outdoor_Air_Method = items.Outdoor_Air_Method
        for items in interimidf.idfobjects["Sizing:Zone".upper()]:
            if newzone.Zone_Name == items.Zone_or_ZoneList_Name:
                newzone.Minimum_Cooling_Supply_Air_Humidity_Ratio = items.Zone_Cooling_Design_Supply_Air_Humidity_Ratio
                newzone.Maximum_Heating_Supply_Air_Humidity_Ratio = items.Zone_Heating_Design_Supply_Air_Humidity_Ratio
                newzone.Minimum_Cooling_Supply_Air_Temperature = items.Zone_Cooling_Design_Supply_Air_Temperature
                newzone.Maximum_Heating_Supply_Air_Temperature = items.Zone_Heating_Design_Supply_Air_Temperature

        for items in interimidf.idfobjects["Controller:OutdoorAir".upper()]:
            newzone.Outdoor_Air_Economizer_Type = items.Economizer_Control_Type

        for items in interimidf.idfobjects["AirLoopHVAC:UnitarySystem".upper()]:
            newzone.Dehumidification_Control_Type = items.Dehumidification_Control_Type

        # Warning: The following code creates missing fields if the schedule names do not correspond the zone name
        for items in interimidf.idfobjects["ThermostatSetpoint:DualSetpoint".upper()]:
            if newzone.Zone_Name in items.Name:
                newthermos.Heating_Setpoint_Schedule_Name = items.Heating_Setpoint_Temperature_Schedule_Name
                newthermos.Cooling_Setpoint_Schedule_Name = items.Cooling_Setpoint_Temperature_Schedule_Name

        building = str(editedidf.idfobjects["Building".upper()][0].Name)
        editedidf.saveas(f"IdealLoads_{building}_converted.idf")

    os.remove(f"{savefolder_path}\\{building}_BuildME_interim.idf")
    os.remove(f"{savefolder_path}\\{building}_BuildME_cleaned.idf")
    return print("The conversion process is completed, the new IDF with Ideal Loads is saved")

if __name__ == "__main__":

    EXAMPLE CODE
    originalidf_path = "...\\BuildME-master\\tools\\SchoolPrimary.idf"
    savefolder_path ="...\\BuildME-master\\tools"

    delete_cmplx_HVAC_keep_DHW(originalidf_path,savefolder_path)
    create_IdealLoads_objects(originalidf_path, savefolder_path)

