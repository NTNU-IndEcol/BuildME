"""
Settings and constants required for the model to run.

Copyright: Niko Heeren, 2019
"""

import os
import platform
import logging


logger = logging.getLogger(__name__)

# Path setting
ep_version = '9.2.0'
basepath = os.path.abspath('.')
ep_path = os.path.abspath("./bin/EnergyPlus-9-2-0/")
ep_idd = os.path.abspath(os.path.join(ep_path, "Energy+.idd"))
archetypes = os.path.abspath("./data/archetype/")
tmp_path = os.path.abspath("./tmp/")
climate_files_path = os.path.abspath("./data/climate/meteonorm71/")

# Checking OS and define files to copy to the temporary folders
platform = platform.system()
if platform == 'Windows':
    ep_exec_files = ["energyplus.exe", "Energy+.idd", "EPMacro.exe", "ExpandObjects.exe",
                     "PreProcess/GrndTempCalc/Basement.exe", "PreProcess/GrndTempCalc/BasementGHT.idd",
                     "PreProcess/GrndTempCalc/Slab.exe", "PreProcess/GrndTempCalc/SlabGHT.idd",
                     "PostProcess/ReadVarsESO.exe", "energyplusapi.dll"
                     ]
elif platform == 'Darwin':
    ep_exec_files = ["energyplus", "energyplus-%s" % ep_version, "Energy+.idd", "EPMacro", "ExpandObjects",
                     "libenergyplusapi.%s.dylib" % ep_version,  # required by energyplus
                     "libgfortran.5.dylib", "libquadmath.0.dylib", 'libgcc_s.1.dylib',  # required by ExpandObjects
                     "PreProcess/GrndTempCalc/Basement", "PreProcess/GrndTempCalc/BasementGHT.idd",
                     "PreProcess/GrndTempCalc/Slab", "PreProcess/GrndTempCalc/SlabGHT.idd",
                     "PostProcess/ReadVarsESO"
                     ]
else:
    raise NotImplementedError('OS is not supported! %s' % platform)

# Modelling settings
shielding = 'medium'  # wind shielding, needed for MMV simulations; set to low, medium or high

# Combination settings
#  Define the combinations to be created, e.g. USA.SFH_standard.RES0

debug_combinations = {
    'USA':
        {'occupation': ['MFH'],
         'energy standard': ['standard'],
         'RES': ['RES0'],
         'climate_region': ['1A'],
         'climate_scenario': ['2015'],
         'cooling': ['HVAC']},
    'IT':
        {'occupation': ['RT', 'MFH', 'SFH'],
         'energy standard': ['non-standard', 'standard', 'efficient', 'ZEB'],
         'RES': ['RES0', 'RES2.1', 'RES2.2', 'RES2.1+RES2.2'],
         'climate_region':
             ['Italy'],
         'climate_scenario': ['2015'],
         'cooling': ['HVAC', 'MMV']
         }
}

