
import collections
import datetime
import multiprocessing as mp
import os
import shutil
import pickle
from time import sleep

import pandas as pd
from tqdm import tqdm

from BuildME import settings, idf, material, energy, simulate, __version__

#creating the corresponding .idf file given an energy standard and a resource efficiency strategy and copy file into folder
simulation_files = simulate.create_combinations(settings.testing_combinations)

#deletes exisitng folders that contains simulation results
simulate.nuke_folders(simulation_files) #deletes only the folder with the case you try to simulate

#copy scenarios .idf to the correct folder
simulate.copy_scenario_files(simulation_files)
simulate.calculate_energy()
simulate.calculate_materials()

#res_energy = simulate.collect_energy(simulation_files)
#res_mat = simulate.load_material(simulation_files)

print("Extracting materials and surfaces...")
    if not simulation_files:
        simulation_files = simulate.load_run_data_file(simulate.find_last_run())
    fallback_materials = material.load_material_data()
    tq = tqdm(simulation_files, desc='Initiating...', leave=True)
    for folder in tq:
        tq.set_description(folder)
        run_path = os.path.join(settings.tmp_path, folder)
        idff = material.read_idf(os.path.join(run_path, 'in.idf'))
        materials = material.read_materials(idff)
        materials_dict = material.make_materials_dict(materials)



        densities = material.make_mat_density_dict(materials_dict, fallback_materials)
        constructions = material.read_constructions(idff)
        mat_vol_m2 = material.calc_mat_vol_m2(constructions, materials_dict, fallback_materials)


        #works until here
        '''
        surfaces = material.get_surfaces(idff, simulation_files[folder]['energy_standard'][2],
                                         simulation_files[folder]['RES'][2])
        
        mat_vol_bdg = material.calc_mat_vol_bdg(surfaces, mat_vol_m2)
        total_material_mass = material.calc_mat_mass_bdg(mat_vol_bdg, densities)
        odym_mat = translate_to_odym_mat(total_material_mass)
        surface_areas = material.calc_surface_areas(surfaces)
        # material_intensity = material.calc_material_intensity(total_material_mass, reference_area)
        res = odym_mat
        res['floor_area_wo_basement'] = surface_areas['floor_area_wo_basement']
        res['footprint_area'] = surface_areas['footprint_area']
        loadbeam = add_surrogate_beams(fnames[folder]['RES'][2], res['floor_area_wo_basement'])
        if loadbeam[0] in res:
            res[loadbeam[0]] += loadbeam[1]
        else:
            res[loadbeam[0]] = loadbeam[1]
        if 'RES2.1' in fnames[folder]['RES'][2]:
            postbeam = add_surrogate_beams(fnames[folder]['RES'][2], surface_areas['ext_wall'])
            res[postbeam[0]] += postbeam[1]
        material.save_materials(res, run_path)

surfaces_to_count = ['Window', 'BuildingSurface:Detailed', 'Door']
total_no_surfaces = [[s for s in idf.idfobjects[st.upper()]] for st in surfaces_to_count]


en_replace = pd.read_excel('./data/replace.xlsx', index_col=[0, 1, 2], sheet_name='en-standard')
res_replace = pd.read_excel('./data/replace.xlsx', index_col=[0, 1, 2], sheet_name='RES')
tq = tqdm(simulation_files, leave=True)
for fname in tq:
    # tq.set_description(fname)
    fpath = os.path.join(settings.tmp_path, fname)
    # create folder
    os.makedirs(fpath)

    # copy climate file
    shutil.copy(simulation_files[fname]['climate_file'], os.path.join(fpath, 'in.epw'))

    # copy IDF archetype file
    idf_f = idf.read_idf(simulation_files[fname]['archetype_file'])

    idf_f = simulate.apply_obj_name_change(idf_f, simulation_files[fname]['energy_standard'],
                                  '-en-std-replaceme')
    idf_f.saveas(os.path.join(fpath, 'in.idf'))
    fnames = simulation_files
    idf_f = simulate.apply_obj_name_change(idf_f, fnames[fname]['RES'],
                                  '-res-replaceme')

    #idf_f = simulate.apply_rule_from_excel(idf_f, fnames[fname]['energy_standard'], en_replace)
    #idf_f = simulate.apply_rule_from_excel(idf_f, fnames[fname]['RES'], res_replace)
    idf_f.idfobjects['Building'.upper()][0].Name = fname
    idf_f.saveas(os.path.join(fpath, 'in.idf'))

# save list of all folders
scenarios_filename = os.path.join(settings.tmp_path, datetime.datetime.now().strftime("%y%m%d-%H%M%S") + '.run')
# pd.DataFrame(fnames.keys()).to_csv(scenarios_filename, index=False, header=False)
pickle.dump(fnames, open(scenarios_filename, "wb"))
return scenarios_filename'''

