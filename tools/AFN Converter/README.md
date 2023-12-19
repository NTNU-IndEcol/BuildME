# Documentation on the AFN converter
Author: Kamila Krych

AFN converter can be used to convert an .idf file to one where infiltration is modeled using AirflowNetwork objects. The infiltration levels are automatically modeled according to Design Builder airtightness standards which serve to reflect BuildME energy standards (see ./docs/framework.md).

The AFN converter was created as part of the MMV procedure, so further details can be found in the MMV documentation file (see `/docs/mmv.md`). 

All archetypes integrated into BuildME have been converted using the AFN converter to ensure that HVAC and MMV archetypes have the same infiltration levels. The original files (before the conversion) are available in the folder 'original'. The .idf files initially saved to folder `/tools/AFN Converter/` have been renamed and moved to folder `/data/archetype/USA/`. The content of the `/tools/AFN Converter/replace_mmv.xlsx` file have been pasted into the file `/data/replace-en-std.csv`.