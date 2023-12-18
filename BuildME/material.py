"""
Functions to manipulate the IDF files.

Copyright: Niko Heeren, 2019
"""
import collections
import math
import os
import numpy as np
import pandas as pd
from eppy.modeleditor import IDF
import eppy.function_helpers
import statistics


def perform_materials_calculation(idf_file, out_dir, atypical_materials, surrogates_dict,
                                  ifsurrogates=True, replace_dict=None):
    # find the materials used in the building
    materials = make_materials_dict(idf_file)
    # find the density of each material
    densities = make_mat_density_dict(materials, atypical_materials)
    # find the thicknesses of material layers in various construction types
    constr_layers = make_construction_dict(idf_file, materials, atypical_materials, replace_dict)
    # calculate the total area of surfaces (including surfaces from zone multipliers and surrogate surfaces)
    surfaces = get_surfaces(idf_file)
    surfaces = get_surfaces_from_floor_multipliers(idf_file, surfaces)
    # add the total floor area and other area measures
    geom_stats = get_building_geometry_stats(idf_file, surfaces)
    save_dict_to_csv(geom_stats, out_dir, 'geom_stats.csv', header=['Geometry statistics', 'Unit', 'Value'],
                     units_dict={'area': 'm^2', 'perimeter': 'm', 'height': 'm', 'num_of_floors': 'floors'})
    # calculate the total material volume (thickness * total area, by material)
    mat_vol_bdg = calc_mat_vol_bdg(idf_file, surfaces, constr_layers)
    # add surrogate materials
    # calculate the total mass (total volume/density, by material)
    mat_mass = {mat: mat_vol_bdg[mat] * densities[mat] for mat in mat_vol_bdg}
    if ifsurrogates:
        for key, calc_dict in surrogates_dict.items():
            if all(v == 0 for k, v in calc_dict.items()):
                continue
            elif key == 'basement':
                mat_mass = add_surrogate_basement(mat_mass, geom_stats, **surrogates_dict['basement'])
            elif key == 'foundation':
                mat_mass = add_surrogate_foundation(mat_mass, geom_stats, **surrogates_dict['foundation'])
            elif key == 'beams':
                mat_mass = add_surrogate_beams(mat_mass, geom_stats, **surrogates_dict['beams'])
            elif key == 'columns':
                mat_mass = add_surrogate_columns(mat_mass, geom_stats, **surrogates_dict['columns'])
            elif key == 'studs':
                mat_mass = add_surrogate_studs(mat_mass, geom_stats, **surrogates_dict['studs'])
            elif key == 'roof_beams':
                mat_mass = add_surrogate_roof_beams(mat_mass, geom_stats, **surrogates_dict['roof_beams'])
            elif key == 'shear_walls':
                mat_mass = add_surrogate_shear_walls(mat_mass, geom_stats, **surrogates_dict['shear_walls'])
            else:
                print(f'Warning: surrogate element {key} not recognized')
    # export
    save_dict_to_csv(mat_mass, out_dir, 'mat_demand.csv', header=['Material name', 'Unit', 'Value'],
                     units_dict={'': 'kg'})


def make_materials_dict(idf_file):
    """
    Takes the IDF file, extracts all material types and places them into a dictionary with the .Name attribute
    as the key, and the idf object as the value, e.g., {material.Name: material}
    :param idff: IDF file
    :return: dictionary with the .Name attribute as the key {material.Name: material}
    """
    # create a list of idf material objects
    materials = []
    for mtype in ['Material', 'Material:NoMass', 'Material:AirGap',
                  'WindowMaterial:SimpleGlazingSystem', 'WindowMaterial:Blind', 'WindowMaterial:Shade',
                  'WindowMaterial:Glazing']:
        materials = materials + [i for i in idf_file.idfobjects[mtype.upper()]]
    # check if no duplicates
    object_names = [io.Name for io in materials]
    duplicates = [item for item, count in collections.Counter(object_names).items() if count > 1]
    assert len(duplicates) == 0, "Duplicate entries for IDF object: '%s'" % duplicates
    # create a dictionary with names and objects
    materials_dict = {m.Name: m for m in materials}
    return materials_dict


