# Setup BuildME

## Initial setup

- Download and copy the [desired energyplus binaries](https://energyplus.net/downloads) into e.g. `./bin/EnergyPlus-9-2-0`. See also the [Energyplus](#Energyplus) section below for more info.
- Correct the paths in `BuildME/settings.py`

The current version should work on macOS and Windows. Linux support could easily be added by editing `ep_exec_files` in `settings.py`.

## Environment

We recommend using a dedicated [Python environment](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html#managing-environments) using Miniconda. Learn more on how to install [here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).

## Instaling dependencies

[//]: # "TODO"

BuildME relies on the great [eppy](https://github.com/santoshphilip/eppy) package. However, it is not listed as a Anaconda package. Therefore installation requires the use of `pip`. In case you use miniconda, follow [this procedure](https://stackoverflow.com/a/43729857/2075003):
```bash
conda install pip 
which pip  # make sure the path corresponds to your conda environment
pip install eppy
```

## Energyplus

Please not that the archetype files in  the [archetypes folder](archetypes) are specific to the energyplus version. If your binaries in `./bin/` do not correspond to the ones in the `.idf` files (see `Version` keyword), you are likely to run into issues. 