combinations = \
    {
        'USA':
            {'occupation': ['RT', 'MFH', 'SFH'],
             'energy standard': ['non-standard', 'standard', 'efficient', 'ZEB'],
             'RES': ['RES0', 'RES2.1', 'RES2.2', 'RES2.1+RES2.2'],
             'climate_region':
                 ['1A', '2A', '2B', '3A', '3B-Coast', '3B', '3C',
                  '4A', '4B', '4C',
                  '5A', '5B', '6A', '6B', '7', '8'],
             'climate_scenario': ['2015'],
             'cooling': ['HVAC', 'MMV']
             },
        'DE':
            {'occupation': ['RT', 'MFH', 'SFH'],
             'energy standard': ['non-standard', 'standard', 'efficient', 'ZEB'],
             'RES': ['RES0', 'RES2.1', 'RES2.2', 'RES2.1+RES2.2'],
             'climate_region':
                 ['Germany'],
             'climate_scenario': ['2015'],
             'cooling': ['HVAC', 'MMV']
             },
        'CN':
            {'occupation': ['RT', 'MFH', 'SFH'],
             'energy standard': ['non-standard', 'standard', 'efficient', 'ZEB'],
             'RES': ['RES0', 'RES2.1', 'RES2.2', 'RES2.1+RES2.2'],
             'climate_region':
                 ['I', 'II', 'III', 'IV', 'V'],
             'climate_scenario': ['2015'],
             'cooling': ['HVAC', 'MMV']
             },
        'JP':
            {'occupation': ['RT', 'MFH', 'SFH'],
             'energy standard': ['non-standard', 'standard', 'efficient', 'ZEB'],
             'RES': ['RES0', 'RES2.1', 'RES2.2', 'RES2.1+RES2.2'],
             'climate_region':
                 ['JP1', 'JP2', 'JP3', 'JP4', 'JP5', 'JP6', 'JP7', 'JP8'],
             'climate_scenario': ['2015'],
             'cooling': ['HVAC', 'MMV']
             },
        'IT':
            {'occupation': ['RT', 'MFH', 'SFH'],
             'energy standard': ['non-standard', 'standard', 'efficient', 'ZEB'],
             'RES': ['RES0', 'RES2.1', 'RES2.2', 'RES2.1+RES2.2'],
             'climate_region':
                 ['Italy'],
             'climate_scenario': ['2015'],
             'cooling': ['HVAC', 'MMV']
             },
        'FR':
            {'occupation': ['RT', 'MFH', 'SFH'],
             'energy standard': ['non-standard', 'standard', 'efficient', 'ZEB'],
             'RES': ['RES0', 'RES2.1', 'RES2.2', 'RES2.1+RES2.2'],
             'climate_region':
                 ['France'],
             'climate_scenario': ['2015'],
             'cooling': ['HVAC', 'MMV']
             },
        'PL':
            {'occupation': ['RT', 'MFH', 'SFH'],
             'energy standard': ['non-standard', 'standard', 'efficient', 'ZEB'],
             'RES': ['RES0', 'RES2.1', 'RES2.2', 'RES2.1+RES2.2'],
             'climate_region':
                 ['Poland'],
             'climate_scenario': ['2015'],
             'cooling': ['HVAC', 'MMV']
             },
        'CA':
            {'occupation': ['RT', 'MFH', 'SFH'],
             'energy standard': ['non-standard', 'standard', 'efficient', 'ZEB'],
             'RES': ['RES0', 'RES2.1', 'RES2.2', 'RES2.1+RES2.2'],
             'climate_region':
                 ['CA5A', 'CA6A', 'CA7'],
             'climate_scenario': ['2015'],
             'cooling': ['HVAC', 'MMV']
             },
        'R32EU12-M':
            {'occupation': ['RT', 'MFH', 'SFH'],
             'energy standard': ['non-standard', 'standard', 'efficient', 'ZEB'],
             'RES': ['RES0', 'RES2.1', 'RES2.2', 'RES2.1+RES2.2'],
             'climate_region':
                 ['R32EU12-M'],
             'climate_scenario': ['2015'],
             'cooling': ['HVAC', 'MMV']
             },
        'IN':
            {'occupation': ['RT', 'MFH', 'SFH'],
             'energy standard': ['non-standard', 'standard', 'efficient', 'ZEB'],
             'RES': ['RES0', 'RES2.1', 'RES2.2', 'RES2.1+RES2.2'],
             'climate_region':
                 ['IN1', 'IN2', 'IN3', 'IN4', 'IN5'],
             'climate_scenario': ['2015'],
             'cooling': ['HVAC', 'MMV']
             },
        'ES':
            {'occupation': ['RT', 'MFH', 'SFH'],
             'energy standard': ['non-standard', 'standard', 'efficient', 'ZEB'],
             'RES': ['RES0', 'RES2.1', 'RES2.2', 'RES2.1+RES2.2'],
             'climate_region':
                 ['Spain'],
             'climate_scenario': ['2015'],
             'cooling': ['HVAC', 'MMV']
             },
        'UK':
            {'occupation': ['RT', 'MFH', 'SFH'],
             'energy standard': ['non-standard', 'standard', 'efficient', 'ZEB'],
             'RES': ['RES0', 'RES2.1', 'RES2.2', 'RES2.1+RES2.2'],
             'climate_region':
                 ['UK'],
             'climate_scenario': ['2015'],
             'cooling': ['HVAC', 'MMV']
             },
        'Oth-R32EU15':
            {'occupation': ['RT', 'MFH', 'SFH'],
             'energy standard': ['non-standard', 'standard', 'efficient', 'ZEB'],
             'RES': ['RES0', 'RES2.1', 'RES2.2', 'RES2.1+RES2.2'],
             'climate_region':
                 ['Oth-R32EU15'],
             'climate_scenario': ['2015'],
             'cooling': ['HVAC', 'MMV']
             },
        'Oth-R32EU12-H':
            {'occupation': ['RT', 'MFH', 'SFH'],
             'energy standard': ['non-standard', 'standard', 'efficient', 'ZEB'],
             'RES': ['RES0', 'RES2.1', 'RES2.2', 'RES2.1+RES2.2'],
             'climate_region':
                 ['Oth-R32EU12-H'],
             'climate_scenario': ['2015'],
             'cooling': ['HVAC', 'MMV']
             },
        'Oth-Asia':
            {'occupation': ['RT', 'MFH', 'SFH'],
             'energy standard': ['non-standard', 'standard', 'efficient', 'ZEB'],
             'RES': ['RES0', 'RES2.1', 'RES2.2', 'RES2.1+RES2.2'],
             'climate_region':
                 ['Indonesia'],
             'climate_scenario': ['2015'],
             'cooling': ['HVAC', 'MMV']
             },
        'Oth-LAM':
            {'occupation': ['RT', 'MFH', 'SFH'],
             'energy standard': ['non-standard', 'standard', 'efficient', 'ZEB'],
             'RES': ['RES0', 'RES2.1', 'RES2.2', 'RES2.1+RES2.2'],
             'climate_region':
                 ['Brazil'],
             'climate_scenario': ['2015'],
             'cooling': ['HVAC', 'MMV']
             },
        'Oth-MAF':
            {'occupation': ['RT', 'MFH', 'SFH'],
             'energy standard': ['non-standard', 'standard', 'efficient', 'ZEB'],
             'RES': ['RES0', 'RES2.1', 'RES2.2', 'RES2.1+RES2.2'],
             'climate_region':
                 ['Egypt'],
             'climate_scenario': ['2015'],
             'cooling': ['HVAC', 'MMV']
             },
        'Oth-MAF-Sub-Sahara':
            {'occupation': ['RT', 'MFH', 'SFH'],
             'energy standard': ['non-standard', 'standard', 'efficient', 'ZEB'],
             'RES': ['RES0', 'RES2.1', 'RES2.2', 'RES2.1+RES2.2'],
             'climate_region':
                 ['Nigeria'],
             'climate_scenario': ['2015'],
             'cooling': ['HVAC', 'MMV']
             },
        'Oth-OECD':
            {'occupation': ['RT', 'MFH', 'SFH'],
             'energy standard': ['non-standard', 'standard', 'efficient', 'ZEB'],
             'RES': ['RES0', 'RES2.1', 'RES2.2', 'RES2.1+RES2.2'],
             'climate_region':
                 ['Turkey'],
             'climate_scenario': ['2015'],
             'cooling': ['HVAC', 'MMV']
             },
        'Oth-REF':
            {'occupation': ['RT', 'MFH', 'SFH'],
             'energy standard': ['non-standard', 'standard', 'efficient', 'ZEB'],
             'RES': ['RES0', 'RES2.1', 'RES2.2', 'RES2.1+RES2.2'],
             'climate_region':
                 ['Russia'],
             'climate_scenario': ['2015'],
             'cooling': ['HVAC', 'MMV']
             },
    }

