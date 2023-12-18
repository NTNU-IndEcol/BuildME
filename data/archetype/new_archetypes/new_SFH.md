## Documentation new residential archetypes
*Andrea A. Nistad, 5.8.2020*

With the BuildME-paper in mind, new residential archetypes have been implemented to BuildME. 

From the main documentation: "Based on the insights and data from the PAGER building inventory data set/IEA report and the WHE database some gaps in our archetype modeling were identified and should be improved to have a better representation of the building stock before continuing  analysis for the paper dedicated to the investigation of the future global building stock."

It is suggested to include one masonry version of the existing SFH and MFH, and implement a smaller SFH with 
three different material options: masonry, RC and wood. Under follows a short documentation of the 
archetypes implemented.

**SFH-MASONRY:** 
-	Exterior walls changed from RC to fired clay brick masonry of 300 mm 
*Thickness of brick wall determined based on SFH in moderate EU climate (SFH_moderate_1990-2010) indicated by (Lavagna et al., 2018), brick masonry archetypes for India (Mastrucci and Rao, 2017) and WHE. The brick material data is taken from the ASHRAE handbook and assume a density of 1920 kg/m3.*
-	Exterior floor slab kept as RC 
*Assumption based on WHE, Lavagna et al. (2018) and Mastrucci and Rao (2017)*
-	Roof structure kept as pitched roof with same construction materials as for RECC SFH
*In warmer climates the roof is often a RC slab instead of pitched roof (Lavagna et al., 2018; Mastrucci and Rao, 2017), while for moderate climates the roof construction is often similar to the existing RECC SFH roof construction (TABULA database)*
-	Interior walls are kept as drywall as for the existing SFH
*Lavagna et al. (2018) indicate wood and plasterboard as typical interior wall materials used in SFH modern masonry buildings in moderate EU climate. In warmer climates, the interior walls are maybe more likely to be brick infill.*

-	In addition, the surrogate basement and surrogate steel beams are still added 
*Would have to check if a basement should be included or not. Adding the steel beams result in steel intensity values higher than calculated by the material intensity database..*

**MFH-MASONRY:**
- Exterior walls changed from RC to fired clay brick walls of thickness 200 mm
*Thickness based on Lavagna et al. (2018) and WHE. Lavagna et al. (2018) indicate 20 cm hollow brick for exterior walls for MFH with RC frame. WHE indicate 100 mm to 300 mm (average of 180 mm approx.) for confined masonry.* 
-	Floors changed to RC slabs of thickness 150 mm 
*Typically reinforced concrete floor slabs according to WHE and Lavagna et al. (2018). 100 to 150 mm RC slab common for confined masonry*
-	Pitched roof is replaced with a flat RC roof slab of 150 mm 
*Assumption based on masonry MFH in WHE and (Lavagna et al., 2018; Mastrucci and Rao, 2017).* 
-	Interior walls of 200 mm brick with plastering on each side instead of RC interior walls
*Assumption based on Lavagna et al. (2018)*

-	The surrogate basement and steel beams are still added to the model as for the existing MFH. 
*As per now, the surrogate steel beams are added to the model. However, masonry MFHs typically have RC frame structure (Lavagna et al., 2018; Mastrucci and Rao, 2017, WHE). Dimensions of columns and beams are determined based on housing report nr. 62 and 64 in WHE and Mastrucci and Rao (2017), and results in columns of 400x400 mm and beams of 300x500 mm with span of 4 m. But is seems like this assumption will underestimate the steel content..* 

**SFH-SMALL-MASONRY:**
-	Exterior walls of 230 mm fired clay bricks
*Assumption based on the unreinforced masonry houses in WHE. Brick material specifications from ASHRAE material dataset. Assume a brick density of 1600 kg/m3, for reference (Mastrucci and Rao, 2017) assume brick density of 1700 kg/m3.* 

-	Roof consisting of timber trusses with metal sheeting 
*Assumption based on unreinforced and confined masonry, single-storey houses described in WHE. Several studies describe a roof construction of timber trusses with either tiles (Mastrucci et al., 2019; Paulsen and Sposto, 2013; Utama et al., 2012) or metal sheeting (Niwamara et al., 2016; Soust-Verdaguer Bernardette et al., 2018).* 

-	RC floor slab with thickness of 100 mm 
*Assumption based on WHE and building descriptions in literature (Mastrucci and Rao, 2017; Muringathuparambil et al., 2017; Oyarzo and Peuportier, 2014; Paulsen and Sposto, 2013)*