'''
#calculate the materials
simulate.calculate_materials()

#collects the required energy plus files, copy to folder to be able to run the energy plus simulation with the files in the scenario folder
simulate.calculate_energy()


res_mat = simulate.load_material(simulation_files)'''

idf = idff
surfaces = {}
# Different for the HR compared to SFH and MFH
surfaces_to_count = ['FenestrationSurface:Detailed', 'BuildingSurface:Detailed']

# Extracting all surfaces from idf file
surfaces_idf = [[s for s in idf.idfobjects[st.upper()]] for st in surfaces_to_count]
# Flatten list
surfaces_idf = [item for sublist in surfaces_idf for item in sublist]
# Need to account for the zone multiplier
# Finding the multiplier used
list_of_multipliers = [x.Multiplier for x in idf.idfobjects["ZONE"] if x.Multiplier is not '']
# Checking if only one floor is modeled with multiplier, if multiple floors have zone multiplier this can not be handle yet
if list_of_multipliers.count(list_of_multipliers[0]) != len(list_of_multipliers):
    raise Exception('Function can not handle multiple floors with zone multiplier')
else:
    zone_multiplier = list_of_multipliers[0]

# List of surfaces for the middle floor modeled with zone multipliers
surfaces_multiplier = [x for x in surfaces_idf if x.Name.startswith('m')]*zone_multiplier

# Removing all surfaces with multiplier
total_no_surfaces = [x for x in surfaces_idf if not x.Name.startswith('m')]
total_no_surfaces.extend(surfaces_multiplier)



#Need to account for zone multiplier
surfaces['ext_wall'] = extract_surfaces_zone_multiplier(total_no_surfaces, ['BuildingSurface:Detailed'], ['Outdoors'], ['Wall'])
surfaces['int_wall'] = extract_surfaces_zone_multiplier(total_no_surfaces, ['BuildingSurface:Detailed'], ['Surface'], ['Wall'])
surfaces['window'] = extract_surfaces_zone_multiplier(total_no_surfaces, ['FenestrationSurface:Detailed'], [''], ['Window'])
surfaces['int_floor'] = extract_surfaces_zone_multiplier(total_no_surfaces, ['BuildingSurface:Detailed'], ['Adiabatic'], ['Floor']) + \
                            extract_surfaces_zone_multiplier(total_no_surfaces, ['BuildingSurface:Detailed'], ['Surface'], ['Floor'])
surfaces['int_ceiling'] = extract_surfaces_zone_multiplier(total_no_surfaces, ['BuildingSurface:Detailed'], ['Surface'], ['Ceiling']) +\
                            extract_surfaces_zone_multiplier(total_no_surfaces, ['BuildingSurface:Detailed'], ['Adiabatic'], ['Ceiling'])
surfaces['ext_floor'] = extract_surfaces_zone_multiplier(total_no_surfaces, ['BuildingSurface:Detailed'], ['Ground'], ['Floor']) + \
                        extract_surfaces_zone_multiplier(total_no_surfaces, ['BuildingSurface:Detailed'], ['Outdoors'], ['Floor'])
surfaces['roof'] = extract_surfaces_zone_multiplier(total_no_surfaces, ['BuildingSurface:Detailed'], ['Outdoors'], ['Roof'])

# TODO: ADD A CHECK SIMILAR TO BELOW
'''
check = [s.Name for s in total_no_surfaces if s.Name not in [n.Name for n in material.flatten_surfaces(surfaces)]]
assert len(check) == 0, "Following elements were not found: %s" % check'''

# Need to account for the zone multiplier here
temp_surface_areas = material.calc_surface_areas(surfaces)
constr_list = {m.Name: m for m in material.read_constructions(idf)}
# TODO: WHAT TO DO WITH INTERNAL WALLS? SLAB?
# TODO: ok to skip the basement
int_wall_constr = constr_list['attic-ceiling-' + energy_standard].Name
surfaces['int_wall'] = surfaces['int_wall'] +\
                       (create_surrogate_int_walls(temp_surface_areas['floor_area_wo_basement'], int_wall_constr))
slab_constr = constr_list['Surrogate_slab-' + res_scenario].Name
surfaces['slab'] = create_surrogate_slab(temp_surface_areas['footprint_area'], slab_constr)
#surfaces['basement'] = create_surrogate_basement(temp_surface_areas['footprint_area'], slab_constr)
