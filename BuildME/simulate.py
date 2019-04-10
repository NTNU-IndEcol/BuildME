"""
Functions to perform the actual simulations.

Copyright: Niko Heeren, 2019
"""
import collections
import datetime
import multiprocessing as mp
import os
import shutil
import pickle
from time import sleep

import pandas as pd
from tqdm import tqdm

from BuildME import settings, idf, material, energy


def create_combinations(comb=settings.combinations):
    """
    Creates permutations of files to be simulated / calculated.
    The foldernames are coded as follows and separated by underscores: World Region, Occupation archetype,
    energy standard, Resource Efficiency Strategy RES, climate region, and climate scenario.
    An example for the USA, single-family home, standard energy efficiency, no RES, in US climate region 1A,
    and with the climate scenario of 2015 (i.e. none): US_SFH_standard_RES0_cr1A_2015
    :return:
    """
    print("Creating scenario combinations")
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
                            fname = '_'.join([region, occ_type, energy_std, res, climate_reg, climate_scen])
                            fnames[fname] = \
                                {
                                'climate_file': os.path.join(settings.climate_files_path, climate_scen,
                                                             settings.climate_stations[region][climate_reg]),
                                'archetype_file': os.path.join(settings.archetypes, region, occ_type + '.idf'),
                                # TODO
                                'energy_standard': [region, occ_type, energy_std],
                                'RES': [region, occ_type, res],
                                'run_folder': os.path.join(settings.tmp_path, fname)
                                }
                            # make sure no underscores are used in the pathname, because this could cause issues later
                            assert list(fnames)[-1].count('_') == 5, \
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
        print("Deleting files...")
        nuke_folders(fnames)
    print("Copying files...")
    res_rules = pd.read_excel('./data/RES.xlsx', index_col=[0, 1, 2])
    tq = tqdm(fnames, desc='Initiating...', leave=True)
    for fname in tq:
        tq.set_description(fname)
        fpath = os.path.join(settings.tmp_path, fname)
        # create folder
        os.makedirs(fpath)
        # copy climate file
        shutil.copy(fnames[fname]['climate_file'], os.path.join(fpath, 'in.epw'))
        # copy IDF archetype file
        idf_f = apply_energy_standard(fnames[fname]['archetype_file'], fnames[fname]['energy_standard'])
        idf_f = apply_RES(idf_f, fnames[fname]['RES'], res_rules)
        idf_f.idfobjects['Building'.upper()][0].Name = fname
        idf_f.saveas(os.path.join(fpath, 'in.idf'))
    # save list of all folders
    scenarios_filename = os.path.join(settings.tmp_path, datetime.datetime.now().strftime("%y%m%d-%H%M%S") + '.run')
    # pd.DataFrame(fnames.keys()).to_csv(scenarios_filename, index=False, header=False)
    pickle.dump(fnames, open(scenarios_filename, "wb"))
    return scenarios_filename


def find_last_run(path=settings.tmp_path):
    """
    Returns the last scenario combination run as saved in copy_scenario_files().
    :param path: folder to scan
    :return: filename, e.g. '190403-230346.run'
    """
    candidates = [f for f in os.listdir(path) if f.endswith('.run')]
    if len(candidates) == 0:
        raise FileNotFoundError("Couldn't find any .run files in %s" % path)
    return os.path.join(path, sorted(candidates)[-1])


def load_run_data_file(filename):
    """
    Returns the last scenario combination run as saved in copy_scenario_files().
    :param filename: Absolute filename
    :return: filename, e.g. '190403-230346.run'
    """
    return pickle.load(open(filename, 'rb'))


def calculate_materials(fnames=None):
    print("Extracting materials and surfaces...")
    if not fnames:
        fnames = load_run_data_file(find_last_run())
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
        mat_vol_m2 = material.calc_mat_vol_m2(constructions, materials_dict, fallback_materials)
        surfaces = material.get_surfaces(idff, fnames[folder]['energy_standard'][2])
        mat_vol_bdg = material.calc_mat_vol_bdg(surfaces, mat_vol_m2)
        total_material_mass = material.calc_mat_mass_bdg(mat_vol_bdg, densities)
        surface_areas = material.calc_surface_areas(surfaces)
        # material_intensity = material.calc_material_intensity(total_material_mass, reference_area)
        res = total_material_mass
        res['floor_area_wo_basement'] = surface_areas['floor_area_wo_basement']
        res['footprint_area'] = surface_areas['footprint_area']
        material.save_materials(res, run_path)


def calculate_energy(fnames=None):
    print("Perform energy simulation...")
    if not fnames:
        fnames = load_run_data_file(find_last_run())
    tq = tqdm(fnames, desc='Initiating...', leave=True)
    for folder in tq:
        run_path = os.path.join(settings.tmp_path, folder)
        tq.set_description(folder)
        copy_us = energy.gather_files_to_copy()
        # TODO: Change Building !- Name
        tmp = energy.copy_files(copy_us, tmp_run_path=folder, create_dir=False)
        energy.run_energyplus_single(tmp)
        energy.delete_ep_files(copy_us, tmp)


