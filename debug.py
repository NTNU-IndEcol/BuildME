from BuildME.climate import *
from BuildME.energy import *
import os


tmp = 'test0001'
copy_us = gather_files_to_copy('USA/SFH_base.idf', '2015/Chicago_IL-hour.epw')
# copy_files(copy_us, tmp)
run_energyplus_single(tmp)
# delete_temp_folder(tmp, verbose=True)

