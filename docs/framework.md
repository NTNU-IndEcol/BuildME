# BuildME framework
The framework consists of a simulation tool and batch simulation tool (incl. the aspect framework). Additionally, BuildME is flexible and can be adjusted (see [Adjusting the BuildME framework](#adjusting-the-buildme-framework)), e.g., to add new building archetypes or change the default BuildME aspects. Some optional tools exist to help users add new archetypes, e.g., IDF Converter. 

## Simulation tool
The BuildME simulation tool allows for combined material and energy demand simulations using the same underlying IDF file. The simulation can be performed for a standalone IDF file but also for a batch of buildings (see [Batch simulation tool and BuildME aspects](#batch-simulation-tool-and-buildme-aspects)).

### Energy demand simulation
Energy demand is calculated by EnergyPlus. In order to perform the simulation, two files need to be provided: IDF file with building-related data and EPW file with weather data. The calculations are initiated using the function `calculate_energy()` of the `simulate.py` file.

### Material demand simulation
Material demand is calculated directly in Python using an IDF file with building-related data . The calculations are initiated using the function `calculate_material()` of the `simulate.py` file. It is also possible to add surrogate elements that are not part of the IDF file, e.g., load-bearing beams and columns. These elements are optional and need to be provided using the dictionary ”surrogates dict” or the configuration file (for batch simulations). The surrogate material calculations are not performed unless requested through the parameter ”surrogate” of the function `calculate_material()`. 

For each surrogate element, the user needs to provide the information about the element geometry (e.g., width and length of the element), material types included in the element (e.g., [Concrete_surrogate, Reinforcement_surrogate]), shares of the material types (e.g., [0.98, 0.02]) and densities of the material types (e.g., [2400,7850]). Then the total surrogate volume is calculated and the total is split between material types and multiplied by their densities to obtain material mass. 

## Batch simulation tool and BuildME aspects
Batch simulations allow BuildME users to simulate numerous buildings at once using a systematic structure with BuildME aspects. The aspects allow to specify the characteristics of the combination of buildings that the user wishes to simulate. 

The default BuildME setup includes seven aspects: region, occupation, climate region, climate scenario, cooling type, energy standard and resource efficiency scenario (RES). BuildME is flexible and allows for adding or removing BuildME aspects (see [Adding or removing BuildME aspects](#adding-or-removing-buildme-aspects)).

### BuildME aspects: region and occupation
The aspects "Region" and "Occupation" serve to choose the building archetype, i.e., the IDF file that is used for running the simulation. For example, the IDF file "Office-CL8" defines an office building archetype that can be considered typical in Brazil and Latin America ("Oth-LAM" in the framework). The default version of the BuildME framework includes numerous residential and non-residential archetypes, however, more archetypes can be added (see [Adding new archetypes](#adding-new-archetypes)). The aspects "Region" and "Occupation" are required by the framework. 

### BuildME aspects: climate region and climate scenario
The aspects "Climate region" and "Climate scenario" serve to choose the weather data file, i.e., the EPW file that is used for running the energy demand simulation. Multiple climate regions can be defined for one "Region"; for example, the climate region "4A" in the USA correponds to the climate typical of the New York City. The aspect "Climate scenario" allows to choose between historical and future climate data. The aspects "Climate region" and "Climate scenario" are required by the framework. 

### BuildME aspects: cooling
The aspect "Cooling" allows to choose between conventional HVAC-based mechanical cooling and mixed-mode ventilation (MMV), which combines mechanical cooling with venting through windows for more realistic values of cooling loads. Read more in (see [afn-mmv.md](afn-mmv.md)). Cooling is an optional aspect - if not selected, the default (HVAC only) cooling system is used. 

### BuildME aspects: resource efficiency scenario

The aspect ”Resource efficiency scenario” (RES) reflects changes occurring in buildings due to material efficiency strategies. ”Resource efficiency scenario” is a replacement aspect, meaning that the IDF building file is modified to substitute the default values of chosen parameters with customized values. This is done automatically through the functions `apply_obj_name_change()` and `apply_rule_from_excel()`. For example, depending on the scenario, different types of constructions are used in the building. Resource efficiency scenarios may also influence surrogate material elements. The RES aspect includes four possible scenario options: 
- **RES0**: the default material choice;
- **RES2.1**: material substitution, where wooden elements substitute some structures made of concrete (e.g., external walls);
- **RES2.2**: downsizing, where the thickness of chosen construction layers is decreased;
- **RES2.1+RES2.2**: combined material substitution and downsizing.

### BuildME aspects: energy standard
The aspects "Energy standard" (en-std) is optional, and is another "replacement aspect".  BuildME includes four possible energy standards: 'non-standard', 'standard', 'efficient', and 'ZEB'. These four options determine the amount of building insulation in walls, roof, etc., the U-value (thermal transmittance) of glazed surfaces, and the parameters describing the air infiltration. 

The characteristics of the insulation layers and the glazed surfaces are defined on the archetype level. For the US building archetypes, the insulation layers have the following characteristics:
| Energy standard  | Material name   | conductivity λ | thickness d | transmittance U |
| ------------ | ----------------------- | -------------- | ----------- | --------------- |
| non-standard | `insulation_layer-2cm`  | 0.10           | 0.02        | 2.70            |
| standard     | `insulation_layer-12cm` | 0.04           | 0.12        | 0.33            |
| efficient    | `insulation_layer-16cm` | 0.04           | 0.16        | 0.24            |
| ZEB          | `insulation_layer-20cm` | 0.04           | 0.20        | 0.19            |

The infiltration levels are modeled using Airflow Network (AFN) objects in EnergyPlus. Although the infiltration level could be modeled differently, AFN objects are required for the MMV cooling (see [afn-mmv.md](afn-mmv.md)), so it is also included in the default cooling option for comparability reasons. Each energy standard corresponds to specific air mass flow parameter values for building elements such as external windows, external walls, internal walls, etc. The normalized values of parameters can be found in the file "afn-mmv-implementation.xlsx" in the folder "data"; they reflect the airtighness standards in Design Builder [DesignBuilder 2.1 User’s Manual](http://www.designbuildersoftware.com/docs/designbuilder/DesignBuilder_2.1_Users-Manual_Ltr.pdf), which in turn are based on empirical data presented by Orme et al. (1998) "Numerical Data for Air Infiltration and Natural Ventilation Calculations".

Each surface with cracks allowing for air flow has its own _AirflowNetwork:MultiZone:Surface_ object. In the field_ Leakage Component Name_, one specifies a name of either Crack or DetailedOpening object. Crack objects serve for surface types such as walls, floors, roofs etc. while DetailedOpening objects serve for doors and windows. 

Both Crack and DetailedOpening objects include fields called _Air Mass Flow Coefficient_ and _Air Mass Flow Exponent_. Depending on the airtightness standard and surface type, DesignBuilder uses different values for coefficients and exponents, as specified in the so-called crack templates. BuildME energy standards were mapped to DesignBuilder airtightness standards as seen in Table 1. 

**Table 1**: The mapping of BuildME energy standards to Design Builder airtightness standards.

|     BuildME energy standard    |     Design Builder airtightness standard      |
|--------------------------------|----------------------------------------------|
|     ZEB                        |     Excellent                                |
|     Efficient                  |     Good		                        |
|     Standard                   |     Medium                                   |
|     Non-standard               |     Poor                                     |

Please note that the two object types _AirflowNetwork:MultiZone:Surface:Crack_ and _AirflowNetwork:MultiZone:Component:DetailedOpening_ have different units for the air mass flow coefficient—kg/s and kg/s.m, respectively—and that the values for Crack objects are **not normalized**. Consequently, the coefficients used in the Crack objects need to be multiplied by the surface area. 

Adding AFN objects that allow for various infiltration levels can done automatically with the tool "AFN Converter" (see [Adding new archetypes](#adding-new-archetypes)). 

## Adjusting the BuildME framework

BuildME is flexible and allows for adding new building archetypes (occupation types) and adding or removing BuildME aspects. 

### Adding new archetypes

New archetypes can be added to the framework if the steps below are followed:
1. A new IDF file needs to be provided.
2. The configuration file needs to be adjusted. As a bare minimum, the sheet "combinations" needs to be modified to add the archetype to a list of possible occupation types in a chosen region. If a new region is introduced, it needs to be added in the "climate stations" sheet of the configuration file. 
3. If replacement aspects are to be included (e.g., energy standard or resource efficiency scenario), the IDF file needs to be modified. It can be done manually, by creating alternative construction names for various aspect values, e.g., alternatives for external wall "Construction" objects could be called "ext-wall-non-standard", "ext-wall-efficient", etc. The external walls surfaces defined in "BuildingSurface:Detailed" can then include the construction name "ext-wall-en-std-replaceme" and the string *-en-std-replaceme* will be replaced by, e.g., "efficient" once the simulation is started. This can also be done automatically using IDF Converter, which is a tool combining multiple IDF files into one with such replacement strings. 
4. Optionally, IdealLoads Converter tool might be used to modify the HVAC system in the building to a simplified one using the Ideal Loads Air System. This is required, e.g., for the mixed-mode ventilation system handling (see point below). 
5. Optionally, if the "Cooling" aspect is to be used, the building needs to be modified using the AFN converter. This tool adds Airflow Network objects in order to add infiltration values, which can then be automatically transformed into mixed-mode ventilation system if the "MMV" option is selected during BuildME execution. 

### Adding or removing BuildME aspects

Four BuildME aspects are required: region, occupation, climate region, climate scenario. The remaining aspects can be skipped if the user does not intend to use them and the underlying IDF files have not been converted yet. (The archetypes included in the framework *must* use the aspects "Energy standard" and "Resource efficiency scenario" or else the *replaceme* strings in the IDF file, e.g., -en-std-replaceme, will not be substituted by a correct construction name.)

Every extra aspect added to the framework will automatically be treated as a replacement aspect. The values will be replaced either directly based on the file "replace-\textit{aspect}.csv" located in the "data" folder or by detecting strings containing "-\textit{aspect}-replaceme" in the IDF file, where \textit{aspect} is the name of the replacement aspect. Such an extra replacement aspect can reflect, e.g., building cohort. If the user intends to add an extra aspect but not a replacement aspect, the code in batch.py needs to be manually edited to define the desired behavior of the software. 