-	Interior walls of 102 mm clay brick with plaster on each side
*Assumed based on building descriptions of low-income dwellings in India (Nutkiewicz et al., 2018) and South-Africa (Muringathuparambil et al., 2017)*

**SFH-SMALL-CONCRETE:**
-	Exterior walls of 150 mm concrete 
*Assumed thickness of concrete walls to be the same as for the RECC SFH and MFH in RC*

-	RC floor slab with thickness of 100 mm 
*Assumption based on WHE and building descriptions in literature (Mastrucci and Rao, 2017; Muringathuparambil et al., 2017)*

-	RC roof slab with thickness of 150 mm, instead of timber and metal sheeting 
*Assumption based on WHE. Thickness of 120 mm roof slab in (Mastrucci and Rao, 2017)*

-	Interior walls of 102 mm clay brick with plaster on each side
*Assumed based on building descriptions of low-income dwellings in India (Nutkiewicz et al., 2018) and South-Africa (Muringathuparambil et al., 2017)*

**SFH-SMALL-WOOD:**
-	The exterior walls have 15 mm wooden boards as the main material layer
*Have assumed the same exterior walls as in RECC SFH and MFH in the wooden resource efficiency scenario RES2.1. Wooden boards are also the exterior wall material highlighted in WHE*

-	Roof composed of timber trusses/rafters with metal sheeting 
*Assumption based on wooden buildings description in WHE, as well as Soust-Verdaguer Bernardette et al. (2018).*

-	100 mm thick RC floor slab 
*Modeled similarly as for the masonry building. Could potentially be wooden floors too, but as no foundation is assumed a RC floor slab as the ground slab seems reasonable*

-	Interior walls of wooden panels 
*Assume the same interior walls as for RECC SFH and RECC MFH for the resource efficiency scenario RES2.1* 

-	Wooden beams and post beams for structural integrity 
*Assume the same wooden beam and studs dimension as for the RECC SFH for the resource efficiency scenario RES2.1* 


The small SFH is modeled with ideal air loads. 
Lightning intensity values are taken from the existing SFH. The same for electrical equipment values, but no washing machine, dryer and dishwasher are assumed. 
Schedules and temperature setpoints are copied from the existing SFH.  


**References**  
Lavagna, M., Baldassarri, C., Campioli, A., Giorgi, S., Dalla Valle, A., Castellani, V., Sala, S., 2018. Benchmarks for environmental impact of housing in Europe: Definition of archetypes and LCA of the residential building stock. Building and Environment 145, 260–275. https://doi.org/10.1016/j.buildenv.2018.09.008


Mastrucci, A., Rao, N.D., 2017. Decent housing in the developing world: Reducing life-cycle energy requirements. Energy and Buildings 152, 629–642. https://doi.org/10.1016/j.enbuild.2017.07.072

Muringathuparambil, R.J., Musango, J.K., Brent, A.C., Currie, P., 2017. Developing building typologies to examine energy efficiency in representative low cost buildings in Cape Town townships. Sustainable Cities and Society 33, 1–17. https://doi.org/10.1016/j.scs.2017.05.011

Soust-Verdaguer Bernardette, Llatas Carmen, García-Martínez Antonio, Gómez de Cózar Juan Carlos, 2018. BIM-Based LCA Method to Analyze Envelope Alternatives of Single-Family Houses: Case Study in Uruguay. Journal of Architectural Engineering 24, 05018002. https://doi.org/10.1061/(ASCE)AE.1943-5568.0000303

Niwamara, T., Olweny, M., Ndibwami, A., 2016. Embodied Energy of Low Income Rural Housing in Uganda. Los Angeles 8.

Nutkiewicz, A., Jain, R.K., Bardhan, R., 2018. Energy modeling of urban informal settlement redevelopment: Exploring design parameters for optimal thermal comfort in Dharavi, Mumbai, India. Applied Energy 231, 433–445. 

Oyarzo, J., Peuportier, B., 2014. Life cycle assessment model applied to housing in Chile. Journal of Cleaner Production 69, 109–116. https://doi.org/10.1016/j.jclepro.2014.01.090

Paulsen, J.S., Sposto, R.M., 2013. A life cycle energy analysis of social housing in Brazil: Case study for the program “MY HOUSE MY LIFE.” Energy and Buildings 57, 95–102. https://doi.org/10.1016/j.enbuild.2012.11.014

Utama, A., Gheewala, S.H., 2008. Life cycle energy of single landed houses in Indonesia. Energy and Buildings 40, 1911–1916. https://doi.org/10.1016/j.enbuild.2008.04.017