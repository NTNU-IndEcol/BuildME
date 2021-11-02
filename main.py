
import pandas as pd
import numpy as np
from tqdm import tqdm
import encodings

from BuildME import settings, pre, idf, material, energy, simulate, __version__

# Some pre-processing
pre.validate_ep_version()

# Creating the corresponding .idf file given an energy standard and a resource efficiency strategy
#  and copy file into folder
simulation_files, run = simulate.create_combinations(settings.debug_combinations)

#deletes exisitng folders that contains simulation results
# simulate.nuke_folders(simulation_files)  # deletes only the folder with the case you try to simulate

# Copy scenarios .idf to the correct folder
simulate.copy_scenario_files(simulation_files, run)
# Create run file
# simulate.create_sq_job(simulation_files)

simulate.calculate_energy()
simulate.calculate_materials(run, simulation_files)

res_energy = simulate.collect_energy(simulation_files)
res_mat = simulate.load_material(simulation_files)


simulate.save_ei_result(run, res_energy, res_mat)
simulate.save_mi_result(run, res_mat)