def calculate_energy_mp(fnames=None, cpus=mp.cpu_count()-1):
    print("Perform energy simulation...")
    if not fnames:
        fnames = load_run_data_file(find_last_run())
    pool = mp.Pool(processes=cpus)
    m = mp.Manager()
    q = m.Queue()
    pbar = tqdm(total=len(fnames), smoothing=0.1)
    args = ((folder, q, no) for no, folder in enumerate(fnames))
    result = pool.map_async(calculate_energy_worker, args)
    old_q = 0
    while not result.ready():
        #pbar.update()
        #print(q.qsize())
        if q.qsize() > old_q:
            pbar.update(q.qsize() - old_q)
        old_q = q.qsize()
        sleep(0.2)
    pool.close()
    pool.join()
    pbar.close()
    result_output = result.get()


def calculate_energy_worker(args):
    folder, q, no = args
    run_path = os.path.join(settings.tmp_path, folder)
    # sleep(1.5)
    copy_us = energy.gather_files_to_copy()
    tmp = energy.copy_files(copy_us, tmp_run_path=folder, create_dir=False)
    energy.run_energyplus_single(tmp)
    energy.delete_ep_files(copy_us, tmp)
    q.put(no)


def simulate_all(fnames):
    """
    Launches the simulations.
    :return:
    """
    # scenarios = pd.read_csv(scenarios_csv)
    calculate_materials(fnames)
    # calculate_energy()
    pass


def collect_logs(fnames, logfile='eplusout.err'):
    """
    Goes through all folders and extracts the last line of the energyplus log file to make sure the simulation was successful.
    :param fnames:
    :param logfile:
    :return:
    """
    print('Collecting E+ logs...')
    res = {}
    for folder in tqdm(fnames):
        res[folder] = {}
        file = os.path.join(fnames[folder]['run_folder'], logfile)
        with open(file, "rb") as f:
            # https://stackoverflow.com/a/18603065/2075003
            # first = f.readline()  # Read the first line.
            f.seek(-2, os.SEEK_END)  # Jump to the second last byte.
            while f.read(1) != b"\n":  # Until EOL is found...
                f.seek(-2, os.SEEK_CUR)  # ...jump back the read byte plus one more.
            last = f.readline()  # Read last line.
            res_string = last.decode("utf-8")
            for repl in [('*', ''), ('  ', ''), ('\n', '')]:
                res_string = res_string.replace(*repl)
            res[folder]['ep_log'] = res_string
    return res


def collect_material(fnames):
    print('Collecting Material results...')
    res = {}
    for folder in tqdm(fnames):
        df = pd.read_csv(os.path.join(fnames[folder]['run_folder'], 'materials.csv'), header=None)
        res[folder] = {d[1][0]: d[1][1] for d in df.iterrows()}
        res[folder]['total_mat'] = df.sum(axis=0)[1]
    return res


def collect_energy(fnames):
    print('Collecting Energy results...')
    res = {}
    for folder in tqdm(fnames):
        energy_res = energy.ep_result_collector(os.path.join(fnames[folder]['run_folder']))
        res[folder] = energy_res.to_dict()
    return res


def disaggregate_scenario_str(in_dict, unstack_cols):
    """
    Converting scenario titles, separated by underscores, into columns.
    Also re-arranging dataframe.
    :param in_dict:
    :param unstack_cols:
    :return:
    """
    res = pd.DataFrame.from_dict(in_dict, orient='index')
    res.index = pd.MultiIndex.from_tuples(tuple(res.index.str.split('_')))
    res.index.names = ['region', 'occupation', 'energy_std', 'RES', 'climate_reg', 'IPCC_scen']
    res = res.unstack(unstack_cols)
    return res


def weighing_climate_region(res):
    """
    Multiplies each result by its climate region ratio given in aggregate.xlsx.
    :param res:
    :return:
    """
    weights = pd.read_excel('./data/aggregate.xlsx', sheet_name='climate_reg', index_col=[0, 1])
    # making sure index is all strings
    weights.index = pd.MultiIndex.from_tuples([(ix[0], str(ix[1])) for ix in weights.index.tolist()])
    # I know looping DFs is lame, but who can figure out this fricking syntax?!
    #  https://stackoverflow.com/a/41494810/2075003
    for region in res.index.levels[0]:
        for cr in res.loc[region].columns.levels[1]:
            res.loc[pd.IndexSlice[region, :, :], pd.IndexSlice[:, cr]] = \
                res.loc[pd.IndexSlice[region, :, :], pd.IndexSlice[:, cr]] * \
                weights.loc[pd.IndexSlice[region, cr], 'share']
    return res


