# Procedures of BuildME

## Energy model

Energy demand is calculated by energyplus.

### Manipulation of energyplus files

That means much of the scenarios are applied by means of manipulation of the energyplus files.

#### Energy standard

The current model knows four energy standards, which may differ per region: 'non-standard', 'standard', 'efficient', and 'ZEB'. In order to change the energy standard of a given IDF archetype, the following changes are made to the base IDF file:

**Ventilation**

*TBD*

**Walls**

The following components exist:

- `ext_wall-non-standard`

- `ext_wall-standard`
- `ext_wall-efficient`
- `ext_wall-ZEB`

