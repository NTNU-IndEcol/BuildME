"""
Functions to adapt custom IDF files to BuildME.

Use these functions:
to automatically insert replaceme strings on surface objects,
to rename materials/constructions based on standards/resource efficiency scenarios or any other layers(i.e., cohort),
to merge idfs that have different materials/constructions,
to update replace.csv,
to update material.csv,
to change Output objects' contents in a way that BuildME accepts

Copyright: Sahin AKIN, 2022
"""

import os
from functools import reduce
from io import StringIO
import glob
from eppy.modeleditor import IDF
import pandas as pd

# Make sure that you have selected the correct working directory (BUILDME)
# Standalone Run Requirements
ep_version = '9.2.0'
path_parent = os.path.dirname(os.getcwd())
os.chdir(path_parent)
basepath = os.path.abspath('..')
ep_path = os.path.abspath("..\\bin\\EnergyPlus-9-2-0")
ep_idd = os.path.abspath("..\\bin\\EnergyPlus-9-2-0\\Energy+.idd")
IDF.setiddname(ep_idd)


def create_combined_idflist(folderpath):
    """
    Creates a list containing the generated idf files
    :param folderpath: (in other words, save folder) containing all generated idfs for standards/res scenarios for a single archetype type (e.g. RT only)
    :return: a combined idf list
    """
    print("IDF list is being generated...")
    filepaths = [os.path.join(folderpath, name) for name in os.listdir(folderpath)]
    all_files = []
    for path in filepaths:
        if "-converted" in path:
            with open(path, 'r') as f:
                file = f.read()
                all_files.append(file)

    return all_files


