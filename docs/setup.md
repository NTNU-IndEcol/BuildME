# Setup BuildME

## Initial setup

- Set up the Python environment ([Python environment](#Python-environment))
- Download EnergyPlus ([Energyplus](#Energyplus))
- Correct the paths in `BuildME/settings.py` ([settings.py](#settings.py))
- (Optional) Include more weather files ([Weather files](#Weather-files))

BuildME should work on Windows, Linux, and MacOS (after adjustments: see [MacOS](#macos)). Adding the support for other platform requires editing the function `get_exec_files()` in `energy.py`.

### Python environment
Before the Python environment is being set up, the user needs to install a source-code editor and a Python interpreter. An example of a source-code editor is Visual Studio Code, which can be used to edit both Python files and Jupyter Notebook files (i.e., the BuildME tutorial). For the Python interpreter, we recommend a dedicated [Python environment](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html#managing-environments) installed e.g., using Miniconda. Miniconda is a minimal installation package for Anaconda, which takes less space compared to a full Anaconda installation and allows customizable package dependencies.

Python dependencies can be installed automatically using the buildme.yml file or manually, using the instructions below.

Installing Python dependencies automatically involves opening Anaconda prompt and typing "conda env create -f environment.yml", which should automatically install all the packages. 

Installing Python dependencies manually involves opening Anaconda prompt and first, creating an environment by typing "conda create -n buildme". Then, the environment can be activated ("conda activate buildme"), and packages can be installed one by one ("conda install package_name"). 

However, BuildME relies also on the [eppy](https://github.com/santoshphilip/eppy) package, which is not listed as an Anaconda package, and therefore its installation requires the use of `pip`. In case you use Miniconda, follow [this procedure](https://stackoverflow.com/a/43729857/2075003):
```
conda install pip 
pip install eppy
```

All other dependencies can be installed directly using conda:
- numpy
- pandas
- openpyxl
- tqdm
- ipykernel
- matplotlib
- seaborn

### Energyplus

Download and copy the [desired energyplus binaries](https://energyplus.net/downloads) into e.g. `./bin/EnergyPlus-9-2-0`. 

Please note that the archetype files in the archetypes folder are specific to the energyplus version. If your binaries in `./bin/` do not correspond to the ones in the `.idf` files (see `Version` keyword), you are likely to run into issues. 

One way to solve this issue is to install EnergyPlus version specified in the settings.ep_version variable. Another way is to convert the IDF files to the desired version of EnergyPlus using the IDF Version Updater found in the EnergyPlus folder and "PreProcess" subfolder.

### settings.py
BuildME relies on correct path names, e.g., to EnergyPlus software. Before you run BuildME, make sure that all the paths listed in `BuildME/settings.py` are correct. In addition, you may also change the configuration file BuildME_config_V1.0.xlsx, e.g., to adjust the variable `debug_combinations`, which lists the default combination of bulding characteristics used in a batch simulation. 

### Weather files

The default BuildME setup includes only one weather file (.EPW) for New York, NY, made available by the U.S. Department of Energy [here](https://www.energycodes.gov/prototype-building-models). The full functionality of the BuildME framework can be achieved by including more weather files - these need to be created by licensed software, e.g., Meteonorm, or alternatively found in online repositories, e.g., [Climate.OneBuilding](https://climate.onebuilding.org). Meteonorm offers historical weather data and future data based on scenarios from the Intergovernmental Panel on Climate Change (IPCC). 

### MacOS 

macOS does not allow to run unnotarized apps. Therefore, it is necessary to allow energyplus to run. If you have issues, try the following:
- Open `System Preferences > Security & Privacy` If you see the button `Allow anyway`, click it. This step has to be repeated for each library and executable :(
- Open `System Preferences > Security & Privacy > Privacy`, scroll to `Developper Tools` and add `Terminal.app` 
- Run `sudo xattr -d -r com.apple.quarantine ./bin/EnergyPlus-9-6-0` on your energyplus folder.






