# Documentation on the AFN converter
Author: Kamila Krych

AFN converter can be used to convert an .idf file to one where infiltration is modeled using AirflowNetwork objects. This is part of the MMV procedure, so further details can be found in the MMV documentation file (see `/docs/mmv documentation.md`). All BuildME archetypes have been converted using the AFN converter to ensure that HVAC and MMV archetypes have the same infiltration levels. 

The original files (before the conversion) are available in the folder 'original'. The .idf files initially saved to folder `/tools/AFN Converter/` have been renamed and moved to folder `/data/archetype/USA/`. The content of the `/tools/AFN Converter/replace_mmv.xlsx` file have been pasted into the file `/data/replace.xlsx`.