def convert_idf_to_BuildME(idf_path, save_folder_path, replace_string="-en-std-replaceme",
                           replace_string_value="-non-standard", base=False):
    """
    This function creates an individual edited IDF file that is compatible with BuildME framework

    Requirements for a clear run:
    1)Window-Skylight Difference should be addressed in construction name (e.g. name contains "sky")

    Run Order:
    -Adds replaceme fields,
    -Renames Materials,
    -Renames Constructions,
    -Defines non-standard U values; if replace_string_value is set accordingly.

    :param idf_path: path for idf file to be converted, standard file should be used forthe non-standard IDF creation
    :param save_folder_path: New location folder path, where the new IDF will be saved
    :param replace_string: Replaceme content (i.e., -en-std-replaceme-res-replacemem-chrt-replaceme), should start with "-"
    :param replace_string_value: Replacer string corresponding to the replace string (i.e., -standard-RES0-1920), should start with "-"
    :param base: Boolean value to declare whether the IDF file corresponding to a base IDF
    :return: A compatible file with BuildME for an IDF with specific features
    """
    if os.path.exists(save_folder_path):
        print("IDF folder exists, emptying the folder")
        files = glob.glob(save_folder_path + "\*")
        for f in files:
            os.remove(f)
    idf1 = IDF(idf_path)
    print("Conversion is initialized, construction and surface objects are being converted...")
    # CONVERTING CONSTRUCTION NAMES AND INSERTING REPLACEME STRINGS:
    # It inserts a replaceme string to the building surface object's construction field, adds a new identical construction to the construction object
    # and renames the construction name corresponding to the replaceme string
    for items in idf1.idfobjects["BuildingSurface:Detailed".upper()]:
        for obj in idf1.idfobjects["Construction".upper()]:
            if obj.Name == items.Construction_Name:

                if items.Surface_Type == "Roof":
                    items.Construction_Name = f"ext-roof{replace_string}"
                    newcons = idf1.copyidfobject(obj)
                    newcons.Name = f"ext-roof{replace_string_value}"

                if items.Surface_Type == "Ceiling":
                    if "int" in items.Construction_Name or "ceiling" in items.Construction_Name or "Ceiling" in items.Name:
                        items.Construction_Name = f"int-ceiling{replace_string}"
                        newcons = idf1.copyidfobject(obj)
                        newcons.Name = f"int-ceiling{replace_string_value}"

                if items.Surface_Type == "Floor":
                    if items.Outside_Boundary_Condition == "Surface":
                        items.Construction_Name = f"int-floor{replace_string}"
                        newcons = idf1.copyidfobject(obj)
                        newcons.Name = f"int-floor{replace_string_value}"
                    if items.Outside_Boundary_Condition == "Adiabatic" or items.Outside_Boundary_Condition == "Ground" or items.Outside_Boundary_Condition == "Outdoors" or items.Outside_Boundary_Condition == "GroundSlabPreprocessorAverage":
                        items.Construction_Name = f"ext-floor{replace_string}"
                        newcons = idf1.copyidfobject(obj)
                        newcons.Name = f"ext-floor{replace_string_value}"

                if items.Surface_Type == "Wall":
                    if "int" in items.Construction_Name or "partition" in items.Construction_Name or items.Outside_Boundary_Condition == "Surface":
                        items.Construction_Name = f"int-wall{replace_string}"
                        newcons = idf1.copyidfobject(obj)
                        newcons.Name = f"int-wall{replace_string_value}"
                    else:
                        items.Construction_Name = f"ext-wall{replace_string}"
                        newcons = idf1.copyidfobject(obj)
                        newcons.Name = f"ext-wall{replace_string_value}"

        if 'CONSTRUCTION:FFACTORGROUNDFLOOR' in [x for x in idf1.idfobjects]:
            for floor in idf1.idfobjects["Construction:FfactorGroundFloor".upper()]:
                if floor.Name == items.Construction_Name:
                    if items.Surface_Type == "Floor":
                        if items.Outside_Boundary_Condition == "GroundFCfactorMethod":
                            items.Construction_Name = f"{items.Construction_Name}{replace_string}"
                            newcons = idf1.copyidfobject(floor)
                            newcons.Name = f"{floor.Name}{replace_string_value}"

        if 'CONSTRUCTION:CFACTORUNDERGROUNDWALL' in [x for x in idf1.idfobjects]:
            for wall in idf1.idfobjects["Construction:CfactorUndergroundWall".upper()]:
                if wall.Name == items.Construction_Name:
                    if items.Surface_Type == "Wall":
                        if items.Outside_Boundary_Condition == "GroundFCfactorMethod" or items.Outside_Boundary_Condition == "Adiabatic":
                            items.Construction_Name = f"{items.Construction_Name}{replace_string}"
                            newcons = idf1.copyidfobject(wall)
                            newcons.Name = f"{wall.Name}{replace_string_value}"

    if 'WINDOW' in [x for x in idf1.idfobjects]:
        for fenest in idf1.idfobjects["Window".upper()]:
            fenest.Construction_Name = f"ext-window{replace_string}"

    if 'DOOR' in [x for x in idf1.idfobjects]:
        for fenest in idf1.idfobjects["Door".upper()]:
            fenest.Construction_Name = f"ext-door{replace_string}"

    if 'WINDOWSHADINGCONTROL' in [x for x in idf1.idfobjects]:
        for shade in idf1.idfobjects["WindowShadingControl".upper()]:
            for obj in idf1.idfobjects["Construction".upper()]:
                if shade.Construction_with_Shading_Name == obj.Name:
                    shade.Construction_with_Shading_Name = f"ext-window-wshade{replace_string}"
                    newcons = idf1.copyidfobject(obj)
                    newcons.Name = f"ext-window-wshade{replace_string_value}"
    print("Checking each window,frame...This will take some time!")
    if 'FENESTRATIONSURFACE:DETAILED' in [x for x in idf1.idfobjects]:
        for fenest in idf1.idfobjects["FenestrationSurface:Detailed".upper()]:
            for obj in idf1.idfobjects["Construction".upper()]:
                for frame in idf1.idfobjects["WindowProperty:FrameAndDivider".upper()]:
                    if fenest.Construction_Name == obj.Name:
                        if fenest.Surface_Type == "Window":

                            # there might be skylights:
                            if fenest.Frame_and_Divider_Name == frame.Name:
                                fenest.Frame_and_Divider_Name = f"ext-frame{replace_string}"
                                newcons = idf1.copyidfobject(frame)
                                newcons.Name = f"ext-frame{replace_string_value}"
                                fenest.Construction_Name = f"ext-window{replace_string}"
                                newcons = idf1.copyidfobject(obj)
                                newcons.Name = f"ext-window{replace_string_value}"

                            if "sky" in fenest.Construction_Name:
                                fenest.Construction_Name = f"ext-skywindow{replace_string}"
                                newcons = idf1.copyidfobject(obj)
                                newcons.Name = f"ext-skywindow{replace_string_value}"
                            else:
                                fenest.Construction_Name = f"ext-window{replace_string}"
                                newcons = idf1.copyidfobject(obj)
                                newcons.Name = f"ext-window{replace_string_value}"

                        if fenest.Surface_Type == "GlassDoor":
                            fenest.Construction_Name = f"ext-window{replace_string}"
                            newcons = idf1.copyidfobject(obj)
                            newcons.Name = f"ext-window{replace_string_value}"
                        if fenest.Surface_Type == "Door":
                            fenest.Construction_Name = f"ext-door{replace_string}"
                            newcons = idf1.copyidfobject(obj)
                            newcons.Name = f"ext-door{replace_string_value}"
    print("Still...")
    if 'FENESTRATIONSURFACE:DETAILED' in [x for x in idf1.idfobjects]:
        for fenest in idf1.idfobjects["FenestrationSurface:Detailed".upper()]:
            for obj in idf1.idfobjects["Construction".upper()]:
                for frame in idf1.idfobjects["WindowProperty:FrameAndDivider".upper()]:
                    if fenest.Construction_Name == obj.Name:
                        if fenest.Surface_Type == "Window":

                            # there might be skylights:
                            if fenest.Frame_and_Divider_Name != " ":
                                fenest.Frame_and_Divider_Name = f"ext-frame{replace_string}"
                                newcons = idf1.copyidfobject(frame)
                                newcons.Name = f"ext-frame{replace_string_value}"
                                fenest.Construction_Name = f"ext-window{replace_string}"
                                newcons = idf1.copyidfobject(obj)
                                newcons.Name = f"ext-window{replace_string_value}"

    # Deleting duplicated construction names
    unique = reduce(lambda l, x: l.append(x) or l if x not in l else l, idf1.idfobjects["Construction".upper()], [])
    idf1.removeallidfobjects("CONSTRUCTION")
    for newcons in unique:
        idf1.copyidfobject(newcons)
    if 'CONSTRUCTION:FFACTORGROUNDFLOOR' in [x for x in idf1.idfobjects]:
        unique = reduce(lambda l, x: l.append(x) or l if x not in l else l,
                        idf1.idfobjects["Construction:FfactorGroundFloor".upper()], [])
        idf1.removeallidfobjects("CONSTRUCTION:FFACTORGROUNDFLOOR")
    for newcons in unique:
        idf1.copyidfobject(newcons)
    if 'CONSTRUCTION:CFACTORUNDERGROUNDWALL' in [x for x in idf1.idfobjects]:
        unique = reduce(lambda l, x: l.append(x) or l if x not in l else l,
                        idf1.idfobjects["Construction:CfactorUndergroundWall".upper()], [])
        idf1.removeallidfobjects("CONSTRUCTION:CFACTORUNDERGROUNDWALL")
    for newcons in unique:
        idf1.copyidfobject(newcons)

    if 'WindowProperty:FrameAndDivider'.upper() in [x for x in idf1.idfobjects]:
        unique = reduce(lambda l, x: l.append(x) or l if x not in l else l,
                        idf1.idfobjects["WindowProperty:FrameAndDivider".upper()], [])
        idf1.removeallidfobjects("WindowProperty:FrameAndDivider".upper())
    for newcons in unique:
        idf1.copyidfobject(newcons)

    print("Material objects are being converted...")
    # CONVERTING MATERIALS
    # For the -non-standard version, values are replaced with %30 worse performing numbers based on the standard/base version.
    if "-non-standard" in replace_string_value:
        for items in idf1.idfobjects["Material".upper()]:
            items.Conductivity = float(items.Conductivity) * 1.3
            items.Name = f"{items.Name}{replace_string_value}"
        for items in idf1.idfobjects["Material:NoMass".upper()]:
            items.Thermal_Resistance = float(items.Thermal_Resistance) * 0.7
            items.Name = f"{items.Name}{replace_string_value}"
        for items in idf1.idfobjects["WindowMaterial:SimpleGlazingSystem".upper()]:
            items.UFactor = float(items.UFactor) * 1.3
            items.Name = f"{items.Name}{replace_string_value}"
        for items in idf1.idfobjects["WindowMaterial:Glazing".upper()]:
            items.Conductivity = float(items.Conductivity) * 1.3
            items.Name = f"{items.Name}{replace_string_value}"
        if 'CONSTRUCTION:FFACTORGROUNDFLOOR' in [x for x in idf1.idfobjects]:
            for items in idf1.idfobjects["Construction:FfactorGroundFloor".upper()]:
                items.FFactor = float(items.FFactor) * 0.7
        if 'CONSTRUCTION:CFACTORUNDERGROUNDWALL' in [x for x in idf1.idfobjects]:
            for items in idf1.idfobjects["Construction:CfactorUndergroundWall".upper()]:
                items.CFactor = float(items.CFactor) * 1.3

    # Material names are changed as they represent different values across standards, some identifiers are added based on replacer_string.
    else:
        for items in idf1.idfobjects["Material".upper()]:
            items.Name = f"{items.Name}{replace_string_value}"
        for items in idf1.idfobjects["Material:NoMass".upper()]:
            items.Name = f"{items.Name}{replace_string_value}"
        for items in idf1.idfobjects["WindowMaterial:SimpleGlazingSystem".upper()]:
            items.Name = f"{items.Name}{replace_string_value}"
        for items in idf1.idfobjects["WindowMaterial:Shade".upper()]:
            items.Name = f"{items.Name}{replace_string_value}"
        for items in idf1.idfobjects["WindowMaterial:Glazing".upper()]:
            items.Name = f"{items.Name}{replace_string_value}"

    # Construction material layer names are matched with above material changes
    for items in idf1.idfobjects["Construction".upper()]:
        for fields in items.fieldnames:
            if fields == "key":
                continue
            if fields == "Name":
                continue
            else:
                if items[fields] == "" or items[fields] == "IRTSurface" or items[fields] == "IRTMaterial":
                    continue
                else:
                    items[fields] = items[fields] + f"{replace_string_value}"

    # SAVING THE IDF FILE
    building = str(idf1.idfobjects["Building".upper()][0].Name)
    if base == True:
        idf1.idfobjects["Building".upper()][0].Name = f"BASE{building}{replace_string_value}"
        idf1.saveas(f"{save_folder_path}/BASE{building}{replace_string_value}-converted.idf")
    else:
        idf1.idfobjects["Building".upper()][0].Name = f"{building}{replace_string_value}"
        idf1.saveas(f"{save_folder_path}/{building}{replace_string_value}-converted.idf")
    print(f'{idf1.idfobjects["Building".upper()][0].Name} IDF file is converted and saved...')
    return idf1