def make_mat_density_dict(materials_dict, atypical_materials):
    """
    Creates a dictionary of material densities by material.
    :param materials_dict: Materials from the IDF file
    :return:
    """
    densities = {}
    for mat in materials_dict:
        # Some materials, such as Material:No Mass have no density attribute
        if hasattr(materials_dict[mat], 'Density'):
            densities[mat] = materials_dict[mat].Density
        else:
            try:
                densities[mat] = atypical_materials[mat]['density']
            except KeyError:
                raise KeyError(f"Material {mat} was not found in material.csv")
    if 'Concrete_surrogate' not in densities.keys():
        densities['Concrete_surrogate'] = 2200
    if 'Insulation_surrogate' not in densities.keys():
        densities['Insulation_surrogate'] = 120
    if 'Reinforcement_surrogate' not in densities.keys():
        densities['Reinforcement_surrogate'] = 7850
    return densities


def make_construction_dict(idf_file, materials_dict, atypical_materials, replace_dict):
    """
    Calculates the material volume in 1 m2 of a construction
    :param idf_file:
    :param materials_dict:
    :return: {'construction_name': {}
    """
    constructions = idf_file.idfobjects['Construction'.upper()]
    constr_layers = {}
    for construction in constructions:
        constr_layers[construction.Name] = {}
        layers = extract_layers(construction)
        for layer in layers:
            obj = materials_dict[layers[layer]]
            if hasattr(obj, 'Thickness'):
                thickness = obj.Thickness
            else:
                try:
                    thickness = float(atypical_materials[layers[layer]]['thickness'])
                except KeyError:
                    raise KeyError(f"Material {obj.Name} was not found in material.csv")
            if layers[layer] not in constr_layers[construction.Name]:
                constr_layers[construction.Name][layers[layer]] = thickness
            else:
                constr_layers[construction.Name][layers[layer]] += thickness

    # create constructions for objects Construction:FfactorGroundFloor and Construction:CfactorUndergroundWall
    Ffactor_objs = idf_file.idfobjects['Construction:FfactorGroundFloor'.upper()]
    Cfactor_objs = idf_file.idfobjects['Construction:CfactorUndergroundWall'.upper()]
    for obj in Ffactor_objs:
        constr_layers = add_ground_floor_ffactor_cfactor(constr_layers, obj, replace_dict)
    for obj in Cfactor_objs:
        constr_layers = add_ground_floor_ffactor_cfactor(constr_layers, obj, replace_dict)
    return constr_layers


def extract_layers(construction):
    # TODO description
    layers_dict = {}
    layers = ['Outside_Layer'] + ['Layer_' + str(i + 2) for i in range(9)]
    for layer in layers:
        if getattr(construction, layer) == '':
            break  # first empty value found
        layers_dict[layer] = getattr(construction, layer)
    return layers_dict


class SurrogateElement:
    """
    A surrogate class for windows and doors, because e.g. idf.idfobjects['Window'.upper()] does not contain an 'area'
    attribute. See also https://github.com/santoshphilip/eppy/issues/230.
    """
    def __init__(self, g):
        if type(g) == dict:
            self.area = g['area']
            self.Building_Surface_Name = g['Building_Surface_Name']
            self.Construction_Name = g['Construction_Name']
            self.key = g['key']
            self.Name = g['Name']
        else:
            self.area = g.Length * g.Height
            self.Building_Surface_Name = g.Building_Surface_Name
            self.Construction_Name = g.Construction_Name
            self.key = g.key
            self.Name = g.Name
            # self.Outside_Boundary_Condition = g.Outside_Boundary_Condition
            # self.Zone_Name = g.Zone_Name
            # self.Surface_Type = g.Surface_Type


def calc_mat_vol_bdg(idff, surfaces, constr_layers):
    """
    Calculate building's total material intensity.
    :param surfaces:
    :param mat_m2: material thickness per element and layer,
        e.g. { 'AtticRoofDeck': {'F12 Asphalt shingles': 0.0032, 'G02 16mm plywood': 0.0159}, ...}
    :return: Dictionary with material and volume
    """
    mat_vol = {}
    flat_surfaces = flatten_surfaces(surfaces)
    for surface in flat_surfaces:
        fenestration = get_fenestration_objects_from_surface(idff, surface)
        if fenestration is None:
            area = get_area(surface)
        else:
            fenestration_area = 0
            for item in fenestration:
                try:
                    fenestration_area += item.area
                except:
                    fenestration_area += SurrogateElement(item).area
            area = get_area(surface) - fenestration_area
        constr_name = surface.Construction_Name
        if constr_name in constr_layers:
            layers = constr_layers[constr_name]
            for material in layers:
                # thickness * surface
                mat_in_element = constr_layers[constr_name][material] * area
                if material not in mat_vol:
                    mat_vol[material] = mat_in_element
                else:
                    mat_vol[material] += mat_in_element
        else:
            print(f"Construction '{constr_name}' cannot be found")
    return mat_vol


