# Documentation for Brazilian office building archetypes
_Kamila Krych, 04.11.2021_

The archetypes presented below are based on the publication "[Factors influencing the life-cycle GHG emissions of Brazilian office buildings](http://doi.org/10.5334/bc.136)". The publication describes most details, so here I present just a brief summary of the main characteristics. A separate section presents how some variables used in the study were assigned fixed values for the purpose of BuildME. 

## Main characteristics 
There are three archetypes, their main different being the height (8 vs. 16 floors) and floor layout (cellular vs. open). All three were based on building types defined by a Brazilian national standard NBR 12721 (ABNT 2006), with CSL-8, CSL-16 and CAL-8 corresponding to archetypes I, II and III, respectively. The archetypes are representative in the sense that they were created taking into account the current real estate market (Sinduscon-MG 2007). Together with [monthly updated material cost data](http://www.cub.org.br/cub-m2-estadual/BA/), the archetypes serve as a tool to estimate construction costs (Sinduscon-MG 2007).
The main design and operational features of the building can be seen in the table below taken from Krych et al. (2021):

| | ARCHETYPE I | ARCHETYPE II | ARCHETYPE III |
|---------|--------------------------------------------------------------|--------------------------------------------------------------|--------------------------------------------------------------|
| Number of floors                                      | 8                                                            | 16                                                           | 8                                                            |
| Floor layout                                          | Cellular                                                     | Cellular                                                     | Open                                                         |
| Building footprint (m)                                | 20 × 30                                                      | 20 × 30                                                      | 20 × 30                                                      |
| Gross floor area (m2)                                 | 4,800                                                        | 9,600                                                        | 4,800                                                        |
| Floor height (m)                                      | 2.8                                                          | 2.8                                                          | 2.8                                                          |
| Number of elevators                         | 2                                                            | 3                                                            | 2                                                            |
| External wall structure                               | 2.5 cm plaster + 9 cm brick + 2.5 cm plaster                 | 2.5 cm plaster + 9 cm brick + 2.5 cm plaster                 | 2.5 cm plaster + 13.5 cm brick + 2.5 cm plaster              |
| Internal wall structure                               | 2.5 cm plaster  + 9 cm brick  + 2.5 cm plaster               | 2.5 cm plaster  + 9 cm brick  + 2.5 cm plaster               | 2.5 cm plaster  + 9 cm brick  + 2.5 cm plaster               |
| Roof structure                                        | 10 cm concrete  + 6 cm air  + 0.6 cm fibre  cement roof tile | 10 cm concrete  + 6 cm air  + 0.6 cm fibre  cement roof tile | 10 cm concrete  + 6 cm air  + 0.6 cm fibre  cement roof tile |
| Floor structure internal                              | 1.25 cm acoustic ceiling  + 10 cm concrete  + 0.5 cm carpet  | 1.25 cm acoustic ceiling  + 10 cm concrete  + 0.5 cm carpet  | 1.25 cm acoustic ceiling  + 10 cm concrete  + 0.5 cm carpet  |
| Floor structure external                              | 20 cm concrete  + 0.5 cm carpet                              | 20 cm concrete  + 0.5 cm carpet                              | 20 cm concrete  + 0.5 cm carpet                              |
| Internal wall area per floor (m2)   | 179.9                                                        | 144.6                                                        | 40.2                                                         |
| Glazing thickness (mm)                         | 6                                                            | 6                                                            | 6                                                            |
| Glazing thermal transmittance (W/(m2.K))              | 5.782                                                        | 5.782                                                        | 5.782                                                        |
| Internal loads schedule                               | 6 AM to 6 PM on weekdays                                     | 6 AM to 6 PM on weekdays                                     | 6 AM to 6 PM on weekdays                                     |
| Occupant density (people/100 m2)                      | 11                                                           | 11                                                           | 11                                                           |
| Lighting use intensity (W/m2)                         | 10.5                                                         | 10.5                                                         | 10.5                                                         |
| Equipment use density (W/m2)                          | 14                                                           | 14                                                           | 14                                                           |
| Mechanical ventilation: fresh air intake (L/s/person) | 7.5                                                          | 7.5                                                          | 7.5                                                          |

Other information is available in the publication. 



## Assigning fixed values to variables
The study (Krych et al. 2021) included a number of variables within the building archetypes. Some of them are related to building design and operation, while others - to life-cycle greenhouse gas (GHG) emissions. The former group is the one of interest in here. It includes: window-to-wall ratio (WWR), solar heat gain coefficient (SHGC), window opening effective area, shading, and cooling set point. 

Of course, one may want to keep them as variables, the same as was done in the study (Krych et al. 2021). However, for the purpose of BuildME, all these variables have to be assigned a value. 

The choice of the values is certainly somehow subjective. In this case, I tried to best reflect the newest construction, in the hope that this will reflect future construction as well. In case one wants to reflect the existing stock, I encourage to look up the soruces cited below.

#### Window-to-wall ratio
The chosen value of WWR is 70%. According to a field study in Belo Horizonte, Brazil, WWR of 50% is the most common even among the buildings built within the last two decades (Alves et al. 2017). In their study of almost 250 Brazilian large offices, Lamberts et al. (2015) note that the typical WWR value is 70%. 
####  Solar heat gain coefficient
The chosen value of SHGC is 0.4. Alves et al. (2017) have used the value of 0.56 for representing the most recent office building archetype in Belo Horizonte built within the last two decades have SHGC of 0.56, based on a field study and other sources. I have decided to use 40% as it's what we get when rounding down to the nearest value used in Krych et al. (2021).
####  Window opening effective area
Window opening effective area is a variable that is only relevant for buildings with mixed-mode ventilation (MMV) system. This option has been implemented in BuildME (see [here](https://github.com/nheeren/BuildME/issues/14)). If MMV is used, window opening effective area is automatically set to 0.27, which was the value used by Neves et al. (2019). 
####  Shading
The chosen value of shading is 0%, meaning no external shading. This is supported by multiple studies which show that a big majority of offices (especially new construction) has no external shading such as window overhang or brise soleil (Alves et al. 2017, Neves et al. 2019, Tamanini Junior and Ghisi 2015).

####  Cooling set point
The chosen value of cooling set point is 23. This choice is associated with high uncertainty, because this value can be anywhere between 22 and 25. However, a study of almost 250 large office buildings in Brazil found that a setpoint of 22.5 is the most common (Lamberts et al. 2015).

## Potential application to other regions
The archetypes could be applied to other regions, but this should be done with caution. Some parameters might need adjustment, particularly the ones listed in the previous section, such as window to wall ratio, and cooling set point. Please keep in mind that the archetypes have the main structure made of reinforced steel, with brick walls covered with cement plaster. This archetype might not be representative for some countries, where the curtain wall archetype with WWR 100% might be predominant.

## References
- ABNT. (2006). NBR 12721-2006. Avaliação de custos de construção para incorporação imobiliária e outras disposições para condomínios edilícios. Associação Brasileira de Normas Técnicas (ABNT). https://www.abntcatalogo.com.br/norma.aspx?ID=62882  
- Alves, T., Machado, L., de Souza, R. G., & de Wilde, P. (2017). A methodology for estimating office building energy use baselines by means of land use legislation and reference buildings. Energy and Buildings, 143, 100–113. DOI: https://doi.org/10.1016/j.enbuild.2017.03.017  
- Krych, K., Heeren, N., & Hertwich, E. G. (2021). Factors influencing the life-cycle GHG emissions of Brazilian office buildings. Buildings and Cities, 2(1), 856–873. DOI: http://doi.org/10.5334/bc.136 
- Lamberts, R., Borgstein, E., Cursino, A., Schinazi, A., & De Dominicis, A. (2015). Benchmarking de escritórios corporativos e recomendações para certificação DEO no Brasil. Conselho Brasileiro de Construção Sustentável (CBCS). http://www.construcaospsustentavel.com.br/biblioteca/Madeira/deo_-_desempenho_energetico_operacional_em_edificacoes  
- Neves, L. O., Melo, A. P., & Rodrigues, L. L. (2019). Energy performance of mixed-mode office buildings: Assessing typical construction design practices. Journal of Cleaner Production, 234, 451–466. DOI: https://doi.org/10.1016/j.jclepro.2019.06.216
- Sinduscon-MG. (2007). Custo unitário básico (CUB/m2): Principais aspectos. Sinduscon-MG. http://www.cub.org.br/cartilha-cub-m2  
- Tamanini Junior, T., & Ghisi, E. Características construtivas de edifícios de escritório localizados em Florianópolis. XIII Encontro Nacional e IX Encontro Latino-americano de Conforto no Ambiente Construído.&nbsp;https://www.researchgate.net/publication/300003807_CARACTERISTICAS_CONSTRUTIVAS_DE_EDIFICIOS_DE_ESCRITORIO_LOCALIZADOS_EM_FLORIANOPOLIS-SC

