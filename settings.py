ep_path = "./bin/EnergyPlus-9-0-1/"
ep_version = '9.0.1'
ep_exec_files = ["energyplus", "energyplus-%s" % ep_version, "Energy+.idd", "EPMacro", "ExpandObjects",
                 "libenergyplusapi.%s.dylib" % ep_version,   # required by energyplus
                 "libgfortran.3.dylib",  "libquadmath.0.dylib", # required by ExpandObjects
                 "PreProcess/GrndTempCalc/Basement", "PreProcess/GrndTempCalc/BasementGHT.idd",
                 "PostProcess/ReadVarsESO"
                 ]
archetypes = "./data/archetype/"
climate_files = "./data/climate/meteonorm71/"
tmp_path = "./tmp/"
