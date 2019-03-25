"""
Functions to manipulate the IDF files.
"""
import collections
import os

import pandas as pd
from eppy.modeleditor import IDF

from BuildME import settings


class SurrogateElement:
    """
    A surrogate class for windows and doors, because e.g. idf.idfobjects['Window'.upper()] does not contain an 'area'
    attribute. See also https://github.com/santoshphilip/eppy/issues/230.
    """
    def __init__(self, g):
        self.area = g.Length * g.Height
        self.Building_Surface_Name = g.Building_Surface_Name
        self.Construction_Name = g.Construction_Name
        self.key = g.key
        self.Name = g.Name
        # self.Outside_Boundary_Condition = g.Outside_Boundary_Condition
        # self.Zone_Name = g.Zone_Name
        # self.Surface_Type = g.Surface_Type


class SurrogateMaterial:
    # TODO: DELETE?
    """
    A surrogate class for materials, such as, because some material types (e.g. 'Material:NoMass') do not contain
    certain attributes that are later required (e.g. 'Density').
    """
    def __init__(self, g):
        self.key = g.key
        self.Name = g.Name
        self.Density = None


def extract_surfaces(idf, element_type, boundary, surface_type):
    """
    Fetches the elements from an IDF file and returns them in a list.
    :param idf: The IDF file
    :param element_type: The elements to be considered, e.g. ['BuildingSurface:Detailed', 'Window']
    :param boundary: "!- Outside Boundary Condition" as specified in the IDF, e.g. ['Outdoors']
    :param surface_type: "!- Surface Type" as specified in the IDF file, e.g. ['Wall']
    :return: List of eppy elements
    """
    surfaces = []
    for e in element_type:
        for s in idf.idfobjects[e.upper()]:
            if s.Outside_Boundary_Condition in boundary and s.Surface_Type in surface_type:
                surfaces.append(s)
    return surfaces


def extract_windows(idf):
    """
    Need a special function here, because eppy doesn't know the 'Window' object.
    If there are more use cases, this function can also be generlaized.
    :param idf:
    :return:
    """
    glazing = idf.idfobjects['Window'.upper()]
    windows = [SurrogateElement(g) for g in glazing]
    return windows


def extract_doors(idf):
    """
    Need a special function here, because eppy doesn't know the 'Door' object.
    If there are more use cases, this function can also be generlaized.
    :param idf:
    :return:
    """
    doors = idf.idfobjects['Door'.upper()]
    windows = [SurrogateElement(d) for d in doors]
    return windows


def flatten_surfaces(surfaces):
    """
    Just a simple function to flatten the surfaces dictionary created in get_surfaces() and return it as a list.
    :param surfaces: dictionary created by get_surfaces()
    :return: flat list of elements e.g. [BuildingSurface:Detailed,...]
    """
    flat = [[s for s in surfaces[sname]] for sname in surfaces]
    flat = [item for sublist in flat for item in sublist]
    return flat


def read_idf(filepath, filename='in.idf'):
    in_file = os.path.join(filepath, filename)
    idd = settings.ep_idd
    IDF.setiddname(idd)
    with open(in_file, 'r') as infile:
        idf = IDF(infile)
    return idf


def get_surfaces(idf):
    """
    A function to derive all surfaces from the IDF file.
    Source: https://unmethours.com/question/15574/how-to-list-and-measure-area-surfaces/?answer=15604#post-id-15604
    The post also explains a method to calculate the external areas by orientation (not implemented here).
    :return: A dictionary for each surface type, e.g. {'ext_wall': [..., ...], 'roof': [...]}
    """
    surfaces = {}
    surfaces_to_count = ['Window', 'BuildingSurface:Detailed', 'Door']
    total_no_surfaces = [[s for s in idf.idfobjects[st.upper()]] for st in surfaces_to_count]
    # flatten the list
    total_no_surfaces = [item for sublist in total_no_surfaces for item in sublist]
    surfaces['ext_wall'] = extract_surfaces(idf, ['BuildingSurface:Detailed'], ['Outdoors'], ['Wall'])
    surfaces['door'] = extract_doors(idf)
    surfaces['window'] = extract_windows(idf)
    surfaces['int_floor'] = extract_surfaces(idf, ['BuildingSurface:Detailed'], ['Adiabatic'], ['Floor'])
    surfaces['basement_ext_wall'] = extract_surfaces(idf, ['BuildingSurface:Detailed'],
                                                     ['GroundBasementPreprocessorAverageWall'], ['Wall'])
    surfaces['basement_int_floor'] = extract_surfaces(idf, ['BuildingSurface:Detailed'], ['Zone'], ['Floor'])
    surfaces['basement_ext_floor'] = extract_surfaces(idf, ['BuildingSurface:Detailed'],
                                                      ['GroundBasementPreprocessorAverageFloor'], ['Floor'])
    surfaces['ceiling_roof'] = extract_surfaces(idf, ['BuildingSurface:Detailed'], ['Zone'], ['Ceiling'])
    surfaces['roof'] = extract_surfaces(idf, ['BuildingSurface:Detailed'], ['Outdoors'], ['Roof'])
    check = [s.Name for s in total_no_surfaces if s.Name not in [n.Name for n in flatten_surfaces(surfaces)]]
    assert len(check) == 0, "Following elements were not found: %s" % check
    # TODO: Interior walls not defined in idf file
    return surfaces


