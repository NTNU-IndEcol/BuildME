# Brazilian office archetypes
Author: Kamila Krych
Date: December 15, 2023

This document describes three Brazilian office building archetypes, added to the BuildME framework under Latin America ("Oth-LAM"). The archetypes were created based on the publication of [Krych at el. (2021)](https://doi.org/10.5334/bc.136). The building archetypes in this publication are called Archetype I, II and III, and were created based on archetypes listed in a a national Brazilian standard NBR 12721 (ABNT, 2006): CSL-8, CSL-16 and CAL-8, respectively. These correspond to three BuildME archetypes: *CL-8, CL-16 and OPL-8*. The archetypes differ by floor layout (cellular vs. open plan), the number of floors (8 vs. 16), and a number of associated characteristics. 

The building footprint is 20 x 30 meters, with gross floor area of 4800 m2 for OfficeCL-8 and OfficeOPL-8 and 9600 m2 for OfficeCL-16.

## Main characteristics of the building archetypes

| Element | Construction |
|---------|--------------|
| External walls  | CL-8 and OPL-8: 2.5 cm plaster + 9 cm brick + 2.5 cm plaster|
| 		  | CL-16: 2.5 cm plaster + 13 cm brick + 2.5 cm plaster|
| Internal walls  | 2.5 cm plaster + 9 cm brick + 2.5 cm plaster|
| Roof            | 1.25 cm acoustic ceiling (incl. airspace) + 10 cm concrete + 6.1 cm airgap + 0.6 cm fibre cement roof tile|
| External floor  | 20 cm concrete + 0.5 cm carpet|
| Internal floor  | 1.25 cm acoustic ceiling (incl. airspace) + 10 cm concrete + 0.5 cm carpet|
| Glazing         | 0.6 cm glass with thermal resistance 5.782 W/(m2*K)|

Other information: 
- Internal loads schedule: from 6 AM to 6 PM on weekdays;
- Occupant density: 11 people/100 m2;
- Lighting use: 10.5 W/m2, equipment use: 14 W/m2;
- Mechanical ventilation: 7.5 liters/(s*person);
- Window-to-wall ratio: 70%;
- Solar heat gain coefficient: 0.6;
- Window opening effective area: 27% (the share of the window area opened when venting);
- Cooling setpoint: 24 degrees Celcius, heating setpoint: 20 degrees Celcius;
- No shading.
- Surrogate elements: default shear walls (concrete with 2% reinforcement), 20 cm foundation (concrete), columns of 30x30 cm every 3 m of the perimeter (concrete with 2% reinforcement).

## Energy standard
In BuildME, the energy standard aspect specifies the thickness of the insulation layer in the building's envelope elements (i.e., wall, roof, floor), the U-value (thermal transmittance) of the glazed surfaces, and the parameters describing the air infiltration. In a cooling-dominated country like Brazil, U-value of the building envelope is not of particular interest, and no insulation is added. The energy standard aspect in the Brazilian office archetypes is reflected only in the air infiltration levels, which were implemented using the AFN Converter (./tools/AFN Converter). 

## Resource efficiency scenario
The section "Main characteristics of the building archetypes" describes the building characteristics for the Brazilian building archetypes with the default resource efficiency scenario RES0. Other RES options are described below. Same construction types applies for all three building archetypes.

RES2.1 - the substitution scenario:
- External walls: the layer of brick reduced to 7 cm
- Internal walls: the layer of brick reduced to 7 cm
- Internal floor: the layer of concrete reduced to 5 cm + 17 cm of cross-laminated timber on top
- Surrogate columns: columns of 30x30 cm every 3 m of the perimeter (20% of concrete with 2% reinforcement, 80% wood)

RES2.2 - the lightweighing scenario:
- External walls: the layer of brick reduced to 7 cm
- Internal walls: the layer of brick reduced to 7 cm
- Internal floor: the layer of concrete reduced to 9 cm
- Surrogate columns: columns of 26.5x21.5 cm every 3 m of the perimeter (concrete with 2% reinforcement)

RES2.1+RES2.2 - the lightweighing and substitution scenario:
- External walls: the layer of brick reduced to 6 cm
- Internal walls: the layer of brick reduced to 6 cm
- Internal floor: the layer of concrete reduced to 4 cm + 17 cm of cross-laminated timber on top
- Surrogate columns: columns of 26.5x21.5 cm every 3 m of the perimeter (20% of concrete with 2% reinforcement, 80% wood)

## References
- ABNT. (2006). NBR 12721 Avaliação de custos de construção para incorporação imobiliária e outras disposições para condomínios edifícios. Associação Brasileira de Normas Técnicas. Retrieved from Associação Brasileira de Normas Técnicas website: https://www.abntcatalogo.com.br/norma.aspx?ID=62882
- Krych, K., Heeren, N., & Hertwich, E. G. (2021). Factors influencing the life-cycle GHG emissions of Brazilian office buildings. Buildings and Cities, 2(1), 856–873. https://doi.org/10.5334/bc.136

