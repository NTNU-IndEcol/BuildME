# US building archetypes

The building archetypes for the US were created based on prototype building models defined by the U.S. Department of Energy (see [here](https://www.energycodes.gov/prototype-building-models)): 
- Single-family house (SFH.idf)
- Multifamily house (MFH.idf)
- Hospital (Hospital.idf)
- Large Hotel (HotelLarge.idf)
- Medium Office (OfficeMedium.idf)
- Stand-alone Retail (RetailStandalone.idf)
- Strip Mall (RetailStripmall.idf)
- Primary School (SchoolPrimary.idf)
- Secondary School (SchoolSecondary.idf)

The exception is the residential tower archetype (RT.idf), which was created by Andrea Nistad - see documentation in [RT.md](RT.md).

## Resource efficiency scenarios

The resource efficiency scenarios (RES) are implemented as follows: 
- `RES0`: The base variant. It is assumed that a concrete or brick construction is the base construction type.
- `RES2.1`: Material substitution or wood construction. Construction elements, such as roofs, walls, floors are replaced by post-beam walls from wood. Also insulation material layers are made from wood-based materials.
- `RES2.2`: Light-weighting or material efficiency. It is assumed that from the RES0 archetype most elements can be downsized by 20%. For example, a 20 cm concrete wall will be downsized to 16 cm.
- `RES2.1+RES2.2`: RES2.1 and RES2.2 are combined. A building mostly made from wood materials, while those material quantities are also reduced by 20%. However, post-beam elements are already very material efficient, this downsizing is not always possible. The insulation layer thickness is to be preserved and therefore no reduction is possible. Thus RES2.1+RES2.2 elements are often identical to RES2.1 elements.

## Energy standard 

The following insulation thicknesses apply for external wall surfaces:

| Energy standard  | Material name           | conductivity λ | thickness d |
| ---------------- | ----------------------- | -------------- | ----------- |
| non-standard     | `insulation_layer-8cm`  | 0.04           | 0.08        |
| standard         | `insulation_layer-12cm` | 0.04           | 0.12        |
| efficient        | `insulation_layer-16cm` | 0.04           | 0.16        |
| ZEB              | `insulation_layer-20cm` | 0.04           | 0.20        |

The following insulation thicknesses apply for external roof surfaces:

| Energy standard  | Material name           | conductivity λ | thickness d |
| ---------------- | ----------------------- | -------------- | ----------- |
| non-standard     | `insulation_layer-8cm`  | 0.04           | 0.08        |
| standard         | `insulation_layer-16cm` | 0.04           | 0.12        |
| efficient        | `insulation_layer-20cm` | 0.04           | 0.16        |
| ZEB              | `insulation_layer-30cm` | 0.04           | 0.20        |

The chosen archetypes contain standard-varying insulation layers on other surface types, e.g., floors. 