# Proxy settings
#  Define archetypes to be used instead
#  E.g. ('DE', 'SFH'): ('DE', 'MFH') will mean that the multi-family home will be used
#  instead of the single-family home for the DE region

archetype_proxies = {
    ('DE', 'SFH'): ('USA', 'SFH'),
    ('DE', 'MFH'): ('USA', 'MFH'),
    ('DE', 'RT'): ('USA', 'RT'),
    ('DE', 'informal'): ('USA', 'informal'),
    ('CN', 'SFH'): ('USA', 'SFH'),
    ('CN', 'MFH'): ('USA', 'MFH'),
    ('CN', 'RT'): ('USA', 'RT'),
    ('CN', 'informal'): ('USA', 'informal'),
    ('JP', 'SFH'): ('USA', 'SFH'),
    ('JP', 'MFH'): ('USA', 'MFH'),
    ('JP', 'RT'): ('USA', 'RT'),
    ('JP', 'informal'): ('USA', 'informal'),
    ('IT', 'SFH'): ('USA', 'SFH'),
    ('IT', 'MFH'): ('USA', 'MFH'),
    ('IT', 'RT'): ('USA', 'RT'),
    ('IT', 'informal'): ('USA', 'informal'),
    ('FR', 'SFH'): ('USA', 'SFH'),
    ('FR', 'MFH'): ('USA', 'MFH'),
    ('FR', 'RT'): ('USA', 'RT'),
    ('FR', 'informal'): ('USA', 'informal'),
    ('PL', 'SFH'): ('USA', 'SFH'),
    ('PL', 'MFH'): ('USA', 'MFH'),
    ('PL', 'RT'): ('USA', 'RT'),
    ('PL', 'informal'): ('USA', 'informal'),
    ('CA', 'SFH'): ('USA', 'SFH'),
    ('CA', 'MFH'): ('USA', 'MFH'),
    ('CA', 'RT'): ('USA', 'RT'),
    ('CA', 'informal'): ('USA', 'informal'),
    ('R32EU12-M', 'SFH'): ('USA', 'SFH'),
    ('R32EU12-M', 'MFH'): ('USA', 'MFH'),
    ('R32EU12-M', 'RT'): ('USA', 'RT'),
    ('R32EU12-M', 'informal'): ('USA', 'informal'),
    ('IN', 'SFH'): ('USA', 'SFH'),
    ('IN', 'MFH'): ('USA', 'MFH'),
    ('IN', 'RT'): ('USA', 'RT'),
    ('IN', 'informal'): ('USA', 'informal'),
    ('ES', 'SFH'): ('USA', 'SFH'),
    ('ES', 'MFH'): ('USA', 'MFH'),
    ('ES', 'RT'): ('USA', 'RT'),
    ('ES', 'informal'): ('USA', 'informal'),
    ('UK', 'SFH'): ('USA', 'SFH'),
    ('UK', 'MFH'): ('USA', 'MFH'),
    ('UK', 'RT'): ('USA', 'RT'),
    ('UK', 'informal'): ('USA', 'informal'),
    ('Oth-R32EU15', 'SFH'): ('USA', 'SFH'),
    ('Oth-R32EU15', 'MFH'): ('USA', 'MFH'),
    ('Oth-R32EU15', 'RT'): ('USA', 'RT'),
    ('Oth-R32EU15', 'informal'): ('USA', 'informal'),
    ('Oth-R32EU12-H', 'SFH'): ('USA', 'SFH'),
    ('Oth-R32EU12-H', 'MFH'): ('USA', 'MFH'),
    ('Oth-R32EU12-H', 'RT'): ('USA', 'RT'),
    ('Oth-R32EU12-H', 'informal'): ('USA', 'informal'),
    ('Oth-Asia', 'SFH'): ('USA', 'SFH'),
    ('Oth-Asia', 'MFH'): ('USA', 'MFH'),
    ('Oth-Asia', 'RT'): ('USA', 'RT'),
    ('Oth-Asia', 'informal'): ('USA', 'informal'),
    ('Oth-LAM', 'SFH'): ('USA', 'SFH'),
    ('Oth-LAM', 'MFH'): ('USA', 'MFH'),
    ('Oth-LAM', 'RT'): ('USA', 'RT'),
    ('Oth-LAM', 'informal'): ('USA', 'informal'),
    ('Oth-MAF', 'SFH'): ('USA', 'SFH'),
    ('Oth-MAF', 'MFH'): ('USA', 'MFH'),
    ('Oth-MAF', 'RT'): ('USA', 'RT'),
    ('Oth-MAF', 'informal'): ('USA', 'informal'),
    ('Oth-MAF-Sub-Sahara', 'SFH'): ('USA', 'SFH'),
    ('Oth-MAF-Sub-Sahara', 'MFH'): ('USA', 'MFH'),
    ('Oth-MAF-Sub-Sahara', 'RT'): ('USA', 'RT'),
    ('Oth-MAF-Sub-Sahara', 'informal'): ('USA', 'informal'),
    ('Oth-OECD', 'SFH'): ('USA', 'SFH'),
    ('Oth-OECD', 'MFH'): ('USA', 'MFH'),
    ('Oth-OECD', 'RT'): ('USA', 'RT'),
    ('Oth-OECD', 'informal'): ('USA', 'informal'),
    ('Oth-REF', 'SFH'): ('USA', 'SFH'),
    ('Oth-REF', 'MFH'): ('USA', 'MFH'),
    ('Oth-REF', 'RT'): ('USA', 'RT'),
    ('Oth-REF', 'informal'): ('USA', 'informal')
}

