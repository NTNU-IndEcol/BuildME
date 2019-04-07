"""
Functions to manipulate the IDF files.

Copyright: Niko Heeren, 2019
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


def read_idf(in_file):
    # in_file = os.path.join(filepath, filename)
    idd = settings.ep_idd
    IDF.setiddname(idd)
    with open(in_file, 'r') as infile:
        idf = IDF(infile)
    return idf


def get_surfaces(idf, energy_standard):
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
    temp_surface_areas = calc_surface_areas(surfaces)
    int_wall_constr = {m.Name: m for m in read_constructions(idf)}
    int_wall_constr = int_wall_constr['attic-ceiling-' + energy_standard].Name
    surfaces['int_wall'] = create_surrogate_int_walls(temp_surface_areas['floor_area_wo_basement'], int_wall_constr)
    return surfaces


def create_surrogate_int_walls(floor_area, construction, linear_m=0.4, room_h=2.8):
    """
    Since IDF files sometimes do not contain internal walls, this function will create surrogate internal walls.
    Based on Kellenberger et al. 2012, 0.4 m per 1.0 m2 floor area is assumed. Assuming a room height of 2.8 m,
     this corresponds to  1.12 m2 per 1.0 m2 floor area.
    :return: List of one surface which can be added to the surfaces variable in get_surfaces().
    """
    int_wall = {
        'key': 'DummyBuildingSurface',
        'Name': 'surrogate_int_wall',
        'Building_Surface_Name': None,
        'Construction_Name': construction,
        'area': linear_m * floor_area * room_h
    }
    return [SurrogateElement(int_wall)]


def calc_surface_areas(surfaces, floor_area=['int_floor', 'basement_int_floor']):
    """
    Sums the surfaces as created by get_surfaces() and returns a corresponding dict.
    :param floor_area:
    :param surfaces:
    :return:
    """
    areas = {}
    for element in surfaces:
        areas[element] = sum(e.area for e in surfaces[element])
    areas['ext_wall_area_net'] = areas['ext_wall'] - areas['window']
    areas['floor_area_wo_basement'] = sum([areas[s] for s in areas if s in floor_area])
    areas['footprint_area'] = areas['basement_int_floor']
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




