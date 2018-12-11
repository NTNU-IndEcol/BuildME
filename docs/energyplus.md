# Documentation on energyplus

## IDF Version updater

The e+ input files (.idf) are version specific. That means the need to be upgraded / converted to the latest version of e+. Currently v9.0 is the latest version. However it only contains an updater that works down to version 7.2. However the e+ community provides a multi-update tool for Windows: http://energyplus.helpserve.com/Knowledgebase/Article/View/86/46/windows---programs-for-converting-older-pre-v720-idf-files-to-current-or-intermediate-versions

However, that file only updates to v8.4, which means the updater that comes with e+ must also be run after that.

## Procedure

There [seems to be](https://github.com/NREL/EnergyPlus/issues/7097) no equivalent of `RunEP.bat` from Windows for macOS. So I am not sure where this is documented in the macOS version.

https://bigladdersoftware.com/epx/docs/9-0/auxiliary-programs/running-energyplus-by-hand.html

1. Run `./ExpandObjects`
2. *Optional*: Run necessary preprocessors
    - `./Basement` if `BasementGHTIn.idf` is present
    - `./Slab` if ??? is present
3. *If preprocessors were run:* Append `expanded.idf` with `EPObjects.txt`
4. Run `./energyplus -r expanded.idf`