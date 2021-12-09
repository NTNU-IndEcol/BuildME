"""
Pre-processing funtions for BuildME.

Copyright: Niko Heeren, 2021
"""
import os

from BuildME import settings
from tqdm import tqdm
from BuildME.idf import read_idf
from BuildME.mmv import change_archetype_to_MMV


def validate_ep_version(folders=settings.archetypes,crash=False):
    """
    Walks through all archetype files and verify matching energyplus version
    :param folders: Folder with archetype files to check
    :param crash: Raise Error if true and an error is found. Else script will continue.
    :return:
    """
    # Check if energyplus version matches the one of the binary
    # Fragile function assuming the version is separated by '-'
    bin_ver = settings.ep_path.split('-')[-3:]
    if '.'.join(bin_ver) != settings.ep_version:
        err = "WARNING: energyplus version in settings (%s) does not match implied version (%s) from path (%s)" \
              % (settings.ep_version, '.'.join(bin_ver), settings.ep_path)
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
                        print("Precalculating the MMV variant of %s archetype of the %s region..." %(occ_type, region))
                        idf_f = read_idf(archetype_wt_ext + '.idf')
                        idf_mmv = change_archetype_to_MMV(idf_f, region, occ_type)
                        idf_mmv.saveas(path)
    return


if __name__ == "__main__":
    validate_ep_version()