def create_combined_idf_archetype(save_folder_path, idflist=list):
    """
    Combines all materials, constructions stored in different idfs and merges them into a single idf file

    Run Order:
    1)Gathers all material and construction objects into lists stored in idfs
    2)Selects the base IDF and deletes all construction and material objects
    3)Creates new materials and constructions from the lists created in 1.
    4)Redefines output variables in a way that BuildME accepts
    5)Saves a new idf file, ready to be used with BuildME

    :param save_folder_path: save folder, where the new merged IDF will be saved
    :param idflist: idf list containing the idf files to be merged
                    this list should only contain an archetype type at a time (e.g. only SFH)
    :return: a new merged archetype idf for BuildME
    """

    cons_list = []
    mat_list = []
    matnomass_list = []
    matwin_list = []
    matwinglazing_list = []
    ffloor_list = []
    cwall_list = []
    matshade_list = []
    matshadecontrol_list = []
    framemat_list = []
    merged_idf = ""

    # Gets required objects in all idf files and puts in a list
    for idf in idflist:
        fhandle = StringIO(idf)
        idf = IDF(fhandle)
        for cons in idf.idfobjects["Construction".upper()]:
            cons_list.append(cons)
        for mat in idf.idfobjects["Material".upper()]:
            mat_list.append(mat)
        for matnomass in idf.idfobjects["Material:NoMass".upper()]:
            matnomass_list.append(matnomass)
        for matwin in idf.idfobjects["WindowMaterial:SimpleGlazingSystem".upper()]:
            matwin_list.append(matwin)
        for matwinglazing in idf.idfobjects["WINDOWMATERIAL:GLAZING".upper()]:
            matwinglazing_list.append(matwinglazing)
        for matshade in idf.idfobjects["WindowMaterial:Shade".upper()]:
            matshade_list.append(matshade)
        for matshadecontrol in idf.idfobjects["WindowShadingControl".upper()]:
            matshadecontrol_list.append(matshadecontrol)
        for framemat in idf.idfobjects["WindowProperty:FrameAndDivider".upper()]:
            framemat_list.append(framemat)
        for ffloor in idf.idfobjects["Construction:FfactorGroundFloor".upper()]:
            ffloor_list.append(ffloor)
        for cwall in idf.idfobjects["Construction:CfactorUndergroundWall".upper()]:
            cwall_list.append(cwall)

    # Removes duplicate elements

    newobjects = cons_list + matnomass_list + matwin_list + matwinglazing_list + ffloor_list + mat_list + matshade_list + matshadecontrol_list + framemat_list + cwall_list
    reduced_newobjects = reduce(lambda l, x: l.append(x) or l if x not in l else l, newobjects, [])

    # Selects the base IDF, deletes all of the objects and rewrites new objects from other IDFs
    for idf in idflist:
        fhandle = StringIO(idf)
        idf = IDF(fhandle)
        print(f'Now, {idf.idfobjects["Building".upper()][0].Name} values are being written to the merged IDF...')
        if "BASE" in idf.idfobjects["Building".upper()][0].Name:

            # checking if the IDF file has a DHW system
            water_outputmeter = []

            for item in idf.idfobjects["OUTPUT:VARIABLE"]:
                if "Water" in item.Variable_Name:
                    newwaterobj=idf.newidfobject("OUTPUT:METER")
                    newwaterobj.Key_Name="WaterSystems:DistrictHeating"
                    newwaterobj.Reporting_Frequency="Hourly"
                    water_outputmeter.append(newwaterobj)

            idf.removeallidfobjects("CONSTRUCTION")
            idf.removeallidfobjects("MATERIAL")
            idf.removeallidfobjects("MATERIAL:NOMASS")
            idf.removeallidfobjects("WINDOWMATERIAL:SHADE")
            idf.removeallidfobjects("WINDOWSHADINGCONTROL")
            idf.removeallidfobjects("WINDOWPROPERTY:FRAMEANDDIVIDER")
            idf.removeallidfobjects("WINDOWMATERIAL:SIMPLEGLAZINGSYSTEM")
            idf.removeallidfobjects("WINDOWMATERIAL:GLAZING")
            idf.removeallidfobjects("CONSTRUCTION:FFACTORGROUNDFLOOR")
            idf.removeallidfobjects("CONSTRUCTION:CFACTORUNDERGROUNDWALL")
            # Output Variables needs to be redefined for BuildME
            idf.removeallidfobjects("OUTPUT:VARIABLEDICTIONARY")
            idf.removeallidfobjects("OUTPUT:SURFACES:DRAWING")
            idf.removeallidfobjects("OUTPUT:CONSTRUCTIONS")
            idf.removeallidfobjects("OUTPUT:TABLE:SUMMARYREPORTS")
            idf.removeallidfobjects("OUTPUT:TABLE:MONTHLY")
            idf.removeallidfobjects("OUTPUTCONTROL:TABLE:STYLE")
            idf.removeallidfobjects("OUTPUT:VARIABLE")
            idf.removeallidfobjects("OUTPUT:METER")
            idf.removeallidfobjects("OUTPUT:ENVIRONMENTALIMPACTFACTORS")
            idf.removeallidfobjects("ENVIRONMENTALIMPACTFACTORS")
            idf.removeallidfobjects("OUTPUT:DIAGNOSTICS")
            idf.removeallidfobjects("METER:CUSTOM")
            idf.removeallidfobjects("MATERIAL:INFRAREDTRANSPARENT")

            print("Output Variables are being changed...")
            # New output variables are defined by using existing SFH archetype located in data/archetype folder

            SFH_IDF = IDF("..//data//archetype//USA//SFH.idf")
            outputlist = []
            objlist = ["OUTPUT:METER", "OUTPUT:VARIABLEDICTIONARY", "OUTPUT:SURFACES:DRAWING", "OUTPUT:CONSTRUCTIONS",
                       "OUTPUT:TABLE:SUMMARYREPORTS", "OUTPUT:TABLE:MONTHLY", "OUTPUTCONTROL:TABLE:STYLE",
                       "OUTPUT:VARIABLE"]
            for obj in objlist:
                if obj in [x for x in SFH_IDF.idfobjects]:
                    for item in SFH_IDF.idfobjects[f"{obj}"]:
                        outputlist.append(item)

            for newobj in outputlist:
                idf.copyidfobject(newobj)

            # Checks if there are still duplicates
            seen = set()
            dupes = []
            for x in reduced_newobjects:
                if x.Name in seen:
                    dupes.append(x.Name)
                else:
                    seen.add(x.Name)
                    idf.copyidfobject(x)

            unique = reduce(lambda l, x: l.append(x) or l if x not in l else l, water_outputmeter, [])
            for newmeter in unique:
                idf.copyidfobject(newmeter)

            for obj in idf.idfobjects["Construction".upper()]:
                if obj.Name == "IRTSurface" or obj.Outside_Layer == "IRTMaterial":
                    idf.removeidfobject(obj)

            # Renames the merged IDF
            building = idf.idfobjects["Building".upper()][0].Name
            building = building.split("-")[0]
            idf.idfobjects["Building".upper()][0].Name = building
            building = building.split("BASE")[1]
            idf.saveas(f"{save_folder_path}/{building}-BuildMEReady.idf")
            merged_idf = idf

    print("The new merged idf file is successfully created")
    return merged_idf