# Climate station settings
#  Defines sub-regions and allows assigning them climate files

climate_stations = {
    'USA': {
        '1A': 'Miami_FL-hour.epw',
        '2A': 'Houston_Airp_TX-hour.epw',
        '2B': 'Phoenix_AZ-hour.epw',
        '3A': 'Atlanta_GA-hour.epw',
        '3B-Coast': 'Los_Angeles_CA-hour.epw',
        '3B': 'Las_Vegas_NV-hour.epw',
        '3C': 'San_Francisco_CA-hour.epw',
        '4A': 'Baltimore_MD-hour.epw',
        '4B': 'US-Albuquerque_NM-hour.epw',
        '4C': 'Seattle_Tacoma_WA-hour.epw',
        '5A': 'Chicago_IL-hour.epw',
        '5B': 'Boulder_CO-hour.epw',
        '6A': 'Minneapolis_Airp_MN-hour.epw',
        '6B': 'Helena_MT-hour.epw',
        '7': 'Duluth_Airp_MN-hour.epw',
        '8': 'Fairbanks_AK-hour.epw'},
    'DE': {'Germany': 'Frankfurt_am_Main_Airp_-hour.epw'},
    'CN': {'I': 'CN-Harbin.epw',
           'II': 'CN-Beijing.epw',
           'III': 'CN-Wuhan.epw',
           'IV': 'CN-Haikou.epw',
           'V': 'CN-Kunming.epw'},
    'JP': {
        'JP1': 'JP-Asahikawa-hour.epw',
        'JP2': 'JP-Sapporo-hour.epw',
        'JP3': 'JP-Morioka-hour.epw',
        'JP4': 'JP-Sendai-hour.epw',
        'JP5': 'JP-Tsukuba_JA-hour.epw',
        'JP6': 'JP-Osaka-hour.epw',
        'JP7': 'JP-Miyazaki-hour.epw',
        'JP8': 'JP-Naha-hour.epw'},
    'IT': {'Italy': 'Roma_Ciampino-hour.epw'},
    'FR': {'France': 'PARIS_FR-hour.epw'},
    'PL': {'Poland': 'PL-Warszawa-hour.epw'},
    'CA': {'CA5A': 'Chicago_IL-hour.epw',
           'CA6A': 'Minneapolis_Airp_MN-hour.epw',
           'CA7': 'Duluth_Airp_MN-hour.epw'},
    'R32EU12-M': {'R32EU12-M': 'PL-Warszawa-hour.epw'},
    'IN': {
        'IN1': 'IN-Jodhpur.epw',
        'IN2': 'IN-Santacruz_Bombay.epw',
        'IN3': 'IN-Bangalore.epw',
        'IN4': 'IN-Shimla.epw',
        'IN5': 'IN-Hyderabad.epw'},
    'ES': {'Spain': 'Madrid_Barajas-hour.epw'},
    'UK': {'UK': 'Aughton-hour.epw'},
    'Oth-R32EU15': {'Oth-R32EU15': 'PL-Warszawa-hour.epw'},
    'Oth-R32EU12-H': {'Oth-R32EU12-H': 'PL-Warszawa-hour.epw'},
    'Oth-OECD': {'Turkey': 'Istanbul_TU-hour.epw'},
    'Oth-REF': {'Russia': 'MOSKVA_RS-hour.epw'},
    'Oth-Asia': {'Indonesia': 'JAKARTA_ID-hour.epw'},
    'Oth-MAF': {'Egypt': 'CAIRO_EG-hour.epw'},
    'Oth-MAF-Sub-Sahara': {'Nigeria': 'BENIN_NI-hour.epw'},
    'Oth-LAM': {'Brazil': 'Rio_de_Janeiro_BR-hour.epw'}
}

