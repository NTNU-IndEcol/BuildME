"""
Functions to convert simple IDFs to ones with infiltration modeled as AirflowNetwork objects

Copyright: Kamila Krych, 2022
Version 1.0
"""
import os
# Make sure that you have selected the correct working directory (BUILDME)
# Standalone Run Requirements
ep_version = '9.2.0'
path_parent = os.path.dirname(os.path.dirname(os.getcwd()))
os.chdir(path_parent)
from BuildME import mmv
from BuildME.idf import read_idf


def convert_to_AFN(idf_path, occ_type, destination_path):
    idf = read_idf(idf_path)
    dictionaries = mmv.create_dictionaries(idf, occ_type)
    xlsx_mmv = './data/mmv-implementation.xlsx'
    idf_afn = mmv.change_archetype_to_AFN(idf, dictionaries, xlsx_mmv)
    path = destination_path + occupation + '-HVAC-with-AFN.idf'
    if os.path.isfile(path) is True:
        os.remove(path)
    idf_afn.saveas(path)


if __name__ == "__main__":
    originalidf_path = "tools\\AFN Converter\\original\\SFH-HVAC.idf"
    occupation = 'SFH'
    savefolder_path = "tools\\AFN Converter\\"

    convert_to_AFN(originalidf_path, occupation, savefolder_path)