def update_replace_csv(idflist, save_folder_path, Region, Occupation,replace_string):
    """
    Creates a new csv file that stores the new values comes from the new idf files.

    :param idflist: list that contains idf files
    :param save_folder_path: Save folder for the csv file
    :param Region: Region
    :param Occupation: Occupation type
    :return: a new replace csv file
    """
    replaceme_file_path = "..\\data\\replace_en-std.csv"
    df = pd.read_csv(replaceme_file_path)
    available_combinations = []
    std_list = ["non-standard", "standard", "efficient", "ZEB"]
    objlist = ['ZONEINFILTRATION:EFFECTIVELEAKAGEAREA', "ZONEINFILTRATION:DESIGNFLOWRATE",
               "ZONEINFILTRATION:FLOWCOEFFICIENT", "AIRFLOWNETWORK:MULTIZONE:SURFACE:CRACK",
               "AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING", "LIGHTS", "OTHEREQUIPMENT",
               "SHADING:BUILDING:DETAILED",
               "AIRFLOWNETWORK:MULTIZONE:SURFACE:CRACK",
               "AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING", "SHADINGPROPERTY:REFLECTANCE"]

    if "en-std-replaceme" in replace_string:
        for idf in idflist:
            fhandle = StringIO(idf)
            idf = IDF(fhandle)
            Standard = idf.idfobjects["Building".upper()][0].Name
            for i in std_list:
                if i in str(Standard):
                    standard = Standard.split("-")[1]
                    if standard == "non":
                        standard = "non-standard"
                    available_combinations.append(standard)

                    for obj in objlist:
                        if obj in [x for x in idf.idfobjects]:
                            # Writing all infiltration parameters
                            if obj == 'ZONEINFILTRATION:EFFECTIVELEAKAGEAREA':
                                for items in idf.idfobjects["ZoneInfiltration:EffectiveLeakageArea".upper()]:
                                    new_row =(
                                    f"{Occupation}", f"{standard}", "ZONEINFILTRATION:EFFECTIVELEAKAGEAREA",
                                    f"{items.Name}", "Effective_Air_Leakage_Area", f"{items.Effective_Air_Leakage_Area}",f"{Region}")
                                    df.loc[len(df.index)] = new_row

                            if obj == "ZONEINFILTRATION:DESIGNFLOWRATE":
                                for items in idf.idfobjects["ZoneInfiltration:DesignFlowRate".upper()]:
                                    new_row = (
                                        f"{Occupation}", f"{standard}", "ZONEINFILTRATION:DESIGNFLOWRATE",
                                        f"{items.Name}",
                                        "Air_Changes_per_Hour", f"{items.Air_Changes_per_Hour}",f"{Region}")
                                    df.loc[len(df.index)] = new_row

                            if obj == "ZONEINFILTRATION:FLOWCOEFFICIENT":
                                for items in idf.idfobjects["ZoneInfiltration:FlowCoefficient".upper()]:
                                    new_row = (
                                         f"{Occupation}", f"{standard}", "ZONEINFILTRATION:FLOWCOEFFICIENT",
                                        f"{items.Name}",
                                        "Flow_Coefficient", f"{items.Flow_Coefficient}",f"{Region}")
                                    df.loc[len(df.index)] = new_row

                            if obj == "AIRFLOWNETWORK:MULTIZONE:SURFACE:CRACK":
                                for items in idf.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE:CRACK".upper()]:
                                    new_row = (
                                         f"{Occupation}", f"{standard}",
                                        "AIRFLOWNETWORK:MULTIZONE:SURFACE:CRACK",
                                        f"{items.Name}",
                                        "Air_Mass_Flow_Coefficient_at_Reference_Conditions",
                                        f"{items.Air_Mass_Flow_Coefficient_at_Reference_Conditions}",f"{Region}")
                                    df.loc[len(df.index)] = new_row

                            if obj == "AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING":
                                for items in idf.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING".upper()]:
                                    new_row = (
                                         f"{Occupation}", f"{standard}",
                                        "AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING",
                                        f"{items.Name}",
                                        "Air_Mass_Flow_Coefficient_When_Opening_is_Closed",
                                        f"{items.Air_Mass_Flow_Coefficient_When_Opening_is_Closed}",f"{Region}")
                                    df.loc[len(df.index)] = new_row

                                for items in idf.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING".upper()]:
                                    new_row = (
                                         f"{Occupation}", f"{standard}",
                                        "AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING",
                                        f"{items.Name}",
                                        "Air_Mass_Flow_Exponent_When_Opening_is_Closed",
                                        f"{items.Air_Mass_Flow_Exponent_When_Opening_is_Closed}",f"{Region}")
                                    df.loc[len(df.index)] = new_row

                            if obj == "LIGHTS":
                                for items in idf.idfobjects["LIGHTS".upper()]:
                                    new_row = (
                                        f"{Occupation}", f"{standard}", "LIGHTS",
                                        f"{items.Name}",
                                        "Watts_per_Zone_Floor_Area", f"{items.Watts_per_Zone_Floor_Area}",f"{Region}")
                                    df.loc[len(df.index)] = new_row

                            if obj == "OTHEREQUIPMENT":
                                for items in idf.idfobjects["OTHEREQUIPMENT".upper()]:
                                    new_row = (
                                        f"{Occupation}", f"{standard}", "OTHEREQUIPMENT",
                                        f"{items.Name}",
                                        "Power_per_Zone_Floor_Area", f"{items.Power_per_Zone_Floor_Area}",f"{Region}")
                                    df.loc[len(df.index)] = new_row

                            if obj == "SHADING:BUILDING:DETAILED":
                                for items in idf.idfobjects["SHADING:BUILDING:DETAILED".upper()]:
                                    new_row = (
                                        f"{Occupation}", f"{standard}", "SHADING:BUILDING:DETAILED",
                                        f"{items.Name}",
                                        "Transmittance_Schedule_Name", f"{items.Transmittance_Schedule_Name}",f"{Region}")
                                    df.loc[len(df.index)] = new_row

                            if obj == "SHADINGPROPERTY:REFLECTANCE":
                                for items in idf.idfobjects["SHADINGPROPERTY:REFLECTANCE".upper()]:
                                    new_row = (
                                         f"{Occupation}", f"{standard}", "SHADINGPROPERTY:REFLECTANCE",
                                        f"{items.Shading_Surface_Name}",
                                        "Glazing_Construction_Name", f"{items.Glazing_Construction_Name}",f"{Region}")
                                    df.loc[len(df.index)] = new_row

                            if obj == "AIRFLOWNETWORK:MULTIZONE:SURFACE:CRACK":
                                for items in idf.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE:CRACK".upper()]:
                                    new_row = (
                                        f"{Occupation}", f"{standard}", "AIRFLOWNETWORK:MULTIZONE:SURFACE:CRACK",
                                        f"{items.Name}",
                                        "Air_Mass_Flow_Coefficient_at_Reference_Conditions",
                                        f"{items.Air_Mass_Flow_Coefficient_at_Reference_Conditions}",f"{Region}")
                                    df.loc[len(df.index)] = new_row

                            if obj == "AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING":
                                for items in idf.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING".upper()]:
                                    new_row = (
                                         f"{Occupation}", f"{standard}",
                                        "AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING",
                                        f"{items.Name}",
                                        "Air_Mass_Flow_Coefficient_When_Opening_is_Closed",
                                        f"{items.Air_Mass_Flow_Coefficient_When_Opening_is_Closed}",f"{Region}")
                                    df.loc[len(df.index)] = new_row

                                    new_row = (
                                         f"{Occupation}", f"{standard}",
                                        "AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING",
                                        f"{items.Name}",
                                        "Air_Mass_Flow_Exponent_When_Opening_is_Closed",
                                        f"{items.Air_Mass_Flow_Exponent_When_Opening_is_Closed}",f"{Region}")
                                    df.loc[len(df.index)] = new_row
            df.drop_duplicates(subset=["Occupation","standard","idfobject","Name","objectfield","Value","Comment"], keep='last')
            df.to_csv(f"{save_folder_path}\\replace_en-std_updated.csv")

    if "chr-replaceme" in replace_string:
        df= df.drop(df.index[0:])
        df.columns=["Occupation","cohort","idfobject","Name","objectfield","Value","Comment"]
        available_combinations = []
        for idf in idflist:
            fhandle = StringIO(idf)
            idf = IDF(fhandle)
            Standard = idf.idfobjects["Building".upper()][0].Name
            cohort = Standard.split("-")[1]
            available_combinations.append(cohort)
            for obj in objlist:
                if obj in [x for x in idf.idfobjects]:
                    if obj == 'ZONEINFILTRATION:EFFECTIVELEAKAGEAREA':
                        for items in idf.idfobjects["ZoneInfiltration:EffectiveLeakageArea".upper()]:
                            new_row =(
                            f"{Occupation}", f"{cohort}", "ZONEINFILTRATION:EFFECTIVELEAKAGEAREA",
                            f"{items.Name}", "Effective_Air_Leakage_Area", f"{items.Effective_Air_Leakage_Area}",f"{Region}")
                            df.loc[len(df.index)] = new_row

                    if obj == "ZONEINFILTRATION:DESIGNFLOWRATE":
                        for items in idf.idfobjects["ZoneInfiltration:DesignFlowRate".upper()]:
                            new_row = (
                                f"{Occupation}", f"{cohort}", "ZONEINFILTRATION:DESIGNFLOWRATE",
                                f"{items.Name}",
                                "Air_Changes_per_Hour", f"{items.Air_Changes_per_Hour}",f"{Region}")
                            df.loc[len(df.index)] = new_row

                    if obj == "ZONEINFILTRATION:FLOWCOEFFICIENT":
                        for items in idf.idfobjects["ZoneInfiltration:FlowCoefficient".upper()]:
                            new_row = (
                                 f"{Occupation}", f"{cohort}", "ZONEINFILTRATION:FLOWCOEFFICIENT",
                                f"{items.Name}",
                                "Flow_Coefficient", f"{items.Flow_Coefficient}",f"{Region}")
                            df.loc[len(df.index)] = new_row

                    if obj == "AIRFLOWNETWORK:MULTIZONE:SURFACE:CRACK":
                        for items in idf.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE:CRACK".upper()]:
                            new_row = (
                                 f"{Occupation}", f"{cohort}",
                                "AIRFLOWNETWORK:MULTIZONE:SURFACE:CRACK",
                                f"{items.Name}",
                                "Air_Mass_Flow_Coefficient_at_Reference_Conditions",
                                f"{items.Air_Mass_Flow_Coefficient_at_Reference_Conditions}",f"{Region}")
                            df.loc[len(df.index)] = new_row

                    if obj == "AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING":
                        for items in idf.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING".upper()]:
                            new_row = (
                                 f"{Occupation}", f"{cohort}",
                                "AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING",
                                f"{items.Name}",
                                "Air_Mass_Flow_Coefficient_When_Opening_is_Closed",
                                f"{items.Air_Mass_Flow_Coefficient_When_Opening_is_Closed}",f"{Region}")
                            df.loc[len(df.index)] = new_row

                        for items in idf.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING".upper()]:
                            new_row = (
                                 f"{Occupation}", f"{cohort}",
                                "AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING",
                                f"{items.Name}",
                                "Air_Mass_Flow_Exponent_When_Opening_is_Closed",
                                f"{items.Air_Mass_Flow_Exponent_When_Opening_is_Closed}",f"{Region}")
                            df.loc[len(df.index)] = new_row

                    if obj == "LIGHTS":
                        for items in idf.idfobjects["LIGHTS".upper()]:
                            new_row = (
                                f"{Occupation}", f"{cohort}", "LIGHTS",
                                f"{items.Name}",
                                "Watts_per_Zone_Floor_Area", f"{items.Watts_per_Zone_Floor_Area}",f"{Region}")
                            df.loc[len(df.index)] = new_row

                    if obj == "OTHEREQUIPMENT":
                        for items in idf.idfobjects["OTHEREQUIPMENT".upper()]:
                            new_row = (
                                f"{Occupation}", f"{cohort}", "OTHEREQUIPMENT",
                                f"{items.Name}",
                                "Power_per_Zone_Floor_Area", f"{items.Power_per_Zone_Floor_Area}",f"{Region}")
                            df.loc[len(df.index)] = new_row

                    if obj == "SHADING:BUILDING:DETAILED":
                        for items in idf.idfobjects["SHADING:BUILDING:DETAILED".upper()]:
                            new_row = (
                                f"{Occupation}", f"{cohort}", "SHADING:BUILDING:DETAILED",
                                f"{items.Name}",
                                "Transmittance_Schedule_Name", f"{items.Transmittance_Schedule_Name}",f"{Region}")
                            df.loc[len(df.index)] = new_row

                    if obj == "SHADINGPROPERTY:REFLECTANCE":
                        for items in idf.idfobjects["SHADINGPROPERTY:REFLECTANCE".upper()]:
                            new_row = (
                                 f"{Occupation}", f"{cohort}", "SHADINGPROPERTY:REFLECTANCE",
                                f"{items.Shading_Surface_Name}",
                                "Glazing_Construction_Name", f"{items.Glazing_Construction_Name}",f"{Region}")
                            df.loc[len(df.index)] = new_row

                    if obj == "AIRFLOWNETWORK:MULTIZONE:SURFACE:CRACK":
                        for items in idf.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE:CRACK".upper()]:
                            new_row = (
                                f"{Occupation}", f"{cohort}", "AIRFLOWNETWORK:MULTIZONE:SURFACE:CRACK",
                                f"{items.Name}",
                                "Air_Mass_Flow_Coefficient_at_Reference_Conditions",
                                f"{items.Air_Mass_Flow_Coefficient_at_Reference_Conditions}",f"{Region}")
                            df.loc[len(df.index)] = new_row

                    if obj == "AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING":
                        for items in idf.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING".upper()]:
                            new_row = (
                                 f"{Occupation}", f"{cohort}",
                                "AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING",
                                f"{items.Name}",
                                "Air_Mass_Flow_Coefficient_When_Opening_is_Closed",
                                f"{items.Air_Mass_Flow_Coefficient_When_Opening_is_Closed}",f"{Region}")
                            df.loc[len(df.index)] = new_row

                            new_row = (
                                 f"{Occupation}", f"{cohort}",
                                "AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING",
                                f"{items.Name}",
                                "Air_Mass_Flow_Exponent_When_Opening_is_Closed",
                                f"{items.Air_Mass_Flow_Exponent_When_Opening_is_Closed}",f"{Region}")
                            df.loc[len(df.index)] = new_row
            df.drop_duplicates(subset=["Occupation","cohort","idfobject","Name","objectfield","Value","Comment"], keep='last')
            df.to_csv(f"{save_folder_path}\\replace_cohort_updated.csv")

    if "res-replaceme" in replace_string:
        replaceme_file_path = "..\\data\\replace_res.csv"
        df = pd.read_csv(replaceme_file_path)
        for idf in idflist:
            fhandle = StringIO(idf)
            idf = IDF(fhandle)
            RES = idf.idfobjects["Building".upper()][0].Name
            RES = RES.split("-")[2]
            available_combinations.append(RES)
            new_row = (
                f"{Occupation}", f"{RES}","People","Number_of_People","people_unit1","3","Added by IDF Converter")
            df.loc[len(df.index)] = new_row

        df.drop_duplicates(subset=["Occupation", "RES", "idfobject", "Name", "objectfield", "Value", "Comment"],
                           keep='last')
        df.to_csv(f"{save_folder_path}\\replace_res_updated.csv")
        available_combinations = reduce(lambda l, x: l.append(x) or l if x not in l else l, available_combinations, [])
        return available_combinations