def calc_surface_areas(surfaces, ref_area=['int_floor', 'basement_int_floor']):
    """
    Sums the surfaces as created by get_surfaces() and returns a corresponding dict.
    :param surfaces:
    :return:
    """
    areas = {}
    for element in surfaces:
        areas[element] = sum(e.area for e in surfaces[element])
    areas['ext_wall_area_net'] = areas['ext_wall'] - areas['window']
    areas['reference_area'] = sum([areas[s] for s in areas if s in ref_area])
    return areas


def calc_envelope(areas):
    """
    Calculates the total envelope surface area in the surfaces variable created by get_surfaces().
    :param areas:
    :return: Dictionary of surface area with and without basement
    """
    envelope = {
        'envelope_w_basement': sum(areas[s] for s in ['ext_wall', 'roof', 'basement_ext_floor']),
        'envelope_wo_basement': areas['envelope_w_basement'] + areas['basement_ext_wall']}
    return envelope


def read_materials(idf):
    materials = []
    for mtype in ['Material', 'Material:NoMass', 'Material:AirGap',
                  'WindowMaterial:SimpleGlazingSystem', 'WindowMaterial:Blind',
                  'WindowMaterial:Glazing']:
        materials = materials + [i for i in idf.idfobjects[mtype.upper()]]
    find_duplicates(materials)
    # TODO: Will need to think about windows...
    return materials


def load_material_data():
    filedata = pd.read_excel('data/material.xlsx', sheet_name='properties', index_col='ep_name')
    return filedata


def find_duplicates(idf_object, crash=True):
    """
    Checks if duplicate entries in an IDF object exist
    :param crash:
    :param idf_object:
    :return: None
    """
    object_names = [io.Name for io in idf_object]
    duplicates = [item for item, count in collections.Counter(object_names).items() if count > 1]
    if crash:
        assert len(duplicates) == 0, "Duplicate entries for IDF object: '%s'" % duplicates
    else:
        return duplicates


def make_materials_dict(materials):
    """
    Takes the eppy materials objects and places them into a dictionary with the .Name attribute as the key,
    e.g. {material.Name: material}
    :param materials: list of eppy idf objects as created by read_materials()
    :return: dictionary with the .Name attribute as the key {material.Name: material}
    """
    # Making sure there are no duplicate Material entries in the IDF file
    materials_dict = {m.Name: m for m in materials}
    return materials_dict


def make_mat_density_dict(materials_dict, fallback_mat):
    """
    Creates a dictionary of material densities by material.
    TODO: Not sure if this can be derived from the IDF file only.
    :return:
    """
    densities = {}
    for mat in materials_dict:
        # Some materials, such as Material:No Mass have no density attribute
        if hasattr(materials_dict[mat], 'Density'):
            densities[mat] = materials_dict[mat].Density
        else:
            # print(mat, materials_dict[mat].key)
            densities[mat] = fallback_mat.loc[mat, 'density']
    return densities


def read_constructions(idf):
    """
    Gets the "Construction" elements from the idf files.
    :param idf:
    :return:
    """
    constructions = idf.idfobjects['Construction'.upper()]
    find_duplicates(constructions)
    return constructions


def extract_layers(construction):
    res = {}
    layers = ['Outside_Layer'] + ['Layer_'+str(i+2) for i in range(9)]
    for l in layers:
        if getattr(construction, l) == '':
            break  # first empty value found
        res[l] = getattr(construction, l)
    return res


def calc_mat_vol_m2(constructions, materials_dict):
    """
    Calculates the material volume in 1 m2 of a construction
    :param constructions:
    :param materials_dict:
    :return: {'construction_name': {}
    """
    res = {}
    for construction in constructions:
        res[construction.Name] = {}
        layers = extract_layers(construction)
        for layer in layers:
            if hasattr(materials_dict[layers[layer]], 'Thickness'):
                # This only works as long as we ignore glass!
                # WindowMaterial:SimpleGlazingSystem does not have a Thickness attribute
                thickness = materials_dict[layers[layer]].Thickness
            else:
                thickness = 0
            if layer not in res[construction.Name]:
                res[construction.Name][layers[layer]] = thickness
            else:
                res[construction.Name][layers[layer]] += thickness
    return res


def calc_mat_vol_bdg(surfaces, mat_m2):
    """
    Calculate building's total material intensity.
    :param surfaces:
    :param mat_m2:
    :return: Dictionary with material and volume
    """
    mat_vol = {}
    flat_surfaces = flatten_surfaces(surfaces)
    for surface in flat_surfaces:
        for material in mat_m2[surface.Construction_Name]:
            # thickness * surface
            mat_in_element = mat_m2[surface.Construction_Name][material] * surface.area
            if material not in mat_vol:
                mat_vol[material] = mat_in_element
            else:
                mat_vol[material] += mat_in_element
    return mat_vol


def calc_mat_mass_bdg(mat_vol_bdg, densities):
    """
    Calculate total material mass of the building by converting colume to mass. That means multiplying material volumes
    from calc_mat_vol_bdg() times their density.
    :param mat_vol_bdg: Dictionary of total material volume by material as returned by calc_mat_vol_bdg()
    :param densities: Dictionary of material density
    :return: Dictionary with material and mass
    """
    return {mat: mat_vol_bdg[mat] * densities[mat] for mat in mat_vol_bdg}


def calc_material_intensity(total_material, reference_area):
    """
    Calculate material intensity per reference area.
    **Reference area can be either floor area or building footprint area.**
    :param total_material:
    :param reference_area:
    :return:
    """
    return {mat: total_material[mat] / reference_area for mat in total_material}