# Material settings
#  Assign material categories to individual materials.
#  This will be used in the final aggregation for material intensity.

odym_materials = {'Asphalt_shingle': 'other',
                  'Air_4_in_vert': 'other',
                  'Bldg_paper_felt': 'paper and cardboard',
                  'Std Wood 6inch': 'wood and wood products',
                  'Std Wood 10cm': 'wood and wood products',
                  'Lumber_2x4': 'wood and wood products',
                  'OSB_1/2in': 'wood and wood products',
                  'OSB_5/8in': 'wood and wood products',
                  'Stucco_1in': 'cement',
                  'F07 25mm stucco': 'cement',
                  'F07 50mm stucco': 'cement',
                  'F07 10mm stucco': 'cement',
                  'Concrete_tiles_25mm': 'concrete',
                  'Bitumen_20mm': 'other',
                  'sheathing_consol_layer': 'wood and wood products',
                  'Drywall_1/2in': 'wood and wood products',
                  'G01 16mm gypsum board': 'other',
                  'G01 13mm gypsum board': 'other',
                  'ceil_consol_layer-en-non-standard': 'other',
                  'ceil_consol_layer-en-standard': 'other',
                  'ceil_consol_layer-en-efficient': 'other',
                  'ceil_consol_layer-en-ZEB': 'other',
                  'door_const': 'wood and wood products',
                  'Glass-en-non-standard': 'other',
                  'Glass-en-standard': 'other',
                  'Glass-en-efficient': 'other',
                  'Glass-en-ZEB': 'other',
                  'Plywood_3/4in': 'wood and wood products',
                  'Carpet_n_pad': 'other',
                  'floor_consol_layer': 'wood and wood products',
                  'Concrete_20cm': 'concrete',
                  'Reinforcement_1perc_20cm': 'construction grade steel',
                  'Concrete_15cm': 'concrete',
                  'Reinforcement_1perc_15cm': 'construction grade steel',
                  'Concrete_12cm': 'concrete',
                  '100mm Normalweight concrete floor': 'concrete',
                  '175mm Normalweight concrete floor': 'concrete',
                  '200mm Normalweight concrete floor': 'concrete',
                  'Reinforcement_1perc_12cm': 'construction grade steel',
                  'wall_consol_layer-en-non-standard': 'other',
                  'wall_consol_layer-en-standard': 'other',
                  'wall_consol_layer-en-efficient': 'other',
                  'wall_consol_layer-en-ZEB': 'other',
                  'F13 Built-up roofing': 'other',
                  'F08 Metal surface': 'other',
                  'Reinforcement_2perc_15cm': 'construction grade steel',
                  'Reinforcement_3perc_15cm': 'construction grade steel',
                  'Reinforcement_2perc_20cm': 'construction grade steel',
                  'Reinforcement_2perc_30cm': 'construction grade steel',
                  'Concrete_30cm': 'concrete',
                  'Concrete_10cm': 'concrete',
                  'Reinforcement_1perc_10cm': 'construction grade steel',
                  'Concrete_18cm': 'concrete',
                  'Reinforcement_2perc_17cm': 'construction grade steel',
                  'CLT_170mm': 'wood and wood products',
                  'Concrete_60cm': 'concrete',
                  'Reinforcement_1perc_60cm': 'construction grade steel',
                  'High pressure laminate panel': 'other',
                  'Concrete_4cm': 'concrete',
                  'Concrete_5cm': 'concrete',
                  'Concrete_7cm': 'concrete',
                  'Reinforcement_1perc_7cm': 'construction grade steel',
                  'Cement_plaster_0.012': 'cement',
                  'Brick - fired clay - 1920 kg/m3 - 200mm': 'brick',
                  'Brick - fired clay - 1920 kg/m3 - 300mm': 'brick',
                  'Brick - fired clay - 1600 kg/m3 - 102mm': 'brick',
                  'Brick - fired clay - 1600 kg/m3 - 230mm': 'brick',
                  'Metal_surface': 'other',
                  'Reinforcement_2perc_10cm': 'construction grade steel',
                  'roof_consol_layer-en-standard': 'other',
                  'Brick - fired clay - 1120 kg/m3 - 102mm': 'brick',
                  'Brick inner 105 mm_0.1': 'brick',
                  'Roof Tile_0.01': 'other'
                  }

