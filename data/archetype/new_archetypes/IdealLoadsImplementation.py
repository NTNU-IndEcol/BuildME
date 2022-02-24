#IDEAL LOADS IMPLEMENTATION (this code only includes the generic implementation of the Ideal Loads System to all IDF files,
# however there are some other things should be intervened manually
# (i.e. common simulation parameters between DHW and HVAC)

########Required for standalone run
from eppy import modeleditor
from eppy.modeleditor import IDF
import eppy
import os
import platform
ep_version = '9.2.0'
ep_path = "C:\\Users\\sahina\\PycharmProjects\\BuildME-master\\bin\\EnergyPlus-9-2-0"
ep_idd = "C:\\Users\\sahina\\PycharmProjects\\BuildME-master\\bin\\EnergyPlus-9-2-0\\Energy+.idd"
IDF.setiddname(ep_idd)
# Checking OS and modify files to copy
platform = platform.system()
if platform == 'Windows':
    ep_exec_files = ["energyplus.exe", "Energy+.idd", "EPMacro.exe", "ExpandObjects.exe",
                     "PreProcess/GrndTempCalc/Basement.exe", "PreProcess/GrndTempCalc/BasementGHT.idd",
                     "PreProcess/GrndTempCalc/Slab.exe", "PreProcess/GrndTempCalc/SlabGHT.idd",
                     "PostProcess/ReadVarsESO.exe", "energyplusapi.dll"
                     ]
elif platform == 'Darwin':
    ep_exec_files = ["energyplus", "energyplus-%s" % ep_version, "Energy+.idd", "EPMacro", "ExpandObjects",
                     "libenergyplusapi.%s.dylib" % ep_version,  # required by energyplus
                     "libgfortran.5.dylib", "libquadmath.0.dylib",  # required by ExpandObjects
                     "PreProcess/GrndTempCalc/Basement", "PreProcess/GrndTempCalc/BasementGHT.idd",
                     "PreProcess/GrndTempCalc/Slab", "PreProcess/GrndTempCalc/SlabGHT.idd",
                     "PostProcess/ReadVarsESO"
                     ]
else:
    raise NotImplementedError('OS is not supported!')
##########


#Location of the edited idf (manually deleted idf file)
editedidf_path = "C:\\Users\\sahina\\PycharmProjects\\BuildME-master\\data\\archetype\\new_archetypes\\New folder\\OfficeM.idf"
#Location of the original idf with complex HVAC
originalidf_path= "C:\\Users\\sahina\\PycharmProjects\\BuildME-master\\data\\archetype\\new_archetypes\\OfficeM.idf"

idf1=IDF(editedidf_path)
idforg=IDF(originalidf_path)




def delete_cmplx_HVAC (idforg):
    """
    Deletes Unnecessary fields that are not shared with DHW systems
    :param originalidf: contains complex HVAC data
    :return: editedidf:
    """
    #Warning: In order to prevent mistakes, it is better to delete these objects manually but for the following objects, all of them
    # can be deleted automatically.
    delete_objects_list=[
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
    for x in idforg.idfobjects:
        for y in delete_objects_list:
            if str(x)==y:
                idforg.removeallidfobjects(x)
    idf1=idforg
    return idf1

def create_IdealLoads_objects (idf1,originalidf_path):
    """

    :param idf1: edited idf file
    :param originalidf_path: path for the original idf file contains complex HVAC data
    :return: Ideal Loads implemented idf
    """
    idforg = IDF(originalidf_path)

    zone_names= idf1.idfobjects["Zone".upper()]

    for zone in zone_names:
        #Generic Parameter Definition
        newzone=idf1.newidfobject("HVACTemplate:Zone:IdealLoadsAirSystem")
        newthermos=idf1.newidfobject("HVACTemplate:Thermostat")

        newzone.Zone_Name=zone.Name
        newthermos.Name= "dual_thermostat_" + zone.Name
        newzone.Template_Thermostat_Name =newthermos.Name
        newzone.System_Availability_Schedule_Name = "ALWAYS_ON"
        newzone.Heating_Availability_Schedule_Name = "ALWAYS_ON"
        newzone.Cooling_Availability_Schedule_Name = "ALWAYS_ON"
        newzone.Maximum_Heating_Air_Flow_Rate="autosize"
        newzone.Maximum_Sensible_Heating_Capacity="autosize"
        newzone.Maximum_Total_Cooling_Capacity = "autosize"
        newzone.Maximum_Cooling_Air_Flow_Rate = "autosize"
        newzone.Humidification_Setpoint = "65"
        newzone.Dehumidification_Setpoint = ""
        newzone.Heating_Limit = "LimitFlowRateAndCapacity"
        newzone.Cooling_Limit = "LimitFlowRateAndCapacity"


        # Customization Part: Getting the approximate values from the complex HVAC version of the IDF
        for items in idforg.idfobjects["DesignSpecification:OutdoorAir".upper()]:
            if newzone.Zone_Name in items.Name:
                newzone.Outdoor_Air_Flow_Rate_per_Zone_Floor_Area = items.Outdoor_Air_Flow_per_Zone_Floor_Area
                newzone.Outdoor_Air_Method = items.Outdoor_Air_Method
        for items in idforg.idfobjects["Sizing:Zone".upper()]:
            if newzone.Zone_Name==items.Zone_or_ZoneList_Name:
                newzone.Minimum_Cooling_Supply_Air_Humidity_Ratio = items.Zone_Cooling_Design_Supply_Air_Humidity_Ratio
                newzone.Maximum_Heating_Supply_Air_Humidity_Ratio = items.Zone_Heating_Design_Supply_Air_Humidity_Ratio
                newzone.Minimum_Cooling_Supply_Air_Temperature = items.Zone_Cooling_Design_Supply_Air_Temperature
                newzone.Maximum_Heating_Supply_Air_Temperature = items.Zone_Heating_Design_Supply_Air_Temperature

        for items in idforg.idfobjects["Controller:OutdoorAir".upper()]:
            newzone.Outdoor_Air_Economizer_Type=items.Economizer_Control_Type

        for items in idforg.idfobjects["AirLoopHVAC:UnitarySystem".upper()]:
            newzone.Dehumidification_Control_Type=items.Dehumidification_Control_Type

        #Warning: The following code creates missing fields if the schedule names do not correspond the zone name
        for items in idforg.idfobjects["ThermostatSetpoint:DualSetpoint".upper()]:
            if newzone.Zone_Name in items.Name:
                newthermos.Heating_Setpoint_Schedule_Name=items.Heating_Setpoint_Temperature_Schedule_Name
                newthermos.Cooling_Setpoint_Schedule_Name = items.Cooling_Setpoint_Temperature_Schedule_Name

        building = str(idforg.idfobjects["Building".upper()][0].Name)
        idf1.saveas(f"IdealLoads_{building}.idf")

    return print("The process is completed, the new IDF is saved")



create_IdealLoads_objects(delete_cmplx_HVAC(idforg),originalidf_path)
