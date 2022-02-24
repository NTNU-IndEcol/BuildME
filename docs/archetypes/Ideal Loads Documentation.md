**Documentation on Ideal Loads Implementation**

**1.  Introduction and Motivation**

This document summarizes the implementation of the Ideal Loads HVAC system
(ILHS) on the IDF files, which are modeled using advanced HVAC systems (i.e.,
heat pumps, fans, coils). ILHS is a theoretical HVAC system that fulfills the
amount of system energy to meet zones' cooling and heating loads ideally[^1].
ILHS can be modeled with as few as three simulation parameters, significantly
reducing simulation time. Apart from that, ILHS is a prerequisite for the
mixed-mode ventilation calculations in BuildME.

[^1]: U.S. Department of Energy, “Engineering Reference EnergyPlus 8.0,” 2022,
    https://bigladdersoftware.com/epx/docs/8-0/engineering-reference/.

The workflow presented here should be visited if one wants to run IDF files
modeled with HVAC systems other than ILHS in the mixed-mode option on BuildME.
Otherwise, the IDF files can be used by setting the cooling option in the
debugging combination located at *settings.py* to"HVAC”.

The conversion of the advanced HVAC systems to ILHS is based on deleting all the
HVAC-related parameter objects and creating new ones corresponding to ILHS. ILHS
implementation is not very suitable to be conducted by using a fully-automated
workflow because HVAC systems can be modeled in various ways and may not follow
a consistent pattern to be controlled by a code. In addition, generally advanced
HVAC system parameters are shared with some other domestic-hot water (DHW)
systems, increasing the complexity of the detangling process. For these reasons,
the ILHS conversion process is designed in a semi-automated way, reducing manual
intervention.

The code contains two functions where *delete_cmplx_HVAC* deletes the unique
simulation parameters containing only the HVAC objects, and
*create_IdealLoads_objects* creates new simulation parameters for ILHS by using
the old values in the advanced HVAC objects from the original IDF file. In the
upcoming sections, these functions will be introduced thoroughly.

**2.  Workflow**

The conversion workflow comprises two stages, namely the deletion and creation
stage.

*2.1.  Deletion stage*

The deletion stage consists of two parts, where the first part is automatically
conducted, while the second one requires manual manipulation.

-   *Deleting advanced HVAC simulation parameters via code*
    (*delete_cmplx_HVAC):*

The function deletes the unnecessary parameters that only include advanced HVAC
objects specifically. The parameters in Table 1 do not contain any DHW objects
and can be deleted automatically for all IDF files. The parameter list reported
here does not cover all advanced HVAC objects, therefore based on the user’s
original IDF elements, this list can be expanded.
|Simulation Parameters                        |                                               |
|---------------------------------------------|-----------------------------------------------|
| "DESIGNSPECIFICATION:OUTDOORAIR",           | "UNITARYSYSTEMPERFORMANCE:MULTISPEED",        |
| "DESIGNSPECIFICATION:ZONEAIRDISTRIBUTION",  | "CONTROLLER:WATERCOIL",                       |
| "SIZING:ZONE",                              | "CONTROLLER:OUTDOORAIR",                      |
| "SIZING:SYSTEM",                            | "CONTROLLER:MECHANICALVENTILATION",           |
| "ZONECONTROL:THERMOSTAT",                   | "AIRLOOPHVAC:CONTROLLERLIST",                 |
| "THERMOSTATSETPOINT:DUALSETPOINT",          | "AIRLOOPHVAC",                                |
| "ZONEHVAC:UNIHEATER",                       | "AIRLOOPHVAC:OUTDOORAIRSYSTEM:EQUIPMENTLIST", |
| "ZONEHVAC:FOURPIPEFANCOIL",                 | "AIRLOOPHVAC:OUTDOORAIRSYSTEM",               |
| "AIRTERMINAL:SINGLEDUCT:UNCONTROLLED",      | "OUTDOORAIR:MIXER",                           |
| "AIRTERMINAL:SINGLEDUCT:VAV:REHEAT",        | "AIRLOOPHVAC:ZONESPLITTER",                   |
| "ZONEHVAC:AIRDISTRIBUTIONUNIT",             | "AIRLOOPHVAC:SUPPLYPATH",                     |
| "ZONEHVAC:EQUIPMENTLIST",                   | "AIRLOOPHVAC:ZONEMIXER",                      |
| "ZONEHVAC:EQUIPMENTCONNECTIONS",            | "AIRLOOPHVAC:RETURNPLENUM",                   |
| "FAN:VARIABLEVOLUME",                       | "AIRLOOPHVAC:RETURNPATH",                     |
| "FAN:CONSTANTVOLUME",                       | "NODELIST",                                   |
| "FAN:SYSTEMMODEL",                          | "OUTDOORAIR:NODE",                            |
| "FAN:ONOFF",                                | "OUTDOORAIR:NODELIST",                        |
| "FAN:ZONEEXHAUST",                          | "PUMP:VARIABLESPEED",                         |
| "COIL:COOLING:DX:TWOSPEED",                 | "BOILER:HOTWATER",                            |
| "COIL:COOLING:DX:MULTISPEED",               | "CHILLER:ELECTRIC:EIR",                       |
| "COIL:COOLING:WATER",                       | "AVAILABILITYMANAGER:NIGHTCYCLE",             |
| "COIL:HEATING:WATER",                       | "AVAILABILITYMANAGERASSIGNMENTLIST",          |
| "COIL:HEATING:FUEL",                        | "SETPOINTMANAGER:OUTDOORAIRRESET",            |
| "COIL:HEATING:ELECTRIC",                    | "SETPOINTMANAGER:SINGLEZONE:HEATING",         |
| "COILSYSTEM:COOLING:DX",                    | "SETPOINTMANAGER:SINGLEZONE:COOLING",         |
| "HEATEXCHANGER:AIRTOAIR:SENSIBLEANDLATENT", | "SETPOINTMANAGER:MIXEDAIR",                   |
| "AIRLOOPHVAC:UNITARYSYSTEM",                | "SETPOINTMANAGER:OUTDOORAIRPRETREAT",         |
| "REFRIGERATION:CASEANDWALKINLIST",          | "REFRIGERATION:CASE",                         |
| "CURVE:QUADRATIC",                          | "REFRIGERATION:COMPORESSORRACK",              |
| "CURVE:BIQUADRATIC"                         |                                               |

