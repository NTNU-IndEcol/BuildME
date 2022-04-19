**Documentation on IDF Converter for BuildME**

1.  **Introduction and Motivation**

This document summarizes the main functions of the IDF converter for BuildME and the general workflow to follow once new IDF files need to be implemented in BuildME. This process is cumbersome to perform manually, as there are a lot of fields and files to be modified and generally, mistakes often occur. The IDF converter for BuildME allows users to convert IDF files in an automated way. The script requests different individual IDF files representing various energy standards, cohorts, or regions for the same architectural geometry. The script merges these alternatives into one single IDF file where all material and construction combinations are stored together. For instance, if a user has villa IDFs corresponding to three different construction years and uses distinctive materials in each; these three IDFs can be merged via IDF converter together, and BuildME can access cohort-specific materials during simulations. Also, only a single file can be converted at a time and implemented to BuildME.

The application inserts *"replaceme"* strings in surface elements, and BuildME automatically detect these fields and replaces them according to the user debugging settings. The current version of BuildME performs modifications of the input archetype file depending on the chosen aspects for the Energy standard, RES, and Cooling system. However, this list can be expanded by including cohorts, climate characteristics, and many more.

1.  **Workflow**

IDF Converter for BuildME uses three main functions in total. Moreover, there are additional functions to support xlsx and yaml file exports which can be used to update existing replace and material files stored in BuildME/data folder. In the upcoming sections, these functions will be introduced thoroughly.

1.  **Main Converter Functions**

The functions convert each IDF file introduced by adding *"replaceme"* strings to the surface material names, updating materials/constructions accordingly. If desired, a non-standard energy standard version of the base IDF can be created (optional). All converted IDFs can be merged into one single archetype IDF file (optional) compatible with BuildME.

**2.1.1 convert_IDF_to_BuildME()**

**Description:** This function creates an individual edited IDF file that is compatible with BuildME framework.

**Requirements:** Window-Skylight Difference should be addressed in the construction name (e.g. name contains "sky")

**Python Example:** *def convert_IDF_to_BuildME (IDF_path, save_folder_path, replace_string="-en-std-replaceme", replace_string_value="-non-standard", base=False)*

**Run Order:**

\-Adds replaceme fields,

\-Renames Materials,

\-Renames Constructions,

\-Defines non-standard U values, if replace_string_value is set as it contains “non-standard” string.

**Variables:**

**IDF_path:** path for an IDF file to be converted

**save_folder_path:** New location folder path, where the new IDF will be saved

**replace_string:** Replaceme content (i.e., -en-std-replaceme-res-replacemem-chrt-replaceme), should start with "-"

**replace_string_value***:* Replacer string corresponding to the replace string (i.e., -standard-RES0-1920), should start with "-"

**base:** Boolean value to declare whether the IDF file corresponding to a base IDF

**returns***:* An individual IDF file compatible with BuildME

For non-standard energy standard, a user needs to use the same path name as the standard IDF’s one, and set **base** variable to False. An example can be given as:

*convert_idf_to_BuildME(idfpathstandard, savefolderpath, replace_string="-en-std-replaceme-res-replaceme",replace_string_value="-non-standard-RES0", base=False)*

while the standard version can be written as:

*convert_idf_to_BuildME(idfpathstandard, savefolderpath,, replace_string="-en-std-replaceme-res-replaceme",replace_string_value="-standard-RES0", base=True)*

**2.1.2 create_combined_idflist ()**

**Description:** Creates a list containing all converted IDF files

**Python Example:** *create_combined_idflist(save_folder_path)*

**Variables:**

**save_folder_path:** (in other words, save folder) containing all generated IDFs for a single archetype type (e.g. RT only)

**returns***:* a list containing all converted IDFs

**2.1.3 create_combined_idf_archetype ()**

**Description:** *Combines all materials, constructions stored in different IDFs and merges them into a single IDF file*

**Python Example:** *def create_combined_idf_archetype(save_folder_path, IDFlist=list)*

**Run Order:**

1)Gathers all material and construction objects stored in IDFs individual lists

2)Selects the base IDF and deletes all construction and material objects

3)Creates new materials and constructions from the lists created in 1.