def extract_surfaces(idf, element_type, boundary=None, surface_type=None):
    """
    Fetches the elements from an IDF file and returns them in a list.
    :param idf: The IDF file
    :param element_type: The element type to be considered, e.g. ['BuildingSurface:Detailed']
    :param boundary: "!- Outside Boundary Condition" as specified in the IDF, e.g. ['Outdoors']
    :param surface_type: "!- Surface Type" as specified in the IDF file, e.g. ['Wall']
    :return: List of eppy elements
    """
    surfaces = []
    for s in idf.idfobjects[element_type.upper()]:
        if element_type not in ['Window', 'Door']:
            if boundary is not None and surface_type is not None:
                if s.Surface_Type not in ('Window', 'Door', 'GlassDoor'):
                    if s.Outside_Boundary_Condition == boundary and s.Surface_Type == surface_type:
                        surfaces.append(s)
                else:
                    if s.Outside_Boundary_Condition_Object == boundary and s.Surface_Type == surface_type:
                        surfaces.append(s)
            else:
                surfaces.append(s)
        else:  # Window and Door objects need special handling
            surfaces.append(SurrogateElement(s))
    return surfaces


def flatten_surfaces(surfaces):
    """
    Just a simple function to flatten the surfaces dictionary created in get_surfaces() and return it as a list.
    :param surfaces: dictionary created by get_surfaces()
    :return: flat list of elements e.g. [BuildingSurface:Detailed,...]
    """
    flat = [[s for s in surfaces[sname]] for sname in surfaces]
    flat = [item for sublist in flat for item in sublist]
    return flat



def get_surfaces(idf):
    """
    A function to derive all surfaces from the IDF file.

    Source: https://unmethours.com/question/15574/how-to-list-and-measure-area-surfaces/?answer=15604#post-id-15604
    NB: The post also explains a method to calculate the external areas by orientation (not implemented here).
    :return: A dictionary for each surface type, e.g. {'ext_wall': [..., ...], 'roof': [...]}
    """
    surfaces = {}
    surfaces_to_count = ['Window', 'BuildingSurface:Detailed', 'Door', 'FenestrationSurface:Detailed']
    # Extracting all surfaces from idf file
    total_no_surfaces = [[s for s in idf.idfobjects[st.upper()]] for st in surfaces_to_count]
    # flatten the list
    total_no_surfaces = [item for sublist in total_no_surfaces for item in sublist]

    surfaces['ext_wall'] = extract_surfaces(idf, 'BuildingSurface:Detailed', 'Outdoors', 'Wall')
    surfaces['int_wall'] = extract_surfaces(idf, 'BuildingSurface:Detailed', 'Surface', 'Wall') + \
                           extract_surfaces(idf, 'BuildingSurface:Detailed', 'Zone', 'Wall') + \
                           extract_surfaces(idf, 'InternalMass')
    surfaces['door'] = extract_surfaces(idf, 'Door') + \
                       extract_surfaces(idf, 'FenestrationSurface:Detailed','', 'Door')
    surfaces['window'] = extract_surfaces(idf, 'Window') + \
                         extract_surfaces(idf, 'FenestrationSurface:Detailed', '', 'Window') + \
                         extract_surfaces(idf, 'FenestrationSurface:Detailed', '', 'GlassDoor')
    surfaces['int_floor'] = extract_surfaces(idf, 'BuildingSurface:Detailed', 'Outdoors', 'Floor') + \
                            extract_surfaces(idf, 'BuildingSurface:Detailed', 'Surface', 'Floor') + \
                            extract_surfaces(idf, 'BuildingSurface:Detailed', 'Zone', 'Floor')
    surfaces['int_ceiling'] = extract_surfaces(idf, 'BuildingSurface:Detailed', 'Surface', 'Ceiling') + \
                              extract_surfaces(idf, 'BuildingSurface:Detailed', 'Adiabatic', 'Ceiling')
    surfaces['basement_ext_wall'] = extract_surfaces(idf, 'BuildingSurface:Detailed', 'GroundBasementPreprocessorAverageWall', 'Wall') + \
                                    extract_surfaces(idf, 'BuildingSurface:Detailed', 'GroundFCfactorMethod', 'Wall')
    surfaces['ext_floor'] = extract_surfaces(idf, 'BuildingSurface:Detailed', 'Ground', 'Floor') + \
                            extract_surfaces(idf, 'BuildingSurface:Detailed', 'GroundSlabPreprocessorAverage', 'Floor') + \
                            extract_surfaces(idf, 'BuildingSurface:Detailed', 'GroundFCfactorMethod', 'Floor')
    # adiabatic boundary condition could be used either for internal or external floors
    if surfaces['ext_floor']:
        surfaces['int_floor'] += extract_surfaces(idf, 'BuildingSurface:Detailed', 'Adiabatic', 'Floor')
    else:
        surfaces['ext_floor'] += extract_surfaces(idf, 'BuildingSurface:Detailed', 'Adiabatic', 'Floor')
    surfaces['ceiling_roof'] = extract_surfaces(idf, 'BuildingSurface:Detailed', 'Zone', 'Ceiling')
    surfaces['roof'] = extract_surfaces(idf, 'BuildingSurface:Detailed', 'Outdoors', 'Roof')
    # Check if any surfaces are present in `total_no_surfaces` but were missed in `surfaces`
    check = [s.Name for s in total_no_surfaces if s.Name not in [n.Name for n in flatten_surfaces(surfaces)]]
    assert len(check) == 0, "Following elements are not accounted for: %s" % check
    return surfaces


