"""
Functions to adapt custom IDF files to BuildME.
Use these to automatically insert replaceme strings on surface objects,
to rename materials/constructions based on standards/resource efficiency scenarios.
to merge idfs that have different materials/constructions

Missing Features:
-Different RES values (Currently RES0 is implemented only as a placeholder)
-FFactorConstructions/CFactorConstructions are implemented similar to common construction framework;
after we decide what are we going to do with these objects, we can address them once again to make them be
included in material intensity calculations.

TODO:
Sahin thinks it would be nice to automatically fill out the followinf fields from the idfs.
- replace.xlsx (Infiltration Values)
- material.xlsx (NoMass etc.)
"""

from eppy import modeleditor
from eppy.modeleditor import IDF
import eppy
import os
import platform
from functools import reduce
from io import StringIO

# Standalone Run Requirements
ep_version = '9.2.0'
basepath = os.path.abspath('.')
ep_path = os.path.abspath("C:\\Users\\sahina\\PycharmProjects\\BuildME-master\\bin\\EnergyPlus-9-2-0")
ep_idd = os.path.abspath("C:\\Users\\sahina\\PycharmProjects\\BuildME-master\\bin\\EnergyPlus-9-2-0\\Energy+.idd")
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


def convert_idf_to_BuildME(idf_path, save_folder_path, replacer_std="-en-non-standard", replacer_res="-RES0"):
    """
    This function creates separate edited IDF file that is compatible with BuildME framework

    Requirements for a clear run:
    1)Window-Skylight Difference should be addressed in construction name (e.g. name contains "sky")
    2)Internal-External Wall Difference should be addressed in construction name (e.g. name contains "int_wall")
    3)Floor Difference should be addressed in construction name (e.g. name contains "int_wall")

     Run Order:
    -Adds replaceme fields,
    -Renames Materials,
    -Renames Constructions,
    -Defines non-standard U values; if replacer_std is set accordingly.

    :param idf_path: path for idf file to be converted, standard file should be used forthe non-standard IDF creation
    :param replacer_std: Energy standard (i.e.,-en-non-standard, -en-standard)
    :param replacer_res: Resource Efficiency Scenario name (only applies the string for now) (i.e., RES0)
    :param save_folder_path: New location folder path, where the new IDF will be saved
    :return: A compatible file with BuildME for a specific standard-RES
    """

    idf1 = IDF(idf_path)

    # CONVERTING CONSTRUCTION NAMES AND INSERTING REPLACEME STRING:
    # It replaces the surface construction with replaceme string, adds a new identical construction to the model
    # and renames the construction corresponding to the replaceme string

    for items in idf1.idfobjects["BuildingSurface:Detailed".upper()]:
        for obj in idf1.idfobjects["Construction".upper()]:
            if obj.Name == items.Construction_Name:

                if items.Surface_Type == "Roof":
                    items.Construction_Name = "ext-roof-en-std-replaceme-res-replaceme"
                    newcons = idf1.copyidfobject(obj)
                    newcons.Name = f"ext-roof{replacer_std}{replacer_res}"

                if items.Surface_Type == "Ceiling":
                    if "int" or "ceiling" in items.Construction_Name:
                        items.Construction_Name = "int-ceiling-en-std-replaceme-res-replaceme"
                        newcons = idf1.copyidfobject(obj)
                        newcons.Name = f"int-ceiling{replacer_std}{replacer_res}"

                # !!!!!!!FLOOR STUFF WILL BE DECIDED LATER AS WE DO NOT KNOW IF WE WILL USE A SURROGATE ELEMENT
                if items.Surface_Type == "Floor":
                    if "int" in items.Construction_Name:
                        items.Construction_Name = "int-floor-en-std-replaceme-res-replaceme"
                        newcons = idf1.copyidfobject(obj)
                        newcons.Name = f"int-floor{replacer_std}{replacer_res}"
                    if items.Outside_Boundary_Condition == "Adiabatic":
                        items.Construction_Name = "basement-floor-en-std-replaceme-res-replaceme"
                        newcons = idf1.copyidfobject(obj)
                        newcons.Name = f"basement-floor{replacer_std}{replacer_res}"
                    else:
                        items.Construction_Name = "ext-floor-en-std-replaceme-res-replaceme"
                        newcons = idf1.copyidfobject(obj)
                        newcons.Name = f"ext-floor{replacer_std}{replacer_res}"

                if items.Surface_Type == "Wall":

                    if "int" in items.Construction_Name:
                        items.Construction_Name = "int-wall-en-std-replaceme-res-replaceme"
                        newcons = idf1.copyidfobject(obj)
                        newcons.Name = f"int-wall{replacer_std}{replacer_res}"
                    else:
                        items.Construction_Name = "ext-wall-en-std-replaceme-res-replaceme"
                        newcons = idf1.copyidfobject(obj)
                        newcons.Name = f"ext-wall{replacer_std}{replacer_res}"

        # !!!!!!!FLOOR STUFF WILL BE DECIDED LATER AS WE DO NOT KNOW IF WE WILL USE A SURROGATE ELEMENT
        if 'CONSTRUCTION:FFACTORGROUNDFLOOR' in [x for x in idf1.idfobjects]:
            for floor in idf1.idfobjects["Construction:FfactorGroundFloor".upper()]:
                if floor.Name == items.Construction_Name:
                    if items.Surface_Type == "Floor" and items.Outside_Boundary_Condition == "GroundFCfactorMethod" or items.Outside_Boundary_Condition == "Adiabatic":
                        items.Construction_Name = f"{items.Construction_Name}-en-std-replaceme-res-replaceme"
                        newcons = idf1.copyidfobject(floor)
                        newcons.Name = f"{floor.Name}{replacer_std}{replacer_res}"
        # !!!!!!!FLOOR STUFF WILL BE DECIDED LATER AS WE DO NOT KNOW IF WE WILL USE A SURROGATE ELEMENT
        if 'CONSTRUCTION:CFACTORUNDERGROUNDWALL' in [x for x in idf1.idfobjects]:
            for wall in idf1.idfobjects["Construction:CfactorUndergroundWall".upper()]:
                if wall.Name == items.Construction_Name:
                    if items.Surface_Type == "Wall" and items.Outside_Boundary_Condition == "GroundFCfactorMethod" or items.Outside_Boundary_Condition == "Adiabatic":
                        items.Construction_Name = f"{items.Construction_Name}-en-std-replaceme-res-replaceme"
                        newcons = idf1.copyidfobject(wall)
                        newcons.Name = f"{wall.Name}{replacer_std}{replacer_res}"

    if 'WINDOW' in [x for x in idf1.idfobjects]:
        for fenest in idf1.idfobjects["Window".upper()]:
            fenest.Construction_Name = "ext-window-en-std-replaceme"

    if 'DOOR' in [x for x in idf1.idfobjects]:
        for fenest in idf1.idfobjects["Door".upper()]:
            fenest.Construction_Name = "ext-door-en-std-replaceme"

    if 'FENESTRATIONSURFACE:DETAILED' in [x for x in idf1.idfobjects]:
        for fenest in idf1.idfobjects["FenestrationSurface:Detailed".upper()]:
            for obj in idf1.idfobjects["Construction".upper()]:
                if fenest.Construction_Name == obj.Name:
                    if fenest.Surface_Type == "Window":
                        # there might be skylights:
                        if "sky" in fenest.Construction_Name:
                            fenest.Construction_Name = "ext-skywindow-en-std-replaceme"
                            newcons = idf1.copyidfobject(obj)
                            newcons.Name = f"ext-skywindow{replacer_std}{replacer_res}"
                        else:
                            fenest.Construction_Name = "ext-window-en-std-replaceme"
                            newcons = idf1.copyidfobject(obj)
                            newcons.Name = f"ext-window{replacer_std}{replacer_res}"
                    else:
                        fenest.Construction_Name = "ext-door-en-std-replaceme"
                        newcons = idf1.copyidfobject(obj)
                        newcons.Name = f"ext-door{replacer_std}{replacer_res}"

    # Deleting duplicated construction names
    unique = reduce(lambda l, x: l.append(x) or l if x not in l else l, idf1.idfobjects["Construction".upper()], [])
    idf1.removeallidfobjects("CONSTRUCTION")
    for newcons in unique:
        idf1.copyidfobject(newcons)

    # !!!!!!!FLOOR STUFF WILL BE DECIDED LATER AS WE DO NOT KNOW IF WE WILL USE A SURROGATE ELEMENT
    if 'CONSTRUCTION:FFACTORGROUNDFLOOR' in [x for x in idf1.idfobjects]:
        unique = reduce(lambda l, x: l.append(x) or l if x not in l else l,
                        idf1.idfobjects["Construction:FfactorGroundFloor".upper()], [])
        idf1.removeallidfobjects("CONSTRUCTION:FFACTORGROUNDFLOOR")
    for newcons in unique:
        idf1.copyidfobject(newcons)

    # CONVERTING MATERIAL
    # For the en-non-standard version, values are replaced with %30 worse performing numbers based on the standard version.
    if replacer_std == "-en-non-standard":
        for items in idf1.idfobjects["Material".upper()]:
            items.Conductivity = float(items.Conductivity) * 1.3
            items.Name = f"{items.Name}-en-non-standard"
        for items in idf1.idfobjects["Material:NoMass".upper()]:
            items.Thermal_Resistance = float(items.Thermal_Resistance) * 0.7
            items.Name = f"{items.Name}-en-non-standard"
        for items in idf1.idfobjects["WindowMaterial:SimpleGlazingSystem".upper()]:
            items.UFactor = float(items.UFactor) * 1.3
            items.Name = f"{items.Name}-en-non-standard"
        if 'CONSTRUCTION:FFACTORGROUNDFLOOR' in [x for x in idf1.idfobjects]:
            for items in idf1.idfobjects["Construction:FfactorGroundFloor".upper()]:
                items.FFactor = float(items.FFactor) * 1.3
    # Material names are changed as they represent different values across standards, some identifiers are added.
    else:
        for items in idf1.idfobjects["Material".upper()]:
            items.Name = f"{items.Name}{replacer_std}"
        for items in idf1.idfobjects["Material:NoMass".upper()]:
            items.Name = f"{items.Name}{replacer_std}"
        for items in idf1.idfobjects["WindowMaterial:SimpleGlazingSystem".upper()]:
            items.Name = f"{items.Name}{replacer_std}"

    # Construction material layer names are matched with above material changes
    for items in idf1.idfobjects["Construction".upper()]:
        for fields in items.fieldnames:
            if fields == "key":
                continue
            if fields == "Name":
                continue
            else:
                if items[fields] == "":
                    continue
                else:
                    items[fields] = items[fields] + f"{replacer_std}"

    # SAVING IDF FILE
    building = str(idf1.idfobjects["Building".upper()][0].Name)
    idf1.idfobjects["Building".upper()][0].Name = f"{building}{replacer_std}{replacer_res}"
    idf1.saveas(f"{save_folder_path}/{building}{replacer_std}{replacer_res}.idf")
    return idf1