4)Redefines output variables in a way that BuildME accepts

5)Saves a new IDF file, ready to be used with BuildME

**Variables:**

**save_folder_path:** *save folder, where the new merged IDF will be saved*

**IDFlist:** *IDF list containing the IDF files to be merged; this list should only contain an archetype type at a time (e.g. only SFH)*

**returns***: A new merged archetype IDF for BuildME*

1.  **File Export Functions**

BuildME uses additional files located in BuildME/data folder to manipulate the permutations during simulations. New data from the IDFs should be introduced to the existing files. New data can be translated either in YAML or xlsx file format. Users can select whichever option they prefer as BuildME accepts both file types.

**2.2.1 YAML functions**

**2.2.1.1 create_yaml_userreplace()**

**Description:** *Creates a yaml file that stores the new values from the new IDF files. The current version now only collects infiltration values. However, the code can be manipulated if needed.*

**Python Example:** *create_yaml_userreplace(IDFlist,save_folder_path, Region, Occupation)*

**Variables:**

**IDFlist:** *list that contains IDF files*

**save_folder_path:** *Save folder for the yaml file*

**Region:** *Region*

**Occupation:** *Occupation type*

**Returns:** *yaml file with infiltration values*

**2.2.1.2 create_yaml_userreplace()**

**Description:** *Creates two yaml files storing the new materials from the new IDF files.*

**Python Example:** *create_yaml_usermaterials(merged_IDF,save_folder_path, Region):*

**Variables:**

**merged_IDF:** *Merged IDF file*

**save_folder_path:** *Save folder for the yaml file*

**Region:** *Region*

**Returns:** *a yaml file for nomass materials and another one containing all new materials for odym region assignment*

**2.2.1.3 update_all_datafile_yaml()**

**Description:** *Creates yaml files*

**Python Example:** *update_all_datafile_yaml(IDFlist,merged_IDF,save_folder_path)*

**Variables:**

**IDFlist:** *list that contains IDF files*

**merged_IDF:** *Merged IDF file*

**save_folder_path:** *save folder for conversion outputs*

**Returns:** *summary and yaml files*

**2.2.2 XLSX functions**

**2.2.2.1 update_replace_xlsx()**

**Description:** Creates an xlsx file that stores the new values from the new IDF files. The current version now only collects infiltration values.

**Python Example:** *update_replace_xlsx(IDFlist,save_folder_path, Region, Occupation)*

**Variables:**

**IDFlist:** *a list that contains IDF files*

**save_folder_path:** *Save folder for the xlsx file*

**Region:** *Region*

**Occupation:** *Occupation type*

**Returns:** *xlsx file with infiltration values*

**2.2.2.2 update_material_xlsx ()**

**Description:** *Creates an xlsx file storing the new materials comes from the new IDF files.*

**Python Example:** *update_material_xlsx(merged_IDF,save_folder_path,Region)*

**Variables:**

**merged_IDF:** *Merged IDF file*

**save_folder_path:** *Save folder for the xlsx file*

**Region:** *Region*

**Returns:** *A xlsx file storing nomass materials and all new materials for odym region assignment*

**2.2.2.3 update_all_datafile_xlsx ()**

**Description:** *Creates xlsx files*

**Python Example:** *update_all_datafile_yaml(IDFlist,merged_IDF,save_folder_path)*

**Variables:**

**IDFlist:** *list that contains IDF files*

**merged_IDF:** *Merged IDF file*

**save_folder_path:** *save folder for conversion outputs*

**Returns:** *summary and xlsx files*

**Appendix-Code Example***  
  
\# 2006 IECC idf File Path (standard)  
path1 = "..\\\\data\\\\archetype\\\\new_archetypes\\\\IdealLoads\\\\BUILDME_SchoolSecondary\\\\IdealLoads_SchoolSecondary.idf"  
  
\# 2012 IECC idf File Path (efficient)  
path2 = "..\\\\data\\\\archetype\\\\new_archetypes\\\\IdealLoads\\\\BUILDME_SchoolSecondary\\\\IECC_SchoolSecondary_STD2012_NewYork.idf"  
  
