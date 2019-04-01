"""
Functions to perform the actual simulations.

Copyright: Niko Heeren, 2019
"""

import os
import shutil

from BuildME import settings


def create_combinations(comb=settings.combinations):
    """
    Creates permutations of files to be simulated / calculated.
    The foldernames are coded as follows and separated by underscores: World Region, Occupation archetype,
    energy standard, Resource Efficiency Strategy RES, climate region, and climate scenario.
    An example for the USA, single-family home, standard energy efficiency, no RES, in US climate region 1A,
    and with the climate scenario of 2015 (i.e. none): US_SFH_standard_RES0_cr1A_2015
    :return:
    """
    fnames = {}
    # 1 Region
    for region in [r for r in comb if r != 'all']:
        # 2 archetype
        for occ_type in comb[region]['occupation']:
            # 3 energy standard
            for energy_std in comb[region]['energy standard']:
                # 'informal' type only has 'non-standard' -- skip other combinations
                if occ_type == 'informal' and energy_std in ['standard', 'efficient', 'ZEB']:
                    continue
                # 4 Resource Efficiency Strategy
                for res in comb[region]['RES']:
                    # 5 Climate region
                    for climate_reg in comb[region]['climate_region']:
                        # 6 Climate scenario
                        for climate_scen in comb[region]['climate_scenario']:
                            fnames['_'.join([region, occ_type, energy_std,
                                             occ_type, res, climate_reg, climate_scen])] = \
                                {
                                'climate_file': os.path.join(settings.climate_files_path, climate_scen,
                                                             settings.climate_stations[region][climate_reg])
                                'archetype_file': os.path.join(settings.archetypes, region, occ_type)
                                }
                            # make sure no underscores are used in the pathname, because this could cause issues later
                            assert list(fnames)[-1].count('_') == 6, \
                                "Scenario combination names mustn't use underscores: '%s'" % fnames[-1]
    return fnames


def nuke_folders(fnames, forgive=True):
    """
    Deletes all folders specified in the `fnames` variable.
    :param forgive: will continue also if certain folder's don't exist
    :param fnames: List of foldernames as created by create_combinations()
    :return:
    """
    for fname in fnames:
        fpath = os.path.join(settings.tmp_path, fname)
        if not os.path.exists(fpath) and forgive:
            continue
        shutil.rmtree(fpath)
    remaining_folders = [x[0] for x in os.walk(settings.tmp_path)][1:]
    if len(remaining_folders) > 0:
        print("INFO: 'tmp' folder not empty: %s" % ', '.join(remaining_folders))


def copy_scenario_files(fnames, replace=False):
    """
    Creates scenario folders and copies the necessary files (climate and IDF file) into them. Further,
    it applies the energy standard and RES scenario to the IDF archetype.
    :param replace:
    :type fnames: List of combinations / foldernames as created by create_combinations()
    :return:
    """
    if replace:
        nuke_folders(fnames)
    for fname in fnames:
        fpath = os.path.join(settings.tmp_path, fname)
        # create folder
        os.makedirs(fpath)
        # copy climate file
        shutil.copy(fnames[fname]['climate_file'], fpath)
        # copy IDF archetype file
        shutil.copy(fnames[fname]['IDF'], fpath)
        # TODO: Apply energy-standard to archetype
        # TODO: Apply RES to archetype


def simulate_all():
    """
    Launches the simulations.
    :return:
    """
    pass


def collect_results():
    """
    Collects the results after the simulation.
    :return:
    """
    pass


def cleanup():
    """
    Cleanes up temporary folders and files.
    :return:
    """
    pass


def create_result_table():
    """
    Arragnes the results into a nice table for further aggregation.
    :return:
    """
    pass


def create_odym_input():
    """
    Aggregates the result table into the ODYM format.
    :return:
    """
    pass

