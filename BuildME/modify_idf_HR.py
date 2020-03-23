
import collections
import datetime
import multiprocessing as mp
import os
import shutil
import pickle
from time import sleep

import pandas as pd
from tqdm import tqdm

import numpy as np

from BuildME import settings, idf, material, energy, simulate, __version__

'''This scripts modify the .idf file for the high-rise apartment block to be compatible with the BuildME framework'''

#Reading in the file downloaded from DOE, updated to version v.9.0.1
idf_in = idf.read_idf(r'C:\Users\andrenis\Box Sync\Andrea\High-rise\IECC_ApartmentHighRise_STD2006\updated to v.9.0.1\IECC_ApartmentHighRise_STD2006_Chicago_updated_v901.idf')


idf_SFH = idf.read_idf('./data/archetype/USA/SFH.idf')

construction_SFH = [x.Name for x in idf_SFH.idfobjects['CONSTRUCTION']]
construction_in = [x.Name for x in idf_in.idfobjects['CONSTRUCTION']]
build_SFH = [x.Name for x in idf_SFH.idfobjects['BuildingSurface:Detailed']]

build_in = [x.Name for x in idf_in.idfobjects['BuildingSurface:Detailed']]




'''Removing existing windows and using the same windows as available in the SFH and MFH archetype model'''

# Windows that I want to copy into the HR archetype model
windows_to_copy = [x for x in idf_SFH.idfobjects['CONSTRUCTION'] if 'ext-window' in x.Name]

# Windows that can be deleted from the existing HR archetype model
windows_to_delete = [x for x in idf_in.idfobjects['CONSTRUCTION'] if 'Window' in x.Name]

for window in windows_to_delete:
    idf_in.idfobjects['CONSTRUCTION'].remove(window)

for window in windows_to_copy:
    idf_in.copyidfobject(window)