def create_combined_idflist(folderpath):
    """
    Creates a list containing the generated idf files
    :param folderpath: folderpath containing all generated idfs for standards/res scenarios for a single archetype type (e.g. RT only)
    :return: combined idf list
    """
    filepaths = [os.path.join(folderpath, name) for name in os.listdir(folderpath)]
    all_files = []
    for path in filepaths:
        if "-RES" in path:
            with open(path, 'r') as f:
                file = f.read()
                all_files.append(file)

    return all_files


def create_combined_idf_archetype(save_folder_path, idflist=list):
    """
    Combines all materials, constructions in different idfs and merges them into a single idf file

    Work Order:
    1)Gathers all material and construction objects into lists in all idfs
    2)Selects the standard version and deletes all construction and material objects
    3)Creates new materials and constructions from the lists created in stage 1.
    4)Saves a new idf file, ready to be used with BuildME

    :param idflist: idf list containing the idf files to be merged
                    this list should only contain an archetype type at a time (e.g. only SFH)
    :param save_folder_path: New location folder path, where the new IDF will be saved
    :return: idf: new archetype idf for BuildME
    """
    cons_list = []
    mat_list = []
    matnomass_list = []
    matwin_list = []
    ffloor_list = []

    # gets required objects in all idf files and puts in a list
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
        for ffloor in idf.idfobjects["Construction:FfactorGroundFloor".upper()]:
            ffloor_list.append(ffloor)

    # removes duplicate elements
    cons_list = reduce(lambda l, x: l.append(x) or l if x not in l else l, cons_list, [])
    mat_list = reduce(lambda l, x: l.append(x) or l if x not in l else l, mat_list, [])
    matnomass_list = reduce(lambda l, x: l.append(x) or l if x not in l else l, matnomass_list, [])
    matwin_list = reduce(lambda l, x: l.append(x) or l if x not in l else l, matwin_list, [])
    ffloor_list = reduce(lambda l, x: l.append(x) or l if x not in l else l, ffloor_list, [])
    newobjects = cons_list + matnomass_list + matwin_list + ffloor_list + mat_list
    reduced_newobjects = reduce(lambda l, x: l.append(x) or l if x not in l else l, newobjects, [])

    # finds standard version and uses it as a base to create new merged idf
    for idf in idflist:
        fhandle = StringIO(idf)  # we can make a file handle of a string
        idf = IDF(fhandle)
        print(idf.idfobjects["Building".upper()][0].Name)
        if "-en-standard" in idf.idfobjects["Building".upper()][0].Name:
            print("standard file is found,new idf is creating...")
            idf.removeallidfobjects("CONSTRUCTION")
            idf.removeallidfobjects("MATERIAL")
            idf.removeallidfobjects("MATERIAL:NOMASS")
            idf.removeallidfobjects("WINDOWMATERIAL:SIMPLEGLAZINGSYSTEM")
            idf.removeallidfobjects("CONSTRUCTION:FFACTORGROUNDFLOOR")

            # Checks if there are still duplicates
            seen = set()
            dupes = []
            for x in reduced_newobjects:
                if x.Name in seen:
                    dupes.append(x.Name)
                else:
                    seen.add(x.Name)
                    idf.copyidfobject(x)

            building = idf.idfobjects["Building".upper()][0].Name
            building = building.split("-")[0]
            idf.saveas(f"{save_folder_path}/{building}-BuildME.idf")
    print("The new idf file is successfully created")
    return


