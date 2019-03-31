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
climate_files = "./data/climate/meteonorm71/"
tmp_path = "./tmp/"

# The combinations
#   Example: USA.SFH_standard.RES0.
combinations = {'all': {'occupation_types':
                            ['SFH_non-standard', 'SFH_standard', 'SFH_efficient', 'SFH_ZEB',
                             'MFH_non-standard', 'MFH_standard', 'MFH_efficient', 'MFH_ZEB',
                             'informal_non-standard'],
                        'RES':  # Resource Efficiency Strategy
                            ['RES0'],
                        'climate_scenario':
                            ['2015',
                             '2030_A1B', '2030_A2', '2030_B1',
                             '2050_A1B', '2050_A2', '2050_B1']},
                'USA': {
                    'climate_region':
                        ['1A', '1B', '2A', '2B', '3A', '3B-Coast', '3B', '3C',
                         '4A', '4B', '4C', '5A', '5B', '6A', '6B', '7', '8']}
                }
