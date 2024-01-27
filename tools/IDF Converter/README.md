# **Documentation on IDF Converter for BuildME**

## **1. Introduction and Motivation**

This document summarizes the main functions of the IDF converter for BuildME and the general workflow to follow once new IDF files need to be implemented in BuildME. This process is cumbersome to perform manually, as there are a lot of fields and files to be modified and generally, mistakes occur. The IDF converter for BuildME allows users to convert IDF files in an automated way. The script requests different individual IDF files representing various energy standards, cohorts, or regions for the same architectural geometry. The script merges these alternatives into one single IDF file where all material and construction combinations are stored together. For instance, if a user has villa IDFs corresponding to three different construction years and uses distinctive materials in each; these three IDFs can be merged via IDF converter together, and BuildME can access cohort-specific materials during simulations. Also, only a single file can be converted at a time and implemented to BuildME.

The application inserts *"replaceme"* strings in surface elements, and BuildME automatically detect these fields and replaces them according to the user debugging settings. The current version of BuildME performs modifications of the input archetype file depending on the chosen aspects for the Energy standard, RES, and Cooling system. However, this list can be expanded by including cohorts, climate characteristics, and many more.

## **2. Workflow**

IDF Converter for BuildME uses three main functions in total. Moreover, there are additional functions to support csv file exports which can be used to update existing replace files stored in BuildME/data folder. In the upcoming sections, these functions will be introduced thoroughly.

### **2.1 Main Converter Functions**

The functions convert each IDF file introduced by adding *"replaceme"* strings to the surface material names, updating materials/constructions accordingly. If desired, a non-standard energy standard version of the base IDF can be created (optional). All converted IDFs can be merged into one single archetype IDF file (optional) compatible with BuildME.

##### **2.1.1 convert_IDF_to_BuildME()**
This function creates an individual edited IDF file that is compatible with BuildME framework.
Users can define as many replaceme layers they desire.The replace string values should be set accordingly to the replacer string during the conversion.  To illustrate, some examples are given in Table 1.

| Replace String    | Base IDF  | Alternative IDF 1 | Alternative IDF 2 | Alternative IDF 3 |
|-------------------|-----------|-------------------|-------------------|-------------------|
| -en-std-replaceme | -standard | -efficient        | -ZEB              | -energyPlus       |
| -chr-replaceme    | -1980     | -1990             | -2000             | -2010             |
| -res-replaceme    | -RES0     | -RES1.1           | -RES2.0           | -RES2.2           |
| -climate-replaceme | -Istanbul | -Ankara           | -Izmir            | -Kutahya          |
*Table 1. Replacer and replace string examples*
* *Requirements:* Window-Skylight Difference should be addressed in the construction name (e.g. name contains "sky")

* *Python Example:*
```def convert_IDF_to_BuildME (IDF_path, save_folder_path, replace_string="-en-std-replaceme", replace_string_value="-non-standard", base=False)```

* *Run Order:* 
  1) Adds replaceme fields,
  2) Renames Materials,
  3) Renames Constructions,
  4) Defines non-standard U values, if replace_string_value is set as it contains “non-standard” string.

* *Variables:*

  **IDF_path:** path for an IDF file to be converted
  
  **save_folder_path:** New location folder path, where the new IDF will be saved
  
  **replace_string:** Replaceme content (i.e., -en-std-replaceme-res-replaceme-chr-replaceme), should start with "-"
  
  **replace_string_value:** Replacer string corresponding to the replace string (i.e., -standard-RES0-1920), should start with "-"
  
  **base:** Boolean value to declare whether the IDF file corresponding to a base IDF, meaning that a base IDF to be used as a template to merge the others into. 
  
  **returns:** An individual IDF file compatible with BuildME

  For non-standard energy standard, a user needs to use the same path name as the standard IDF’s one, and set **base** variable to False. An example can be given as:
  
  ```convert_idf_to_BuildME(idfpathstandard, savefolderpath, replace_string="-en-std-replaceme-res-replaceme",replace_string_value="-non-standard-RES0", base=False)```
  
  While the standard version can be written as:
  
  ```convert_idf_to_BuildME(idfpathstandard, savefolderpath,, replace_string="-en-std-replaceme-res-replaceme",replace_string_value="-standard-RES0", base=True)```