# 2006 IECC idf File Path (standard)
path1 = "C:\\Users\\sahina\\PycharmProjects\\BuildME-master\\data\\archetype\\new_archetypes\\IdealLoads\\BUILDME_HotelLarge\\IdealLoads_HotelLarge.idf"

# 2012 IECC idf File Path (efficient)
path2 = "C:\\Users\\sahina\\PycharmProjects\\BuildME-master\\data\\archetype\\new_archetypes\\IdealLoads\\BUILDME_HotelLarge\\IECC_HotelLarge_STD2012_NewYork.idf"

# 2018 IECC File Path (ZEB)
path3 = "C:\\Users\\sahina\\PycharmProjects\\BuildME-master\\data\\archetype\\new_archetypes\\IdealLoads\\BUILDME_HotelLarge\\IECC_HotelLarge_STD2018_NewYork.idf"

# Main Folder, every generated data will be located
# Tip: make sure to put the 'r' in front
folderpath = r"C:\\Users\\sahina\\PycharmProjects\\BuildME-master\\data\\archetype\\new_archetypes\\IdealLoads\\BUILDME_HotelLarge"

convert_idf_to_BuildME(path1, folderpath, replacer_std="-en-non-standard", replacer_res="-RES0")
convert_idf_to_BuildME(path1, folderpath, replacer_std="-en-standard", replacer_res="-RES0")
convert_idf_to_BuildME(path2, folderpath, replacer_std="-en-efficient", replacer_res="-RES0")
convert_idf_to_BuildME(path3, folderpath, replacer_std="-en-ZEB", replacer_res="-RES0")

listed = create_combined_idflist(folderpath)
create_combined_idf_archetype(folderpath, listed)
