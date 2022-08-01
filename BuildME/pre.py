"""
Pre-processing funtions for BuildME.

Copyright: Niko Heeren, 2021
"""
import os

from BuildME import settings
from tqdm import tqdm
from BuildME.idf import read_idf
from BuildME.mmv import change_archetype_to_MMV, create_empty_replace_mmv


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


def create_mmv_variants(comb=settings.combinations):
    """Create MMV variants for the archetypes"""
    # 1 Region
    cool_str = '_auto-MMV'
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
                    # if the archetype MMV file doesn't exist, we create it
                    path = archetype_wt_ext + cool_str + '.idf'
                    if os.path.isfile(path) is False:
                        print("Precalculating the MMV variant of %s archetype..." % occ_type)
                        idf_f = read_idf(archetype_wt_ext + '.idf')
                        idf_mmv = change_archetype_to_MMV(idf_f, occ_type)
                        idf_mmv.saveas(path)
    return


if __name__ == "__main__":
    validate_ep_version()
