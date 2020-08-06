## Documentation (high-rise) office buildings 
*Andrea Nistad, 06.08.2020*

The high-rise office building prototype is developed based on the large office building described by DOE prototype commercial buildings . 
This prototype is representative for office buildings in the US and is a RC structure. 
Additionally, an archetype for high-rise office buildings in India is obtained from Bhatnagar et al. (2019), which yields a brick masonry version of a geometrically similar office building. 

**RC high-rise office building (representative for USA):**   
The archetype is developed based on the large office buildings from DOE. This is a 12 floor office building, with one basement level and a data center. The building measures 48 x 73 m. 
The data center is removed and replaced with a regular office to represent a more generic office globally. The HVAC system is also modified and replaced by HVACtemplate:IdealLoadsAirSystem, as the heating and cooling demand is the (current) output values from BuildME.
The cooling and heating setpoint are 24 C and 21 C respectively. Other details regarding the energy modeling is available in the idf file. 

Structural:

The building envelope is kept as defined in the original prototype model. External walls and floor slabs are reinforced concrete. 
The reinforcement ratio of the reinforced concrete is assumed to be 2% (as referred by Bhatnagar et al. (2019) for a similar office building in India). The “Built-up roofing” for the roof is replaced by a 150 mm reinforced concrete slab. In addition to the structures described in the idf file, interior walls, a foundation and perimeter columns are added to the model. The dimensions of the foundation and perimeter columns are assumed equal to the RT archetype.

Currently no RC beams are added to the model. 
Interior walls are assumed to be gypsum boards (as this defined in the DOE prototype). However, the interior walls may potentially
be modified to concrete walls. 

Energy standards: 

Currently, only the standard building is modeled. U-values for exterior walls, roof and exterior floor slab is based on IECC 2009 for office buildings in climate zone 4 (New York)   
The following U-values are used:   
Wall: 0.57 W/m2K  
Roof: 0.27 W/m2K  
Floor: 1.35 W/m2K  
Windows: 2.9 W/m2K  
While the infiltration value is set to 0.4 1/h (increase?)  


**Brick masonry high-rise office building (representative for India):**  
The high-rise office archetype for India is described in Bhatnagar et al. (2019). The building described is a rectangular 9 floors office building. The shape, height and WWR of this building is similar to the USA archetype, hence the shape, WWR and number of floors is kept constant. Materials, insulation levels, internal loads and occupancy are however changed. Both a building with 24- and 8-hour operation is described in Bhatnagar et al. (2019), but only the 8-hour operation is implemented. 

Structural:  
External and interior walls are brick walls, while the roof and exterior slab are reinforced concrete. The thickness of the exterior walls are 203 mm. The reinforcement ratio is 2%. Reinforced concrete beams and columns are common structural elements for office buildings in India (personal communication, Bhatnagar, 6 July 2020). 
As for the USA high-rise office archetype, a foundation and vertical columns with same specifications as for the RT is added to the model. 
No RC beams are added to the model, as the dimensions and reinforcement are unknown. 

Energy standards:   
Only a building with the standard energy efficiency level is modeled yet. The thermal properties of the envelope are defined based on the idf files (for Lucknow, largest share of commercial stock) provided by Bhatnagar et al. (2019).  
U-values are:  
Wall: 0.83 W/m2K  
Roof: 0.75 W/m2K  
Floor: 1.354 W/m2K  
Infiltration is set to 0.4 1/h as for the large office prototype from the US  


**References**   
Bhatnagar, M., Mathur, J., Garg, V., 2019. Development of reference building models for India. Journal of Building Engineering 21, 267–277. https://doi.org/10.1016/j.jobe.2018.10.027

DOE prototype models 
https://www.energycodes.gov/development/commercial/prototype_models
