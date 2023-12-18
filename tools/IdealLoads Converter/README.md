# **Documentation on Ideal Loads Implementation**

## **1.  Introduction and Motivation**

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
HVAC-related parameter objects and creating new ones corresponding to ILHS.
HVAC systems can be modeled in various ways and these systems are generally shared with some other domestic-hot water (DHW)
systems, which makes deleting only HVAC objects cumbersome. For these reasons, the detangling of the HVAC and DHW systems is required. 
IdealLoads Converter is designed in an automated way, reducing manual
intervention as much as possible. The only prerequisite is thath DHW elements should have an identifier, or common string throughout. This could be "DHW" or "SHW" or any other string portion that is used repeatedly in all DHW objects.

Ideal Loads Converter has several functions where *delete_cmplx_HVAC* deletes the unique
simulation parameters containing only the HVAC objects, *delete_cmplx_HVAC_keep_DHW* deletes the HVAC objects without intervening the DHW systems
and lastly, *create_IdealLoads_objects* creates new simulation parameters for ILHS by using
the old values in the advanced HVAC objects from the original IDF file. In the
upcoming sections, these functions will be introduced thoroughly.

## **2.  Workflow**

The conversion workflow comprises two stages, namely the deletion and creation
stage.

### *2.1.  Deletion stage*

The deletion stage consists of two functions, where the first function is only applicable to the IDFs without DHW systems and the latter can be used if there is also an existing DHW system available in IDF.

#### *2.1.1 Deleting advanced HVAC simulation parameters*
 ```delete_cmplx_HVAC(originalidf_path,savefolder_path)```:

The function deletes the unnecessary parameters that include advanced HVAC
objects. The function should only be used if the IDF about to be converted does not contain any DHW objects. 
All parameters between **'HVACTEMPLATE:THERMOSTAT** and **'MATRIX:TWODIMENSION'** will be deleted and a new IDF file will be saved to the save folder.
There is also a backup routine implemented to avoid losses in the original IDF files. 


*Variables*:

**originalidf_path**: Path for the original IDF with a complex HVAC data

**savefolder_path**: Path to use where all converted files will be saved

#### *2.1.2 Deleting advanced HVAC simulation parameters exluding the DHW parameters*
 ```delete_cmplx_HVAC_keep_DHW(originalidf_path,savefolder_path)```:

This function is only required if IDF files also contain a DHW system along
with the advanced HVAC objects.  The code makes it possible to separate DHW and HVAC systems without manual intervention.
As the naming of the DHW object names depends on user choices, the only requirement is that DHW elements should have an identifier, or common string throughout.
This could be "DHW" or "SHW" or any other string portion that is used repeatedly in all DHW objects. Users will be prompted to specify the repeating string portion in DHW objects when the code is run. All parameters between **'HVACTEMPLATE:THERMOSTAT** and **'MATRIX:TWODIMENSION'** will be checked if they contain any DHW parameter, then the HVAC objects will be deleted and a new IDF file will be saved to the save folder. There is also a backup routine implemented to avoid losses in the original IDF files. 

*Variables*:

**originalidf_path**: Path for the original IDF with a complex HVAC data

**savefolder_path**: Path to use where all converted files will be saved




### *2.2.  Creation stage*

For ILHS conversion, one needs to define or have at least three objects in
total, these are:

-   *HVACTemplate:Thermostat,*

-   *HVACTemplate:ZoneIdealLoadsAirSystem,*

-   *Sizing:Parameters*

“*Sizing:Parameter*s” parameter should have been already defined in the original
IDF file so that the same parameter can be used without any intervention. For
the remaining two parameters, a fully automated workflow is followed.


#### *2.2.1 Creating new ILHS objects*
 ```create_IdealLoads_objects(originalidf_path,savefolder_path)```:
 
The function uses the original IDF file as
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
    
*Variables*:

**originalidf_path**: Path for the original IDF with a complex HVAC data

**savefolder_path**: Path to use where all converted files will be saved

![image](https://user-images.githubusercontent.com/33637609/155561450-d85c7d8d-775a-4992-8c6a-64d1e641d97a.png)
                            
Figure 1. Creating a new object and filling its missing fields automatically
with the values from the original IDF file

## **3.  Final Remarks**

The functions introduced in this document are optional to use. A user can
perform the conversion process either by following a completely manual workflow
or operationalizing one or both functions as needed.
