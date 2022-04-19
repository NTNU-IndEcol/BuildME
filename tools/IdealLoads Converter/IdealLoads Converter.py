"""
Functions to convert IDFs with complex HVAC systems to create IDF versions with Ideal Loads Systems.

Use these functions:
to delete complex HVAC objects in IDF files,
to create new Ideal Loads objects,
to fill out missing fields in new Ideal Loads objects with the values from the original complex HVAC IDFs

Copyright: Sahin AKIN, 2022
"""

import os
from eppy.bunch_subclass import BadEPFieldError
from eppy.modeleditor import IDF

# Make sure that you have selected the correct working directory (BUILDME)
# Standalone Run Requirements
ep_version = '9.2.0'
path_parent = os.path.dirname(os.getcwd())
os.chdir(path_parent)
basepath = os.path.abspath('..')
ep_path = os.path.abspath("..\\bin\\EnergyPlus-9-2-0")
ep_idd = os.path.abspath("..\\bin\\EnergyPlus-9-2-0\\Energy+.idd")
IDF.setiddname(ep_idd)


def delete_cmplx_HVAC(originalidf_path):
    """
    Deletes Unnecessary fields that are not shared with DHW systems
    :param originalidf_path: Path for the original IDF with a complex HVAC data
    :return: editedidf
    """
    originalidf = IDF(originalidf_path)

    # The following objects can be deleted automatically.
    delete_objects_list = [
        "DESIGNSPECIFICATION:OUTDOORAIR",
        "DESIGNSPECIFICATION:ZONEAIRDISTRIBUTION",
        "SIZING:ZONE",
        "SIZING:SYSTEM",
        "ZONECONTROL:THERMOSTAT",
        "THERMOSTATSETPOINT:DUALSETPOINT",
        "ZONEHVAC:UNIHEATER",
        "ZONEHVAC:FOURPIPEFANCOIL",
        "AIRTERMINAL:SINGLEDUCT:UNCONTROLLED",
        "AIRTERMINAL:SINGLEDUCT:VAV:REHEAT",
        "ZONEHVAC:AIRDISTRIBUTIONUNIT",
        "ZONEHVAC:EQUIPMENTLIST",
        "ZONEHVAC:EQUIPMENTCONNECTIONS",
        "FAN:VARIABLEVOLUME",
        "FAN:CONSTANTVOLUME",
        "FAN:SYSTEMMODEL",
        "FAN:ONOFF",
        "FAN:ZONEEXHAUST",
        "COIL:COOLING:DX:TWOSPEED",
        "COIL:COOLING:DX:MULTISPEED",
        "COIL:COOLING:WATER",
        "COIL:HEATING:WATER",
        "COIL:HEATING:FUEL",
        "COIL:HEATING:ELECTRIC",
        "COILSYSTEM:COOLING:DX",
        "HEATEXCHANGER:AIRTOAIR:SENSIBLEANDLATENT",
        "AIRLOOPHVAC:UNITARYSYSTEM",
        "UNITARYSYSTEMPERFORMANCE:MULTISPEED",
        "CONTROLLER:WATERCOIL",
        "CONTROLLER:OUTDOORAIR",
        "CONTROLLER:MECHANICALVENTILATION",
        "AIRLOOPHVAC:CONTROLLERLIST",
        "AIRLOOPHVAC",
        "AIRLOOPHVAC:OUTDOORAIRSYSTEM:EQUIPMENTLIST",
        "AIRLOOPHVAC:OUTDOORAIRSYSTEM",
        "OUTDOORAIR:MIXER",
        "AIRLOOPHVAC:ZONESPLITTER",
        "AIRLOOPHVAC:SUPPLYPATH",
        "AIRLOOPHVAC:ZONEMIXER",
        "AIRLOOPHVAC:RETURNPLENUM",
        "AIRLOOPHVAC:RETURNPATH",
        "NODELIST",
        "OUTDOORAIR:NODE",
        "OUTDOORAIR:NODELIST",
        "PUMP:VARIABLESPEED",
        "BOILER:HOTWATER",
        "CHILLER:ELECTRIC:EIR",
        "AVAILABILITYMANAGER:NIGHTCYCLE",
        "AVAILABILITYMANAGERASSIGNMENTLIST",
        "SETPOINTMANAGER:OUTDOORAIRRESET",
        "SETPOINTMANAGER:SINGLEZONE:HEATING",
        "SETPOINTMANAGER:SINGLEZONE:COOLING",
        "SETPOINTMANAGER:MIXEDAIR",
        "SETPOINTMANAGER:OUTDOORAIRPRETREAT",
        "REFRIGERATION:CASE",
        "REFRIGERATION:COMPORESSORRACK",
        "REFRIGERATION:CASEANDWALKINLIST",
        "CURVE:QUADRATIC",
        "CURVE:BIQUADRATIC"
    ]
    for x in originalidf.idfobjects:
        for y in delete_objects_list:
            if str(x) == y:
                originalidf.removeallidfobjects(x)
    editedidf = originalidf
    return editedidf