\# 2018 IECC File Path (ZEB)  
path3 = "..\\\\data\\\\archetype\\\\new_archetypes\\\\IdealLoads\\\\BUILDME_SchoolSecondary\\\\IECC_SchoolSecondary_STD2018_NewYork.idf"  
  
\# Main Folder, every generated data will be located  
folderpath = r"..\\\\data\\\\archetype\\\\new_archetypes\\\\IdealLoads\\\\BUILDME_SchoolSecondary"  
  
convert_idf_to_BuildME(path1, folderpath, replace_string="-en-std-replaceme-res-replaceme",replace_string_value="-non-standard-RES0", base=False)  
convert_idf_to_BuildME(path1, folderpath, replace_string="-en-std-replaceme-res-replaceme",replace_string_value="-standard-RES0", base=True)  
convert_idf_to_BuildME(path2, folderpath, replace_string="-en-std-replaceme-res-replaceme", replace_string_value="-efficient-RES0", base=False)  
convert_idf_to_BuildME(path3, folderpath, replace_string="-en-std-replaceme-res-replaceme", replace_string_value="-ZEB-RES0", base=False)  
  
listed = create_combined_idflist(folderpath)  
merged_idf=create_combined_idf_archetype(folderpath, listed)  
update_all_datafile_xlsx(listed,merged_idf,folderpath)*

**Documentation on IDF Converter App for BuildME**

1.  **Introduction**

IDF Converter App for BuildME uses the same functions mentioned above but offers a more user-friendly interface for users with limited coding competencies. The app was created by using a python package for GUI named kivy. \*kv file should accompany the main app script. This document includes a set of instructions to give an insight into how to use the app. Each stage is explained thoroughly below.

1.  **Instructions**

![](media/a50e3217bf0081ecdcdd47058c90cc69.png)

**Welcome Screen:** The screen includes a preface and authors/contributors section. Users can interact with the navigation panel to proceed to the next page.

![](media/adf73f8643305969a8008fe3afde792f.png)

**Phase One:** Users need to tick both boxes to proceed to the next page. Then, IDF files included in the conversion process should be selected via the slider.

![](media/14223dff7cff76b878965ee57b1eb7ae.png)

**Phase Two:** Users need to fill out the boxes accordingly. Some examples can be given as:

First Box: TR, USA, PL, GER, IT…

Second Box: SFH, MFH, RT, HTL…

![](media/2cefe62ce8e05f9084a335b396ea7003.png)

![Graphical user interface Description automatically generated](media/bb97945d1c2f5280452ea31644644366.png)

**Phase Three:** Based on the selection in the first phase, users are prompted to load IDF files to the app. A popup file browser will be opened for file selection. Please select one file at a time.

![](media/052a04dcc9340f47410e6053755c1349.png)

**Phase Four:** The selected files will appear on top of the event panel. In order to be sure, users can check the base and alternative IDFs order. In order to define replaceme string, the first text input box is used. Users can define as many layers they desire. The latter should contain a specific keyword that best describes the specific layer characteristics in each file. To illustrate, some examples are given in Table 1.

| Replacer String   | Base IDF  | Alternative IDF 1 | Alternative IDF 2 | Alternative IDF 3 |
|-------------------|-----------|-------------------|-------------------|-------------------|
| -en-std-replaceme | -standard | -efficient        | -ZEB              | -energyPlus       |
| -chr-replaceme    | -1980     | -1990             | -2000             | -2010             |

**Table 1. Replacer and replace string examples**

![](media/dd8ece057d3df4bb4749eab359249561.png)

**Phase Five:** If desired, users can create a non-standard IDF by ticking the box. The non-standard version will be created by altering the base IDF’s performance-parameter values. It is required to select a save folder to conduct the conversion process. A popup screen will appear once the button is clicked.

![](media/ac14dc2d8b62628a5045bc60904da20e.png)

**Phase Six:** The first section of the event panel asks users to select whether a merged IDF file is requested, while the second section asks for user preferences about the export file format. Both YAML and xlsx can be selected at the same time.

![](media/063bf7696ff276486528984ebfccff4b.png)

**Final Summary:** The screen includes a summary, next steps, and caution sections specific to the conversion process. Users can terminate the app by clicking the Finish button.