def update_all_datafile_csv(idflist, save_folder_path,replace_string):
    """
    Creates csv files

    :param idflist: list that contains idf files
    :param merged_idf: Merged IDF file
    :param save_folder_path: save folder for conversion outputs
    :return: summary
    """

    def colored(r, g, b, text):
        return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)

    Region = input(colored(0, 255, 255, "Please specify a region name (i.e., USA, UK):"))
    Occupation = input(colored(0, 255, 255, "Please specify the occupancy type (i.e., SFH, MFH, RT):"))
    available_combinations = update_replace_csv(idflist, save_folder_path, Region, Occupation, replace_string)
    print(" \n")
    print(colored(102, 204, 0,
                  f"SUMMARY:\nThe conversion is completed: The following debugging combinations can be used now:\n{Region}, {Occupation}, {available_combinations}\n\n"))
    print(colored(255, 255, 51,
                  "NEXT STEPS:\n 1. Please update BuildME_config_V1.0.xlsx according to the new idf combinations\n 2. Select a weather file\n 3. Replace the existing replace.csv files located in data folder with the newly created ones\n \n\n"))
    print(colored(255, 0, 0,
                  "CAUTION:\n 1. You need to run your new file with BuildME first in order to get the atypical materials and general material aggregations unique to the new converted files"))