Table 1. Advanced HVAC parameters

-   *Deleting advanced HVAC simulation parameters manually:*

Manual editing is only required if IDF files also contain a DHW system along
with the advanced HVAC objects. The following parameters are commonly used
between DHW and HVAC (Table 2). As the naming of the object names depends on
user choices, automation in this part does not guarantee a functional IDF after
the run. Therefore, manual manipulation to winnow out HVAC objects is
recommended for the common parameters shared with DHW systems. As stated
previously, this list can be expanded based on the advanced HVAC type in the
original IDF file.
|Simulation Parameters                             |                                     |
|--------------------------------------------------|-------------------------------------|
| "SCHEDULE:CONSTANT ",                            | "ENERGYMANAGEMENTSYSTEM:SENSOR ",   |
| "SETPOINTMANAGER:SCHEDULED ",                    | "ENERGYMANAGEMENTSYSTEM:ACTUATOR ", |
| "ENERGYMANAGEMENTSYSTEM:PROGRAMCALLINGMANAGER ", | "PUMP:CONSTANTSPEED ",              |
| "ENERGYMANAGEMENTSYSTEM:PROGRAM ",               | "PIPE:ADIABATIC ",                  |
| "ENERGYMANAGEMENTSYSTEM:SENSOR ",                | "SIZING:PLANT ",                    |
| "PLANTEQUIPMENTLIST ",                           | "BRANCH ",                          |
| "PLANTEQUIPMENTOPERATION:HEATINGLOAD ",          | "BRANCHLIST ",                      |
| "PLANTEQUIPMENTOPERATION:COOLINGLOAD ",          | "CONNECTOR:SPLITTER",               |
| "PLANTEQUIPMENTOPERATIONSCHEMES ",               | "CONNECTOR:MIXER",                  |
| "CONNECTOR:LIST ",                               |                                     |

Table 2. Advanced HVAC parameters shared with DHW systems

*2.2  Creation stage*

For ILHS conversion, one needs to define or have at least three objects in
total, these are:

-   *HVACTemplate:Thermostat,*

-   *HVACTemplate:ZoneIdealLoadsAirSystem,*

-   *Sizing:Parameters*

“*Sizing:Parameter*s” parameter should have been already defined in the original
IDF file so that the same parameter can be used without any intervention. For
the remaining two parameters, a fully automated workflow is followed.

-   *“create_IdealLoads_objects”:* The function uses the original IDF file as
    the data source to fill the missing fields in the newly created ILHS objects
    (Figure 1). The function contains two subsections as generic and customized
    parameter definitions. Generic parameter definition is applied to all IDF
    files independent from the building type and previous HVAC settings. On the
    other hand, customized parameter definition obtains specifically calculated
    zone inputs from the original IDF file and write them to the new ILHS
    objects. This function creates two new parameters:
    *“HVACTemplate:Thermostat”* and “*HVACTemplate:ZoneIdealLoadsAirSystem”.* It
    is essential to state that when filling the *“HVACTemplate:Thermostat”*
    object, the user needs to check the "ThermostatSetpoint:DualSetpoint"
    parameter’s objects in the original IDF to see whether the schedule names
    includes the zone names. If the naming for the schedules does not contain
    zone names, then the function returns missing values for those particular
    schedules in the new IDF file.

![image](https://user-images.githubusercontent.com/33637609/155561450-d85c7d8d-775a-4992-8c6a-64d1e641d97a.png)
                            
Figure 1. Creating a new object and filling its missing fields automatically
with the values from the original IDF file

**3.  Final Remarks**

The functions introduced in this document are optional to use. A user can
perform the conversion process either by following a completely manual workflow
or operationalizing one or both functions as needed.