def get_surfaces_from_floor_multipliers(idf, surfaces):
    multipliers = {x.Name: int(float(x.Multiplier)) for x in idf.idfobjects["ZONE"] if x.Multiplier != ''}
    for key in surfaces.keys():
        temp_elem = []
        for elem in surfaces[key]:
            if elem.key == "InternalMass":
                zone_name = elem.Zone_or_ZoneList_Name
            elif key in ['door', 'window']:
                surface_name = elem.Building_Surface_Name
                zone_name = [obj.Zone_Name for obj in idf.idfobjects['BuildingSurface:Detailed']
                             if obj.Name == surface_name]
                zone_name = zone_name[0]  # the window should belong to exactly one wall
            else:
                zone_name = elem.Zone_Name

            if zone_name in multipliers.keys():
                temp_elem.extend(np.repeat(elem, multipliers[zone_name] - 1).tolist())
        surfaces[key].extend(temp_elem)
    return surfaces


def get_building_geometry_stats(idf_file, surfaces):
    """
    Sums the surfaces as created by get_surfaces() and returns a corresponding dict.
    :param idf_file:
    :param surfaces:
    :return:
    """
    geom_stats = {}
    for element in surfaces:
        geom_stats[element+'_area'] = sum(get_area(e) for e in surfaces[element])
    geom_stats['ext_wall_area_net'] = geom_stats['ext_wall_area'] - geom_stats['window_area']
    # calculate footprint, assuming a rectangular one based on coordinates of 'ext_floor' surfaces
    x_min, y_min = math.inf, math.inf
    x_max, y_max = -math.inf, -math.inf
    for surface in surfaces['ext_floor']:
        coords = eppy.function_helpers.getcoords(surface)
        for i in range(0, len(coords)):
            if coords[i][0] < x_min:
                x_min = coords[i][0]
            if coords[i][1] < y_min:
                y_min = coords[i][1]
            if coords[i][0] > x_max:
                x_max = coords[i][0]
            if coords[i][1] > y_max:
                y_max = coords[i][1]
    geom_stats['footprint_area'] = (y_max-y_min)*(x_max-x_min)
    geom_stats['footprint_perimeter'] = (y_max-y_min)*2+(x_max-x_min)*2
    zones_with_people = [obj.Zone_or_ZoneList_Name for obj in idf_file.idfobjects['People'.upper()]]
    zones_with_cond = [obj.Zone_Name for obj in idf_file.idfobjects['HVACTemplate:Zone:IdealLoadsAirSystem'.upper()]]
    if not zones_with_cond:
        print('Warning: No zones with IdealLoadsAirSystem found. The conditioned floor area will not be calculated.')
    floor_area_occupied = 0
    floor_area_conditioned = 0
    for surface in surfaces['int_floor']+surfaces['ext_floor']:
        if surface.Zone_Name in zones_with_people:
            floor_area_occupied += get_area(surface)
        if surface.Zone_Name in zones_with_cond:
            floor_area_conditioned += get_area(surface)
    geom_stats['floor_area_occupied'] = floor_area_occupied
    geom_stats['floor_area_conditioned'] = floor_area_conditioned
    geom_stats['total_floor_area'] = geom_stats['ext_floor_area'] + geom_stats['int_floor_area']
    heights = {obj.Name: obj.height for obj in idf_file.idfobjects['BuildingSurface:Detailed'.upper()] if
               obj.Surface_Type == 'Wall'}
    geom_stats['median_floor_height'] = statistics.median(heights.values())
    bld_height = 0
    for surface in surfaces['roof']:
        coords = eppy.function_helpers.getcoords(surface)
        for i in range(0, len(coords)):
            if coords[i][2] > bld_height:
                bld_height = coords[i][2]
    geom_stats['building_height'] = bld_height
    geom_stats['num_of_floors'] = geom_stats['total_floor_area'] / geom_stats['ext_floor_area']
    geom_stats['num_of_floors2'] = geom_stats['building_height'] / geom_stats['median_floor_height']
    return geom_stats