if __name__ == "__main__":

    #USER SPECIFIC INPUTS:
    #EXAMPLE PURPOSES ONLY

    # 1st IDF to be converted:standard
    path1 = "..\\data\\archetype\\new_archetypes\\SFH_tobeconverted.idf"
    # 2nd IDF to be converted:efficient
    path2 = "..\\data\\archetype\\new_archetypes\\SFHefficient_tobeconverted.idf"

    # Main Folder, every generated data will be located
    # Tip: make sure to put the 'r' in front
    folderpath = r"..\\data\\archetype\\new_archetypes\\new"

    #replace_string should start with "-" and end with "-replaceme"
    convert_idf_to_BuildME(path1, folderpath, replace_string="-en-std-replaceme-res-replaceme",replace_string_value="-standard-RES0", base=True)
    convert_idf_to_BuildME(path2, folderpath, replace_string="-en-std-replaceme-res-replaceme",replace_string_value="-efficient-RES0", base=False)
    #On demand, a non-standard option for the IDF is also can be created by assigning 30% worse performing values to the standard file.
    convert_idf_to_BuildME(path1, folderpath, replace_string="-en-std-replaceme-res-replaceme",
                           replace_string_value="-non-standard-RES0", base=False)


    listed = create_combined_idflist(folderpath)
    merged_idf=create_combined_idf_archetype(folderpath, listed)
    update_all_datafile_csv(listed,folderpath,replace_string="-chr-replaceme-res-replaceme")