
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
#simulate.copy_scenario_files(simulation_files)


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
    '''
    idf_f = apply_obj_name_change(idf_f, fnames[fname]['RES'],
                                  '-res-replaceme')
    idf_f = apply_rule_from_excel(idf_f, fnames[fname]['energy_standard'], en_replace)
    idf_f = apply_rule_from_excel(idf_f, fnames[fname]['RES'], res_replace)
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