def weighing_energy_carrier(ei_result):
    energy_dict = {'Cooling': 'Cooling:EnergyTransfer [J](Hourly)',
                   'Heating': 'Heating:EnergyTransfer [J](Hourly)'}
    weights = pd.read_excel('./data/aggregate.xlsx', sheet_name='energy_carrier', index_col=[0])
    ei_result.index = ei_result.index.droplevel(4)
    # Can't believe there is no easier way... https://stackoverflow.com/a/42612344/2075003
    df = pd.DataFrame(data=0.0, index=ei_result.index, columns=['Heating', 'Cooling', 'DHW']).stack()
    df = pd.DataFrame(data=0.0, index=df.index, columns=weights.columns).stack()
    df.index.names = ei_result.index.names + ['ServiceType', 'energy_carrier']
    for i, s in df.iteritems():
        if i[4] == 'Heating':
            df[i] = ei_result.loc[i[:-2], [energy_dict[i[4]]]].sum() * \
                    weights.loc[i[0], i[-1]]
        elif i[4] == 'DHW':  # TODO: Not implemented yet
            df[i] = 0.0
        else:
            if i[5] == 'electricity':
                df[i] = ei_result.loc[i[:-2], [energy_dict[i[4]]]].sum() * \
                        1.0
            else:
                df[i] = 0.0
    return df


def divide_by_area(energy, material_surfaces, ref_area='floor_area_wo_basement'):
    res = {}
    for scenario in energy:
        res[scenario] = {}
        area = material_surfaces[scenario][ref_area]
        for e in energy[scenario]:
            res[scenario][e] = energy[scenario][e] / area / 10**6
    return res


def save_ei_result(energy, material_surfaces, ref_area='floor_area_wo_basement'):
    """

    :param res:
    :param ref_area:
    :return:
    """
    res = divide_by_area(energy, material_surfaces, ref_area)
    res = disaggregate_scenario_str(res, ['climate_reg'])
    res = weighing_climate_region(res)
    writer = pd.ExcelWriter(find_last_run().replace('.run', '_ei.xlsx'),
                            engine='xlsxwriter')
    res.to_excel(writer, 'all')
    res['Heating:EnergyTransfer [J](Hourly)'].sum(axis=1).to_excel(writer, 'heat')
    res['Cooling:EnergyTransfer [J](Hourly)'].sum(axis=1).to_excel(writer, 'cool')
    res['InteriorLights:Electricity [J](Hourly)'].sum(axis=1).to_excel(writer, 'light')
    res['InteriorEquipment:Electricity [J](Hourly) '].sum(axis=1).to_excel(writer, 'equip')
    (res['InteriorEquipment:Electricity [J](Hourly) '].sum(axis=1) +
     res['InteriorLights:Electricity [J](Hourly)'].sum(axis=1)).to_excel(writer, 'elec_total')
    res.sum(axis=1).to_excel(writer, 'total')
    writer.save()
    return res


def save_ei_for_odym(ei_result):
    res = weighing_energy_carrier(ei_result)
    new_idx_names = ['Products', 'Use_Phase_i4', 'RES', 'Service', 'SSP_Regions_32', 'Energy carrier']
    new_idx = [tuple(['_'.join((i[1], i[2]))] + ['Energy Intensity UsePhase'] + [i[n] for n in (3, 4, 0, 5)])
               for i in res.index.values]
    res.index = pd.MultiIndex.from_tuples(new_idx, names=new_idx_names)
    res = pd.DataFrame(res, columns=['Value'])
    res['Unit'] = 'MJ/m2/yr'
    res['Stats_array_string'] = ''
    res['Comment'] = 'Simulated in BME v0.0'
    # some more stuff?
    res.to_excel(find_last_run().replace('.run', '_ODYM_ei.xlsx'), merge_cells=False)


def save_all_result_csv(res):
    res.to_csv(find_last_run().replace('.run', '_totals.csv'))


def calculate_measures(res):
    """
    Adds further metrics to the results collected in all_results_collector(), such as material and energy intensity,
    i.e. material / energy per floor area.
    :param res: Dataframe created by all_results_collector()
    :return: Dataframe with additional columns
    """
    return res


def all_results_collector(fnames):
    """
    Collects the results after the simulation.
    :return: Dictionary with scenario as key and material intensity, energy intensity, and e+ log file, e.g.
                {'USA_SFH_ZEB_RES0_1A_2015': {Asphalt_shingle: 4.2, ...}}
    """
    ep_logs = collect_logs(fnames)
    material_res = collect_material(fnames)
    energy_res = collect_energy(fnames)
    res = {}
    for f in ep_logs:
        res[f] = {**material_res[f], **energy_res[f], **ep_logs[f]}
    res = pd.DataFrame.from_dict(res, orient='index')
    res.index.names = ['scenario']
    res = calculate_measures(res)
    save_all_result_csv(res)
    ei_result = save_ei_result(energy_res, material_res)
    save_ei_for_odym(ei_result)
    mi_result = save_mi_result(material_res)
    # TODO save_mi_result_csv(energy_res, material_res)
    return res


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