# Region settings
#  Translates BuildME regions to ODYM regions in the final result file

odym_regions = {'USA': 'R32USA',
                'CA': 'R32CAN',
                'CN': 'R32CHN',
                'R32EU12-M': 'R32EU12-M',
                'IN': 'R32IND',
                'JP': 'R32JPN',
                'FR': 'France',
                'DE': 'Germany',
                'IT': 'Italy',
                'PL': 'Poland',
                'ES': 'Spain',
                'UK': 'UK',
                'Oth-R32EU15': 'Oth_R32EU15',
                'Oth-R32EU12-H': 'Oth_R32EU12-H',
                'Oth-OECD': 'R5.2OECD_Other',
                'Oth-REF': 'R5.2REF_Other',
                'Oth-Asia': 'R5.2ASIA_Other',
                'Oth-MAF-Sub-Sahara': 'R5.2MAF_Other_Sub_Sahara',
                'Oth-MAF': 'R5.2MAF_Other',
                'Oth-LAM': 'R5.2LAM_Other'}

# Logging settings
# The logging settings were adapted from:
# https://guicommits.com/how-to-log-in-python-like-a-pro/
ERROR_LOG_FILENAME = '.BuildME-errors.log'  # TODO(cbreton026): Add specific path?

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            "datefmt": "%Y-%m-%d %H:%M:%S",  # How to display dates
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',  # Originally 'INFO'
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
        'logfile': {
            'level': 'ERROR',
            'formatter': 'standard',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': ERROR_LOG_FILENAME,
            'maxBytes': 1048576,  # 1*1024*1024 or 1MB
            'backupCount': 2,  # Keeps up to two 1MB logfiles
        },
    },
    'loggers': {
        'BuildME': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': False
        },
        '__main__': {  # if __name__ == '__main__'
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': False
        },
    },
    'root': {
        'level': 'INFO',  # Affects all, except defined loggers
        'handlers': ['default', 'logfile'],
    },
}