def create_IdealLoads_objects(editedidf, originalidf_path):
    """
    :param editedidf: edited IDF file
    :param originalidf_path: path for the original IDF file contains complex HVAC data
    :return: an IDF with IdealLoads systems
    """
    originalidf = IDF(originalidf_path)

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
        for items in originalidf.idfobjects["DesignSpecification:OutdoorAir".upper()]:
            if newzone.Zone_Name in items.Name:
                newzone.Outdoor_Air_Flow_Rate_per_Zone_Floor_Area = items.Outdoor_Air_Flow_per_Zone_Floor_Area
                newzone.Outdoor_Air_Method = items.Outdoor_Air_Method
        for items in originalidf.idfobjects["Sizing:Zone".upper()]:
            if newzone.Zone_Name == items.Zone_or_ZoneList_Name:
                newzone.Minimum_Cooling_Supply_Air_Humidity_Ratio = items.Zone_Cooling_Design_Supply_Air_Humidity_Ratio
                newzone.Maximum_Heating_Supply_Air_Humidity_Ratio = items.Zone_Heating_Design_Supply_Air_Humidity_Ratio
                newzone.Minimum_Cooling_Supply_Air_Temperature = items.Zone_Cooling_Design_Supply_Air_Temperature
                newzone.Maximum_Heating_Supply_Air_Temperature = items.Zone_Heating_Design_Supply_Air_Temperature

        for items in originalidf.idfobjects["Controller:OutdoorAir".upper()]:
            newzone.Outdoor_Air_Economizer_Type = items.Economizer_Control_Type

        for items in originalidf.idfobjects["AirLoopHVAC:UnitarySystem".upper()]:
            newzone.Dehumidification_Control_Type = items.Dehumidification_Control_Type

        # Warning: The following code creates missing fields if the schedule names do not correspond the zone name
        for items in originalidf.idfobjects["ThermostatSetpoint:DualSetpoint".upper()]:
            if newzone.Zone_Name in items.Name:
                newthermos.Heating_Setpoint_Schedule_Name = items.Heating_Setpoint_Temperature_Schedule_Name
                newthermos.Cooling_Setpoint_Schedule_Name = items.Cooling_Setpoint_Temperature_Schedule_Name

        building = str(originalidf.idfobjects["Building".upper()][0].Name)
        editedidf.saveas(f"IdealLoads_{building}.idf")

    return print("The process is completed, the new IDF is saved")


def idfobjectkeys(idf):
    """returns the object keys in the order they were in the IDD file
    it is an ordered list of idf.idfobjects.keys()
    keys of a dict are unordered, so idf.idfobjects.keys() will not work for this purpose"""
    return idf.model.dtls


def delete_cmplx_HVAC_keep_DHW(idf, **kwargs):
    """return the object, if the Name or some other field is known.
    send field in ``**kwargs`` as Name='a name', Roughness='smooth'
    Returns the first find (field search is unordered)
    objkeys -> if objkeys=['ZONE', 'Material'], search only those"""

    # Lets find out all available keys in the IDF file
    allkeys = idfobjectkeys(idf)
    # Getting all possible HVAC-related keys by via filtering...
    relavent_items = ["VER","DESIGNSPECIFICATION"]


    for keys in allkeys:
        for item in relavent_items:
            mystr= f"{item}"
            if mystr in keys:
                allkeys.remove(f"{keys}")

    filteredkeys = allkeys
    print(filteredkeys)


    objectswithDHW = []
    for objkey in filteredkeys:
        idfobjs = idf.idfobjects[objkey.upper()]
        for idfobj in idfobjs:
            for key, val in kwargs.items():
                try:
                    if val in idfobj[key]:
                        objectswithDHW.append(idfobj)
                except BadEPFieldError as e:
                    continue
    # now,lets delete everything and recreate all DHW objects!
    return filteredkeys

if __name__ == "__main__":
    originalidf_path = "C:\\Users\\sahina\\PycharmProjects\\Kamila\\tools\\SchoolPrimary.idf"
    idf1 = delete_cmplx_HVAC(originalidf_path)
    # print(name2idfobject((delete_cmplx_HVAC(originalidf_path)),objkeys=["OUTPUT:"],field="Hourly"))
    # print(idf1.getiddgroupdict())
    print(delete_cmplx_HVAC_keep_DHW(idf1))
