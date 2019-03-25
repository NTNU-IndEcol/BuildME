"""
Functions in this file contain the Resource Efficiency strategies to be applied to the archetypes.yp
"""



from . import *
from eppy import modeleditor


def apply_material_substitution(idf, mat, mate_new):
    """
    Replaces a given material in the archetype.
    :param idf: Eppy idf class
    :param mat: Material to be substituted
    :param mate_new: object
    :return:
    """
    pass


def apply_lightweighting():
    pass


def apply_more_intense_use(idf, new_occ, assert_occ=None):
    """
    Applies the RE strategy "More intense use".
    :param idf:
    :param new_occ: New building occupation to apply.
    :param assert_occ: Check if the occupation has an expected value.
    :return:
    """
    if assert_occ is not None:
        pass
    pass


def get_idf(idf_file):
    """Returns the idf file as a eppy class"""
    modeleditor.IDF.setiddname(settings.ep_idd)
    return modeleditor.IDF(idf_file)


def get_dimensions(idf):
    res = {}
    for zone in idf.idfobjects['ZONE']:
        res[zone.Name] = {'zonearea': modeleditor.zonearea(idf, zone.Name)}
        res[zone.Name]['zonearea_floor'] = modeleditor.zonearea_floor(idf, zone.Name)
        res[zone.Name]['zvolume'] = modeleditor.zonevolume(idf, zone.Name)
        # res[zone.Name]['A/V'] = res[zone.Name]['area']/res[zone.Name]['volume']
    return res


def get_matrial_inventory():
    pass