def get_area(e):
    if e.key == "InternalMass":
        area = e.Surface_Area
    else:
        area = e.area
    return area


def get_fenestration_objects_from_surface(idf, surface_obj):
    """
    Finds all fenestration objects assigned to a given surface
    :param idf: The .idf file
    :param surface_obj: Surface object (BuildingSurface:Detailed)
    :return: list of fenestration objects
    """
    surface = surface_obj.Name
    fenestration = []
    for item in ['Window', 'Door', 'FenestrationSurface:Detailed']:
        new = [obj for obj in idf.idfobjects[item] if obj.Building_Surface_Name == surface]
        fenestration.extend(new)
    return fenestration


def add_ground_floor_ffactor_cfactor(constr_layers, obj, replace_dict):
    try:
        res = replace_dict['res']
    except KeyError:
        res = ''
    # get the surrogate construction or create one
    if 'Surrogate_slab-' + res in constr_layers:
        constr_name = 'Surrogate_slab-' + res
        constr_layers[obj.Name] = {key: value for key, value in constr_layers[constr_name].items()}
        constr_layers[obj.Name]['Insulation_surrogate'] = 0.2  # TODO: change? vary with en_std?
    else:
        # Assumptions ground floor: 20 cm concrete, 1% reinforcement and 20 cm insulation.
        constr_layers[obj.Name] = {}
        constr_layers[obj.Name]['Concrete_surrogate'] = 0.2*0.99
        constr_layers[obj.Name]['Reinforcement_surrogate'] = 0.2*0.01
        constr_layers[obj.Name]['Insulation_surrogate'] = 0.2  # TODO: change? vary with en_std?
    return constr_layers


def add_surrogate_basement(mat_mass, geom_stats, height=None, width=None, length=None, distance=None, materials=None,
                           shares=[1], densities=None, room_h=2.8):
    area_slab = geom_stats['footprint_area']
    area_walls = geom_stats['footprint_perimeter'] * room_h
    volume = height * (area_slab+area_walls)
    return convert_volume_to_mass(mat_mass, volume, materials, shares, densities)


def add_surrogate_foundation(mat_mass, geom_stats, height=None, width=None, length=None, distance=None, materials=None,
                             shares=[1], densities=None):
    volume = geom_stats['footprint_area'] * height
    return convert_volume_to_mass(mat_mass, volume, materials, shares, densities)


