"""
Settings and constants required for the model to run.

Copyright: Niko Heeren, 2019
"""

import os
import platform
from BuildME import settings_functions

# Path setting
ep_version = '9.2.0'
config_file_version = 'V1.0'
basepath = os.path.abspath('.')
ep_path = os.path.abspath("./bin/EnergyPlus-9-2-0/")
archetypes = os.path.abspath("./data/archetype/")
tmp_path = os.path.abspath("./tmp/")
climate_files_path = os.path.abspath("./data/climate/meteonorm71/")
material_csv_path = os.path.abspath("./data/material.csv")
replace_csv_dir = os.path.abspath("./data/")
config_file = os.path.abspath(os.path.join(basepath, "BuildME_config_" + config_file_version + ".xlsx"))

# Read settings and dictionaries from BuildME_config.xlsx
SimulationConfig, combinations, debug_combinations, archetype_proxies, climate_stations, material_aggregation, \
    atypical_materials, climate_region_weight, surrogate_elements = settings_functions.read_config_file(config_file)

if SimulationConfig['cover version'] != config_file_version:
    raise AssertionError(f'Config version {config_file_version} differs from config version '
                         f'{SimulationConfig["cover version"]} indicated in BuildME_config.xlsx')

# Modelling settings
shielding = SimulationConfig['shielding']  # wind shielding, needed for MMV simulations; set to low, medium or high
cpus = SimulationConfig['cpus']  # Number of CPUs used for energy simulation. 'max' = all. 'auto' = available CPUSs - 1
