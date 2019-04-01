"""
Settings and constants required for the model to run.

Copyright: Niko Heeren, 2019
"""

ep_version = '9.0.1'
ep_path = "./bin/EnergyPlus-9-0-1/"
ep_idd = "bin/EnergyPlus-9-0-1/Energy+.idd"
ep_exec_files = ["energyplus", "energyplus-%s" % ep_version, "Energy+.idd", "EPMacro", "ExpandObjects",
                 "libenergyplusapi.%s.dylib" % ep_version,  # required by energyplus
                 "libgfortran.3.dylib", "libquadmath.0.dylib",  # required by ExpandObjects
                 "PreProcess/GrndTempCalc/Basement", "PreProcess/GrndTempCalc/BasementGHT.idd",
                 "PostProcess/ReadVarsESO"
                 ]
archetypes = "./data/archetype/"
tmp_path = "./tmp/"

# The combinations
#   Example: USA.SFH_standard.RES0.
combinations = \
    {
        'all':  # maybe not necessary
            {'occupation_types':
                 ['SFH_non-standard', 'SFH_standard', 'SFH_efficient', 'SFH_ZEB',
                  'MFH_non-standard', 'MFH_standard', 'MFH_efficient', 'MFH_ZEB',
                  'informal_non-standard'],
             'RES': ['RES0'],
             'climate_scenario':
                 ['2015',
                  '2030_A1B', '2030_A2', '2030_B1',
                  '2050_A1B', '2050_A2', '2050_B1']},
        'USA':
            {'occupation': ['SFH', 'MFH', 'informal'],
             'energy standard': ['non-standard', 'standard', 'efficient', 'ZEB'],
             'RES': ['RES0'],
             'climate_region':
                 ['1A', '2A', '2B', '3A', '3B-Coast', '3B', '3C',
                  '4A', '4B',
                  # TODO: Climate file missing for '4C',
                  '5A', '5B', '6A', '6B', '7', '8'],
             'climate_scenario': ['2015']
             }
    }

climate_files_path = "./data/climate/meteonorm71/"
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
        '4B': 'Albuquerque_NM-hour.epw',
        # TODO Climate file missing '4C': 'Seattle, Washington',
        '5A': 'Chicago_IL-hour.epw',
        '5B': 'Boulder_CO-hour.epw',
        '6A': 'Minneapolis_Airp_MN-hour.epw',
        '6B': 'Helena_MT-hour.epw',
        '7': 'Duluth_Airp_MN-hour.epw',
        '8': 'Fairbanks_AK-hour.epw'
    }
}
