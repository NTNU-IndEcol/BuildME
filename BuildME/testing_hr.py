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