def convert_volume_to_mass(mat_mass, volume, materials, shares, densities):
    if type(materials) is str:
        materials = [str(i).strip() for i in materials.replace('[', '').replace(']', '').split(',')]
    if type(shares) is str:
        shares = [float(i) for i in shares.replace('[', '').replace(']', '').split(',')]
    elif type(shares) is int or type(shares) is float:
        shares = [shares]
    if type(densities) is str:
        densities = [float(i) for i in densities.replace('[', '').replace(']', '').split(',')]
    else:
        densities = [densities]
    if shares == [0]:  # the cell was empty
        shares = [1]
    if len(materials) != len(shares) != len(densities):
        raise Exception('The lengths of the provided material lists are not consistent')
    if sum(shares) != 1:
        raise Exception('The shares of the provided materials do not sum to 1')
    for i, mat in enumerate(materials):
        if mat not in mat_mass:
            mat_mass[mat] = volume * shares[i] * densities[i]
        else:
            mat_mass[mat] += volume * shares[i] * densities[i]
    return mat_mass


def add_surrogate_columns(mat_mass, geom_stats, height=None, width=None, length=None, distance=None, materials=None,
                          shares=[1], densities=None):
    vol_column = geom_stats['building_height'] * width * length
    try:
        number = geom_stats['footprint_perimeter'] / distance + 1
    except ZeroDivisionError:
        number = 0
    volume = number * vol_column
    return convert_volume_to_mass(mat_mass, volume, materials, shares, densities)


def add_surrogate_beams(mat_mass, geom_stats, height=None, width=None, length=None, distance=None, materials=None,
                        shares=[1], densities=None):
    blg_side_estimate = geom_stats['footprint_perimeter']/4
    vol_beam = blg_side_estimate * width * length
    try:
        number_per_floor = blg_side_estimate / distance + 1
    except ZeroDivisionError:
        number_per_floor = 0
    volume = number_per_floor * vol_beam * geom_stats['num_of_floors']
    return convert_volume_to_mass(mat_mass, volume, materials, shares, densities)


def add_surrogate_studs(mat_mass, geom_stats, height=None, width=None, length=None, distance=None, materials=None,
                        shares=[1], densities=None):
    vol_stud = height * width * length
    try:
        number_studs = (geom_stats['footprint_perimeter'] / distance + 1) * geom_stats['num_of_floors']
    except ZeroDivisionError:
        number_studs = 0
    volume = number_studs * vol_stud
    return convert_volume_to_mass(mat_mass, volume, materials, shares, densities)


def add_surrogate_roof_beams(mat_mass, geom_stats, height=None, width=None, length=None, distance=None,
                             materials=None, shares=[1], densities=None):
    vol_roof_beam = length * width
    blg_side_estimate = geom_stats['footprint_perimeter']/4
    try:
        number_beams = blg_side_estimate / distance + 1
    except ZeroDivisionError:
        number_beams = 0
    volume = vol_roof_beam * blg_side_estimate * number_beams
    return convert_volume_to_mass(mat_mass, volume, materials, shares, densities)


def add_surrogate_shear_walls(mat_mass, geom_stats, height=None, width=None, length=None, distance=None,
                             materials=None, shares=[1], densities=None, shear_wall_ratio=0.02):
    """
    The RT archetype need shear/core walls for lateral load resistance.
    The shear wall ratio is assumed 2% (the footprint of the shear walls to the floor area)
    Based on: https://ascelibrary.org/doi/full/10.1061/(ASCE)ST.1943-541X.0000785
    """
    volume = geom_stats['building_height'] * geom_stats['footprint_area'] * shear_wall_ratio
    return convert_volume_to_mass(mat_mass, volume, materials, shares, densities)


def save_dict_to_csv(dict_in, folder, filename, header=[], units_dict=None):
    """
    Saves a materials dictionary to a csv file.
    :param dict_in: Input dictionary
    :param folder: Path for the file
    :param filename: Filename
    :return: None
    """
    dict_in_copy = {k: v for k,v in dict_in.items()}  # working on the copy not to change the original dict
    if units_dict:
        flag = True
        for k, v in dict_in_copy.items():
            for units_k, units_v in units_dict.items():
                if units_k in k:
                    dict_in_copy[k] = [units_v, v]
                    flag = False
            if flag:
                dict_in_copy[k] = ['', v]
    df = pd.DataFrame.from_dict(dict_in_copy, orient='index')
    df = df.reset_index()
    full_filename = os.path.join(folder, filename)
    df.to_csv(full_filename, header=header, index=False)
    return
