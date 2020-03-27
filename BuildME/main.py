
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
simulation_files = simulate.create_combinations()

#deletes exisitng folders that contains simulation results
simulate.nuke_folders(simulation_files) #deletes only the folder with the case you try to simulate

#copy scenarios .idf to the correct folder
simulate.copy_scenario_files(simulate.create_combinations())

#calculate the materials
simulate.calculate_materials()

#collects the required energy plus files, copy to folder to be able to run the energy plus simulation with the files in the scenario folder
simulate.calculate_energy()


res_mat = simulate.load_material(simulation_files)
res_energy = simulate.collect_energy(simulation_files)