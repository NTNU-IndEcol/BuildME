# Archetype description

BuildME comes with a number of archetypes in the `./data/archetype` folder. They are organised by country and occupation / type. In `settings.py` it can be specified if archetypes serve as a proxy for other regions.

## Creating new archetypes

In order to introduce new IDF files as archetypes in BuildME the following should be considered:

- Energy standard. The building components `BuildingSurface:Detailed` must refer to a `Construction` that ends with the name `-en-std-replaceme`. This will then be replaced with the energy standard keywords (non-standard, standard, efficient, ZEB). For instance, `attic-ceiling-en-std-replaceme` will be converted to `attic-ceiling-non-standard`, `attic-ceiling-standard`, etc. Of course this also means that all of these `Construction` elements must also be present in the IDF file.

- Resource Efficiency Strategy (RES). The same applies for the RES. The `-res-replace` string will be replaced with RES0, RES2, RES2.1, RES2.2, or RES2.1+RES2.2.

- Energy standard and RES are permutated and therefore each combination must be present in the IDF file. For example, `ext-floor-en-std-replaceme-res-replaceme` will be translated into ext-wall-non-standard-RES0, ext-wall-standard-RES0, ..., ext-wall-ZEB-RES2.1+RES2.2.

- Further replacements can be controlled in the `./replace.xlsx` file.
*TODO*



## Rationale

Guidelines that were used to determine the scenarios and manipulating the archetypes.

### Resource Efficiency Strategies RES

Currently three Resource Efficiency Strategies (RES) are implemented. 

- `RES0`: The base variant. It is assumed that a concrete or brick construction is the base construction type.
- `RES2.1`: Material substitution or wood construction. Construction elements, such as roofs, walls, floors are replaced by post-beam walls from wood. Also insulation material layers are made from wood-based materials.
- `RES2.2`: Light-weighting or material efficiency. It is assumed that from the RES0 archetype most elements can be downsized by 20%. For example, a 20 cm concrete wall will be downsized to 16 cm.
- `RES2.1+RES2.2`: RES2.1 and RES2.2 are combined. A building mostly made from wood materials, while those material quantities are also reduced by 20%. However, post-beam elements are already very material efficient, this downsizing is not always possible. The insulation layer thickness is to be preserved and therefore no reduction is possible. Thus RES2.1+RES2.2 elements are often identical to RES2.1 elements.

### Thermal insulation layer

$U = 1/R_T = \frac{1}{R_{se}+d_1/\lambda_{1}+...+d_n/\lambda_{n}+R_{si}}$

Interior and exterior thermal resistance for walls are $R_{si}=0.13$, $R_{se}=0.04$, but not considered here.

The following insulation thicknesses apply for RES0 (the baseline Resource Efficiency scenario).

|                         | conductivity λ | thickness d | transmittance U |
| ----------------------- | -------------- | ----------- | --------------- |
| `insulation_layer-2cm`  | 0.10           | 0.02        | 2.70            |
| `insulation_layer-12cm` | 0.04           | 0.12        | 0.33            |
| `insulation_layer-16cm` | 0.04           | 0.16        | 0.24            |
| `insulation_layer-20cm` | 0.04           | 0.20        | 0.19            |

For RES2.1 (material substitution / wood construction) and RES 2.1+RES2.2 (material substitution+light-weighting) the same characteristics are applied, but the names are changed to insulation_layer-wood-2cm, insulation_layer-wood-12cm, etc.

The RES2.2 uses the same insulation materials as RES0.

## `HotelLarge` archetype

| int-floor    | RES0                                                         | RES2.1 | RES2.2 | RES2.1+RES2.2 |
| ------------ | ------------------------------------------------------------ | ------ | ------ | ------------- |
| non-standard | Nonres_Floor_Insulation-non-standard-RES0<br />100mm Normalweight concrete floor<br />CP02 CARPET PAD |        |        |               |
| standard     |                                                              |        |        |               |
| efficient    |                                                              |        |        |               |
| ZEB          |                                                              |        |        |               |

