# Documentation Residential Tower Archetype 
*Andrea A. Nistad, 15. July 2020*
*update: Kamila Krych, 12. Dec 2023*

The residential tower archetype model is intended to represent urban residential buildings. The model is based on the DOE prototype high-rise model (available from: 
https://www.energycodes.gov/development/commercial/prototype_models).  

The original prototype model has 10 floors but is adapted to 30 floors to represent typical residential towers found in large Asian cities/China etc. In China, residential high-rise buildings have a typical height of 18 to 33 (Jiang et al., 2019; Kuilen et al., 2011; Li and Li, 2015; Peng et al., 2020; Wan and Yik, 2004).

## Shape, building design, structural design etc.
The building shape is kept equal to the DOE model. Regarding the shape, Foraboschi et al. (2014) notes that the slenderness ratio of buildings between 20 and 80 floors are typically 5 to 7. The archetype developed is 46 m x 17 m, about 90 m tall. The resulting slenderness ratio is about 5.3.
The window-to-wall ratio is modified from 30% in the DOE prototype model to 15% in all directions.
 The assumption is based on a statistical investigation of residential towers in the Pearl Delta region (Peng et al., 2020).

The residential tower is a reinforced concrete structure. Taller buildings require a different structural design to both account for the effect on increased self-weight and increased lateral loads. Typical structures for 20-40 floors buildings is composed of flat slabs, columns and shear or core walls (Ali and Moon, 2007; Foraboschi et al., 2014; Taranath, 2010). In China, the mainstream building structure from 1949 to 2015 is brick-concrete and steel-concrete (Yang et al., 2020). Reinforced concrete structures are typically used in buildings more than 7 stories tall (Guo et al., 2019). In China, more than 90 % of the high-rise buildings are reinforced concrete structures (K and Wing, 2005).

The RT is modeled using zone multipliers, meaning that only the first, last and two middle floors are modeled. This simplifies modeling of high-rise buildings and still yield acceptable accuracy of simulation results (Chen and Hong, 2018; Ellis and Torcellini, n.d.)

The heating and cooling setpoint is modified compared to the prototype DOE high-rise building. The cooling set point is set to 26 C. The heating set point is modified to 22.22 C, as for the MFH and SFH. Exterior blinds are also added to the model, and will be used if the outside temperature reaches 25 C.

The model is then modified according to different energy standards and resource efficiency strategies.

## Energy standards

Different energy standards are modeled by changing insulation levels and ACH.

The thickness of insulation layers in external walls and roofs depend on the energy standard. The same thickness as used for the MFH and SFH is applied (see documentation on these archetypes).

## Resource efficiency strategy

### RES0: Reinforced concrete residential tower

The following assumptions are made for the structural design:

| Element                | Construction                                                                                                                                                                                                                                                                                                                                                                                    |
|------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|     External walls     | 25 mm stucco                                                                                                                                                                                                                                                                                                                                                                                    |
|                        | 150 mm concrete                                                                                                                                                                                                                                                                                                                                                                                 |
|                        | 1% reinforcement ratio                                                                                                                                                                                                                                                                                                                                                                          |
|                        | Insulation (depending on energy standard, same thickness as for MFH and SFH)                                                                                                                                                                                                                                                                                                                    |
|                        | 16mm gypsum board                                                                                                                                                                                                                                                                                                                                                                               |
| Roof                   | Concrete tiles                                                                                                                                                                                                                                                                                                                                                                                  |
|                        | 20 mm bitumen                                                                                                                                                                                                                                                                                                                                                                                   |
|                        | 25 mm cement                                                                                                                                                                                                                                                                                                                                                                                    |
|                        | 150 mm concrete                                                                                                                                                                                                                                                                                                                                                                                 |
|                        | Insulation (depending on energy standard, same thickness as for MFH and SFH)                                                                                                                                                                                                                                                                                                                    |
|                        | 13 mm gypsum board                                                                                                                                                                                                                                                                                                                                                                              |
| External floor         | 200 mm concrete                                                                                                                                                                                                                                                                                                                                                                                 |
|                        | 1% reinforcement ratio                                                                                                                                                                                                                                                                                                                                                                          |
|                        | Insulation (same as for MFH and SFH)                                                                                                                                                                                                                                                                                                                                                            |
|                        | Interior finish                                                                                                                                                                                                                                                                                                                                                                                 |
| Internal floor         | Flat slab                                                                                                                                                                                                                                                                                                                                                                                       |
|                        | 200 mm concrete                                                                                                                                                                                                                                                                                                                                                                                 |
|                        | 150 kg/m3 of reinforcement, 2% reinforcement (Veljkovic, 2016, p. 311)                                                                                                                                                                                                                                                                                                                          |
|                        | 13 mm gypsum board                                                                                                                                                                                                                                                                                                                                                                              |
| Internal walls         | 120 mm concrete                                                                                                                                                                                                                                                                                                                                                                                 |
|                        | 1% reinforcement                                                                                                                                                                                                                                                                                                                                                                                |
|                        | 13 mm gypsum board (remove?)                                                                                                                                                                                                                                                                                                                                                                    |
| Columns                | Columns placed along building perimeter with 9 m spacing between (Kim et al., 2008; Taranath, 2010)                                                                                                                                                                                                                                                                                             |
|                        | 950mm x 750 mm reinforced concrete (assume that this is the average column size of the building, in theory the column size is reduced towards the upper floors) (Taranath, 2010, p.219). This equals about 840mmx840mm                                                                                                                                                                          |
|                        | 200 to 250 kg/m3 of reinforcement (Foraboschi et al., 2014; Ma et al., 2000) -> 2,5%-3% reinforcement ratio                                                                                                                                                                                                                                                                                     |
| Shear walls/core walls | 450 mm reinforced concrete assumed (Taranath, 2010, p.218)                                                                                                                                                                                                                                                                                                                                      |
|                        | 150 kg/m3 of reinforcement (~6% reinforcement) (Foraboschi et al., 2014)                                                                                                                                                                                                                                                                                                                                            |
                                                                                                                                                                                  |
| Foundations            | Assume deep pile foundation or raft foundation.                                                                                                                                                                                                                                                                                                                                                 |
|                        | Based on a review of literature the concrete intensity of foundations seems highly variable. For the buildings data are available from (10+ floors), concrete intensity is 0.25 to 1.68 m3 concrete per m2 footprint area. Steel intensity is in the range of 65-150 kg steel per m3 concrete. The average values of 0.6 m3 concrete per m2 footprint and 100 kg steel per m3 concrete (~4% reinforcement) is used. |
| Basement               |     Assume two levels of   basements                                                                                                                                                                                                                                                                                                                                                            |
|                        | 200 mm reinforced concrete walls and slabs with approx. 100 kg/m3 of reinforcement (~4% reinforcement)                                                                                                                                                                                                                                                                                                           |

The figure below is used as a rough guideline to doublecheck the assumptions for slab thickness, column size and span, taken from (Allen and Iano, 2006, p.125). For heavy loads column size should be increased by 50 to 100 mm. Columns assumed for RES0 is about 840mmx840mm, span is 9m and slab thickness is 200mm. Hence, columns and span are fairly within expected ranges, while the slab thickness is a bit lower (200 mm instead of ~300 mm).


### RES 2.1: Wooden version

The wooden version of the 30 floor RT is based on the design of the Tall Wood student resident by UBS Brooks Commons in Vancouver (Athena, 2018).

This 18 floors hybrid wood-concrete construction is currently the world&#39;s tallest timber-based construction. The design is anticipated to be feasible to extend to 30-40 floors too (see [https://dailyhive.com/vancouver/1745-west-8th-avenue-vancouver-canada-earth-tower](https://dailyhive.com/vancouver/1745-west-8th-avenue-vancouver-canada-earth-tower), Rolf Andr� Bohne, personal communication may 2020).

The building is designed with CLT floor slabs, wooden columns and high-pressure laminate on the external wall surfaces, in addition to a thick concrete core around the elevator shaft for lateral load resistance. Hybrid construction systems are typically used for high-rise timber buildings as a solely timber based construction is too light, and do not serve the sufficient sound and fire requirements (Rolf Andr� Bohne, personal communication may 2020)

The following assumptions regarding the structural design is made and is based on the design of UBS Brooks Commons Tall Wood House:

| Element                | Construction                                                                                                                      |
|------------------------|-----------------------------------------------------------------------------------------------------------------------------------|
|     External walls     | High pressure laminate panels                                                                                                     |
|                        | Insulation layer (same as for MFH and SFH, see doc)                                                                               |
|                        | 16 mm gypsum board                                                                                                                |
|                        | Lightweight steel studs (added as a surrogate element with 5x10 cm, 3m long, every 0.4 m)                                         |
| Roof                   | 20 mm bitumen                                                                                                                     |
|                        | Insulation layer (same as for MFH and SFH, see doc)                                                                               |
|                        | OSB_5/8in                                                                                                                         |
|                        | Metal surface                                                                                                                     |
|                        | Steel beams                                                                                                                       |
| External floor         | Interior finish                                                                                                                   |
|                        | Insulation layer (same as for MFH and SFH, see doc)                                                                               |
|                        | 120 mm Reinforced concrete slab                                                                                                   |
| Internal floor         | 13 mm gypsum board                                                                                                                |
|                        | 50 mm Concrete                                                                                                                    |
|                        | 170 mm CLT                                                                                                                        |
|                        | Second floor is 600 mm reinforced concrete slab                                                                                   |
| Internal walls         | Lightweight steel studs (modeled as 5mm-thick sheet) with 16 mm gypsum board on both sides                                        |
| Columns                | Exterior and interior columns with 3 m spacing                                                                                    |
|                        | 300x300 mm glulam (floor 3 – 30)                                                                                                  |
|                        | 500x500 mm reinforced concrete columns (floor 1-2), same reinforcement ratio as for RES0                                          |
| Shear walls/core walls | Same as for RES0, no changes                                                                                                      |
| Foundations            | Same as for RES0, no changes                                                                                                      |
| Basement               | Same as for RES0, no changes                                                                                                      |

### RES2.2: Lightweighting reinforced concrete building

- Interior walls reduced from 120 mm to 100 mm reinforced concrete
- Basement walls reduced from 200 mm to 150 mm reinforced concrete
- Exterior walls reduced from 150 mm to 120 mm reinforced concrete
- Interior floor slabs reduced from 200 mm to 175 mm reinforced concrete

###

### RES2.1+RES2.2: Lightweight wood building

Make the following changes to the model described in RES2.1:

- Reducing the thickness of the concrete layer on top of CLT floor slabs from 50 mm to 40 mm
- Reducing the size of steel beams for the roof from 250x250mm to 200x200mm
- Reducing size of wood columns from 300x300mm to 265x215mm (as in Tallwood House)

### Validation of model results

#### RES0: Reinforced concrete structure

See new pull request in GitHub repo
 on material intensity database (https://github.com/nheeren/material\_intensity\_db](https://github.com/nheeren/material_intensity_db) for the new datapoints added for buildings with more than 20 floors.

The two datapoints from Chen et al. (2001) describe public residential buildings with 40 floors in Hong Kong but produce a very low concrete intensity 150-180 kg/m2. A newer study by Yim et al. (2018) describe the same type of public residential building in Hong Kong (but a newer edition) and report a concrete intensity of 2077.44 kg/m2, 174.85 kg/m2 steel and 2.5 kg/m2 wood.

Model by Foraboschi et al. (2014) indicate for a model reinforced concrete building of 30 floors a steel intensity of 43.35 kg/m2 and 1373 kg concrete per m2 floor area for the structural frame and core. Kim et al. (2008) indicate 65 kg/m2 and 1272 kg concrete per m2 floors area for the structural model of a 40 storey reinforced concrete building.

From material intensity database, MI in kg/m2:

|                              |     20-30 floors     *only 4 datapoints!    |     30-40 floors     *only 4 datapoints! excluding Chen et al. (2001))    |     30-40 floors      *incl. Chen et al. (2001)    |
|------------------------------|---------------------------------------------|---------------------------------------------------------------------------|----------------------------------------------------|
|     Steel                    |     89                                      |     135                                                                   |     137                                            |
|     Concrete                 |     1346                                    |     1608                                                                  |     1129                                           |
|     Cement                   |     51                                      |     57                                                                    |     57                                             |
|     Wood                     |     19.9                                    |     1.3                                                                   |     1.33                                           |
|     Paper   and cardboard    |                                             |                                                                           |                                                    |
|     Other                    |                                             |                                                                           |                                                    |

The material intensity obtain is also well in line with recent studies on material use in urban Chinese buildings by Guo et al. (2019) and Yang et al. (2020). 

#### RES2.1: Wooden version
The material intensity for wooden high-rise buildings collected are shown below (see Dropbox docs for details):

|     Building                                             |     Stories     |     Floor area    |     Wood        |     Concrete     |     Steel       |
|----------------------------------------------------------|-----------------|-------------------|-----------------|------------------|-----------------|
|     Mjøstårnet                                           |     18          |     11300         |     107.1814    |     534.3717     |     34.05522    |
|     Treet                                                |                 |     3780          |     109.7476    |     59.04762     |     20.7672     |
|     Hypothetical building, Skullestad et   al. (2016)    |     21          |     11823         |     198.036     |     145.7498     |     7.866024    |
|     Sweden, 8 floors timber                              |     8           |     3375          |     148.0741    |     449.8865     |     21.10933    |
|     Brock Commons Tallwood                               |     18          |     840           |     67.31446    |     524.8447     |     31.34645    |
|     HoHo                                                 |                 |     25000         |     78          |     132          |                 |
|     Mean                                                 |                 |                   |     118.1089    |     307.629      |     23.02884    |
|     Median                                               |                 |                   |     108.4645    |     297.8182     |     21.10933    |

The effect of RES on energy use shows, like MFH and SFH, that the wooden version has about 3-4% increase in thermal energy demand compared to the reinforced concrete building.

# References

Ali, M.M., Moon, K.S., 2007. Structural Developments in Tall Buildings: Current Trends and Future Prospects. Architectural Science Review 50, 205�223. https://doi.org/10.3763/asre.2007.5027

Allen, E., Iano, J., 2006. The Architect&#39;s Studio Companion: Rules of Thumb for Preliminary Design. John Wiley &amp; Sons.

Athena, 2018. Environmental Declaration Tallwood House.

Chen, Y., Hong, T., 2018. Impacts of building geometry modeling methods on the simulation results of urban building energy models. Applied Energy 215, 717�735. https://doi.org/10.1016/j.apenergy.2018.02.073

Ellis, P.G., Torcellini, P.A., n.d. Simulating Tall Buildings Using EnergyPlus: Preprint 12.

Foraboschi, P., Mercanzin, M., Trabucco, D., 2014. Sustainable structural design of tall buildings based on embodied energy. Energy and Buildings 68, 254�269. https://doi.org/10.1016/j.enbuild.2013.09.003

Guo, J., Miatto, A., Shi, F., Tanikawa, H., 2019. Spatially explicit material stock analysis of buildings in Eastern China metropoles. Resources, Conservation and Recycling 146, 45�54. https://doi.org/10.1016/j.resconrec.2019.03.031

Jiang, B., Li, H., Dong, L., Wang, Y., Tao, Y., 2019. Cradle-to-Site Carbon Emissions Assessment of Prefabricated Rebar Cages for High-Rise Buildings in China. Sustainability 11, 42. https://doi.org/10.3390/su11010042

K, C.Y., Wing, C.K., 2005. Tall Buildings: From Engineering To Sustainability. World Scientific.

Kim, S.B., Lee, Y.H., Scanlon, A., 2008. Comparative study of structural material quantities of high-rise residential buildings. The Structural Design of Tall and Special Buildings 17, 217�229. https://doi.org/10.1002/tal.348

Kuilen, J.W.G.V.D., Ceccotti, A., Xia, Z., He, M., 2011. Very Tall Wooden Buildings with Cross Laminated Timber. Procedia Engineering, The Proceedings of the Twelfth East Asia-Pacific Conference on Structural Engineering and Construction 14, 1621�1628. https://doi.org/10.1016/j.proeng.2011.07.204

Li, Y., Li, X., 2015. Natural ventilation potential of high-rise residential buildings in northern China using coupling thermal and airflow simulations. Build. Simul. 8, 51�64. https://doi.org/10.1007/s12273-014-0188-1

Ma, G., Hao, H., Zhou, Y., 2000. Assessment of structure damage to blasting induced ground motions. Engineering Structures 22, 1378�1389. https://doi.org/10.1016/S0141-0296(99)00072-3

Peng, H., Li, M., Lou, S., He, M., Huang, Y., Wen, L., 2020. Investigation on spatial distribution and thermal properties of typical residential buildings in South China&#39;s Pearl River Delta. Energy and Buildings 206, 109555. https://doi.org/10.1016/j.enbuild.2019.109555

Taranath, B.S., 2010. Reinforced concrete design of tall buildings. CRC press.

Veljkovic, M., 2016. Sustainable Steel Buildings: A Practical Guide for Structures and Envelopes. John Wiley &amp; Sons.

Wan, K.S.Y., Yik, F.W.H., 2004. Building design and energy end-use characteristics of high-rise residential buildings in Hong Kong. Applied Energy 78, 19�36. https://doi.org/10.1016/S0306-2619(03)00103-X

Yang, D., Guo, J., Sun, L., Shi, F., Liu, J., Tanikawa, H., 2020. Urban buildings material intensity in China from 1949 to 2015. Resources, Conservation and Recycling 159, 104824. https://doi.org/10.1016/j.resconrec.2020.104824

Yim, S.Y.C., Ng, S.T., Hossain, M.U., Wong, J.M.W., 2018. Comprehensive Evaluation of Carbon Emissions for the Development of High-Rise Residential Building. Buildings 8, 147. https://doi.org/10.3390/buildings8110147

