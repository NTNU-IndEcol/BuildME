"""
Functions to perform the actual simulations.

Copyright: Niko Heeren, 2019
"""
import datetime
import os
import shutil

import pandas as pd
from tqdm import tqdm

from BuildME import idf, material, settings


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
                                                             settings.climate_stations[region][climate_reg]),
                                'archetype_file': os.path.join(settings.archetypes, region, occ_type + '.idf'),
                                # TODO
                                'energy_standard': [region, occ_type, energy_std],
                                'RES': [region, occ_type, res]
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
        print("INFO: './tmp' folder not empty: %s" % ', '.join(remaining_folders))


def apply_energy_standard(archetype_file, energy_standard):
    """
    Replaces the all 'Construction' objects in the IDF with the current energy standard version.
    :param archetype_file:
    :param energy_standard:
    """
    replace_me = '-en-std-replaceme'
    objects = ['Window', 'BuildingSurface:Detailed', 'Door']
    # Load IDF file
    idf_data = idf.read_idf(archetype_file)
    for obj_type in objects:
        for obj in idf_data.idfobjects[obj_type.upper()]:
            if obj.Construction_Name.endswith(replace_me):
                # replace the item
                obj.Construction_Name = obj.Construction_Name.replace(replace_me, '-' + energy_standard[2])
    # idf_data.idfobjects['Building'.upper()][0].Name = '.'.join(energy_standard)
    return idf_data


def apply_RES(idf_f, res, res_rules):
    res_values = res_rules.loc(axis=0)[[res[0]], [res[1]], [res[2]]]
    assert len(res_values) > 0, "Did not find a RES strategy for '%s" % res
    for res_value in res_values.iterrows():
        for idfobj in idf_f.idfobjects[res_value[1]['idfobject'].upper()]:
            setattr(idfobj, res_value[1]['objectfield'], res_value[1]['Value'])
    return idf_f


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
    res_rules = pd.read_excel('./data/RES.xlsx', index_col=[0, 1, 2])
    tq = tqdm(fnames, desc='Initiating...', leave=True)
    for fname in tq:
        tq.set_description(fname)
        fpath = os.path.join(settings.tmp_path, fname)
        # create folder
        os.makedirs(fpath)
        # copy climate file
        shutil.copy(fnames[fname]['climate_file'], fpath)
        # copy IDF archetype file
        idf_f = apply_energy_standard(fnames[fname]['archetype_file'], fnames[fname]['energy_standard'])
        idf_f = apply_RES(idf_f, fnames[fname]['RES'], res_rules)
        idf_f.idfobjects['Building'.upper()][0].Name = fname
        idf_f.saveas(os.path.join(fpath, 'in.idf'))
    # save list of all folders
    scenarios_csv = os.path.join(settings.tmp_path, datetime.datetime.now().strftime("%y%m%d-%H%M%S") + '.run')
    pd.DataFrame(fnames.keys()).to_csv(scenarios_csv, index=False, header=False)
    return scenarios_csv


def load_last_run(path=settings.tmp_path):
    """
    Returns the last scenario combination run as saved in copy_scenario_files().
    :param path: folder to scan
    :return: filename, e.g. '190403-230346.run'
    """
    candidates = [f for f in os.listdir(path) if f.endswith('.run')]
    if len(candidates) == 0:
        raise FileNotFoundError("Couldn't find any .run files in %s" % path)
    fnames = pd.read_csv(os.path.join(path, sorted(candidates)[-1]), header=None)
    return fnames.to_csv(None, header=False, index=False).split('\n')


def calculate_materials(fnames=None):
    if not fnames:
        fnames = load_last_run()
    fallback_materials = material.load_material_data()
    tq = tqdm(fnames, desc='Initiating...', leave=True)
    for folder in tq:
        tq.set_description(folder)
        run_path = os.path.join(settings.tmp_path, folder)
        idff = material.read_idf(os.path.join(run_path, 'in.idf'))
        materials = material.read_materials(idff)
        materials_dict = material.make_materials_dict(materials)
        densities = material.make_mat_density_dict(materials_dict, fallback_materials)
        constructions = material.read_constructions(idff)
        mat_vol_m2 = material.calc_mat_vol_m2(constructions, materials_dict)
        surfaces = material.get_surfaces(idff)
        mat_vol_bdg = material.calc_mat_vol_bdg(surfaces, mat_vol_m2)
        total_material_mass = material.calc_mat_mass_bdg(mat_vol_bdg, densities)
        surface_areas = material.calc_surface_areas(surfaces)
        reference_area = surface_areas['floor_area_wo_basement']
        material_intensity = material.calc_material_intensity(total_material_mass, reference_area)
        material.save_material_intensity(material_intensity, run_path)


def simulate_all(fnames):
    """
    Launches the simulations.
    :return:
    """
    # scenarios = pd.read_csv(scenarios_csv)
    calculate_materials(fnames)
    # calculate_energy()
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

