"""
Pre-processing funtions for BuildME.

Copyright: Niko Heeren, 2021
"""
import os

from BuildME import settings, mmv
from tqdm import tqdm
from BuildME.idf import read_idf


def validate_ep_version(folders=settings.archetypes, crash=True):
    """
    Walks through all archetype files and verify matching energyplus version
    :param folders: Folder with archetype files to check
    :param crash: Raise Error if true and an error is found. Else script will continue.
    """
    # Check if energyplus version matches the one of the binary
    with open(settings.ep_idd, mode='r') as f:
        bin_ver = f.readline().strip().split()[1]  # Extract the version from the IDD file's first line, e.g. '!IDD_Version 9.2.0'

    if bin_ver != settings.ep_version:
        err = "WARNING: energyplus version in settings (%s) does not match implied version (%s) from path (%s)" \
              % (settings.ep_version, bin_ver, settings.ep_idd)
        if crash:
            raise AssertionError(err)
        else:
            print(err)
    # https://stackoverflow.com/a/18394205/2075003
    files = [os.path.join(dp, f) for dp, dn, filenames in
             os.walk(settings.archetypes) for f in
             filenames if os.path.splitext(f)[1] == '.idf']
    for idff in tqdm(files):
        # idf = read_idf(idff)
        with open(idff) as f:
            for line in f:
                if '!- Version Identifier' in line:
                    if settings.ep_version[:-2] not in line:
                        print("WARNING: '%s' has the wrong energyplus version; %s" % (idff, line))
                    # f.close()


def create_mmv_variants(comb=settings.combinations, refresh_excel=True):
    """
    Create MMV variants for the archetypes
    :param comb: a dictionary with the chosen combination of archetypes to be simulated
    :param refresh_excel: a boolean value indicating if the excel sheet replace_mmv.xlsx should be created
    """
    xlsx_mmv = './data/mmv-implementation.xlsx'
    dir_replace_mmv = './data/replace_mmv.xlsx'
    if refresh_excel:
        if os.path.isfile(dir_replace_mmv) is True:
            # delete existing mmv-implementation.xlsx
            os.remove(dir_replace_mmv)
    # 1 Region
    created = []  # List to keep of the created MMV archetypes
    for region in [r for r in comb]:
        # 2 archetype
        for occ_type in comb[region]['occupation']:
            for cool in comb[region]['cooling']:
                if cool == 'MMV':
                    if (region, occ_type) in settings.archetype_proxies:
                        archetype_wt_ext = os.path.join(settings.archetypes,
                                                        settings.archetype_proxies[(region, occ_type)][0],
                                                        settings.archetype_proxies[(region, occ_type)][1])
                    else:
                        archetype_wt_ext = os.path.join(settings.archetypes, region, occ_type)
                    if archetype_wt_ext in created:
                        # Ugly hotfix! Don't need to create the MVV variant twice. However, if proxies are being used,
                        # the MMV variants are being re-created over and over.
                        print("Skipping MMV creation for proxy %s" % os.path.join(region, occ_type))
                        continue
                    idf_f = read_idf(archetype_wt_ext + '.idf')
                    dictionaries = mmv.create_dictionaries(idf_f, occ_type)
                    # if the archetype doesn't have the proper AFN objects, print a message and stop execution #TODO
                    flag = mmv.check_if_mmv_zones(dictionaries)
                    if flag:  # if the archetype can be created
                        path = archetype_wt_ext + '_auto-MMV.idf'
                        print(f"Creating the MMV variant for %s..." % os.path.relpath(path, settings.archetypes))
                        idf_mmv = mmv.change_archetype_to_MMV(idf_f, dictionaries, xlsx_mmv)
                        if os.path.isfile(path) is True:
                            os.remove(path)
                        idf_mmv.saveas(path)
                        if refresh_excel:
                            mmv.create_or_update_excel_replace(occ_type, xlsx_mmv, dictionaries, dir_replace_mmv)
                        created.append(archetype_wt_ext)
                    else:
                        print(f"The MMV variant for {occ_type} cannot be created")
    return


if __name__ == "__main__":
    validate_ep_version()
