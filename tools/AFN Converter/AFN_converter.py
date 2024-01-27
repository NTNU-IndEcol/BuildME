"""
Functions to convert simple IDFs to ones with infiltration modeled as AirflowNetwork objects

Copyright: Kamila Krych, 2022
Version 1.0
"""
import os
import sys
# Make sure that you have selected the correct working directory (BUILDME)
# Standalone Run Requirements
ep_version = '9.2.0'
if os.path.basename(os.getcwd()) != 'BuildME':
    os.chdir('../..')
sys.path.append(os.getcwd()) 
from BuildME import mmv, settings
from BuildME.simulate import read_idf


def convert_to_AFN(idf_path, occ_type, destination_path, refresh_excel=False):
    idf = read_idf(settings.ep_path, idf_path)
    dictionaries = mmv.create_dictionaries(idf, occ_type)
    xlsx_mmv = './data/afn-mmv-implementation.xlsx'
    idf_afn = mmv.change_archetype_to_AFN(idf, dictionaries, xlsx_mmv)
    path = destination_path + occ_type + '-HVAC-with-AFN.idf'
    if os.path.isfile(path) is True:
        os.remove(path)
    idf_afn.saveas(path)
    # create or update excel file with replace instructions
    dir_replace_mmv = destination_path + 'replace_mmv.xlsx'
    if refresh_excel:
        if os.path.isfile(dir_replace_mmv) is True:
            # delete existing replace_mmv.xlsx
            os.remove(dir_replace_mmv)
    mmv.create_or_update_excel_replace(occ_type, xlsx_mmv, dictionaries, dir_replace_mmv)


if __name__ == "__main__":
    for occupation in ['RT', 'MFH', 'SFH', 'HotelLarge', 'OfficeMedium', 'SchoolPrimary', 'SchoolSecondary',
                            'RetailStripmall', 'RetailStandalone']:
        print(f'Converting {occupation} archetype to the AFN variant...')
        originalidf_path = "tools\\AFN Converter\\original\\" + occupation + "-HVAC.idf"
        savefolder_path = "tools\\AFN Converter\\"

        convert_to_AFN(originalidf_path, occupation, savefolder_path)
