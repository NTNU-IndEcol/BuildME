"""
Functions to manipulate the IDF files.

Copyright: Niko Heeren, 2019
"""

import collections
import os

import pandas as pd
from eppy.modeleditor import IDF

from BuildME import settings
from BuildME.idf import *


def calc_mat_vol_m2(constructions, materials_dict, fallback_mat):
    """
    Calculates the material volume in 1 m2 of a construction
    :param constructions:
    :param materials_dict:
    :param fallback_mat:
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
                thickness = fallback_mat.loc[layers[layer], 'thickness']
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


def save_materials(res_dict, folder, filename='materials.csv'):
    s = pd.Series(res_dict)
    full_filename = os.path.join(folder, filename)
    s.to_csv(full_filename, header=False)