##### **2.1.2 create_combined_idflist ()**
Creates a list containing all converted IDF files

* *Python Example:* ```def create_combined_idflist(save_folder_path)```

* *Variables:*

  **save_folder_path:** (in other words, save folder) containing all generated IDFs for a single archetype type (e.g. RT only)

  **returns:** a list containing all converted IDFs

##### **2.1.3 create_combined_idf_archetype ()**

Combines all materials, constructions stored in different IDFs and merges them into a single IDF file

* *Python Example:* ```def create_combined_idf_archetype(save_folder_path, IDFlist=list)```

* *Run Order:* 
  1) Gathers all material and construction objects stored in IDFs individual lists,
  2) Selects the base IDF and deletes all construction and material objects,
  3) Creates new materials and constructions from the lists created in 1,
  4) Redefines output variables in a way that BuildME accepts,
  5) Saves a new IDF file, ready to be used with BuildME,

* *Variables:*

  **save_folder_path:** save folder, where the new merged IDF will be saved

  **IDFlist:** IDF list containing the IDF files to be merged; this list should only contain an archetype type at a time (e.g. only SFH)

  **returns**: A new merged archetype IDF for BuildME

###  **2.2 File Export Functions**

BuildME uses additional files located in BuildME/data folder to manipulate the permutations during simulations. New data from the IDFs should be introduced to the existing files. New data can be translated in a csv file format.

#### **2.2.1 update_replace_csv()**

Creates a csv file that stores the new values from the new IDF files. 

* *Python Example:* ```def update_replace_csv(IDFlist,save_folder_path, Region, Occupation, replace_string)```

* *Variables:*

  **IDFlist:** A list that contains IDF files

  **save_folder_path:** Save folder for the csv file

  **Region:** Region

  **Occupation:** Occupation type

  **replace_string:** Replaceme content (i.e., -en-std-replaceme-res-replaceme-chr-replaceme), should start with "-"

  **Returns:** csv file with new idf values


##### **2.2.2. update_all_datafile_csv ()**

Creates csv files for new replace.csvs

* *Python Example:* ```def update_all_datafile_csv(IDFlist,merged_IDF,save_folder_path,replace_string)```

* *Variables:*

  **IDFlist:** list that contains IDF files

  **merged_IDF:** Merged IDF file

  **save_folder_path:** save folder for conversion outputs

  **replace_string:** Replaceme content (i.e., -en-std-replaceme-res-replaceme-chr-replaceme), should start with "-"

  **Returns:** summary and csv files

### **Appendix-Code Example**
 ```
    #USER SPECIFIC INPUTS:
    #EXAMPLE PURPOSES ONLY

    # 1st IDF to be converted:standard
    path1 = "..\\data\\archetype\\new_archetypes\\SFH_tobeconverted.idf"
    # 2nd IDF to be converted:efficient
    path2 = "..\\data\\archetype\\new_archetypes\\SFHefficient_tobeconverted.idf"

    # Main Folder, every generated data will be located
    # Tip: make sure to put the 'r' in front
    folderpath = r"..\\data\\archetype\\new_archetypes\\new"

    #replace_string should start with "-" and end with "-replaceme"
    convert_idf_to_BuildME(path1, folderpath, replace_string="-en-std-replaceme-res-replaceme",replace_string_value="-standard-RES0", base=True)
    convert_idf_to_BuildME(path2, folderpath, replace_string="-en-std-replaceme-res-replaceme",replace_string_value="-efficient-RES0", base=False)
    #On demand, a non-standard option for the IDF is also can be created by assigning 30% worse performing values to the standard file.
    convert_idf_to_BuildME(path1, folderpath, replace_string="-en-std-replaceme-res-replaceme",
                           replace_string_value="-non-standard-RES0", base=False)


    listed = create_combined_idflist(folderpath)
    merged_idf=create_combined_idf_archetype(folderpath, listed)
    update_all_datafile_csv(listed,folderpath,replace_string="-chr-replaceme-res-replaceme")
```
