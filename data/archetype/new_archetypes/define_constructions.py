"""
Functions to define the different material options based on an idf file
Use this to define the different material sub-types for the small SFH.

Should be put into idf.py if used in future
"""
from BuildME import idf

def set_surface_element(idf_f, surface, boundary, construction):
    """
    Function to define the building envelope elements. Can't use the idf file and need to use a list
    of surfaces instead.
    :param idf_f: idf file to modify
    :param surface: surface to modify: floor, roof, wall
    :param boundary: Outdoors, Surface, Grounds etc.
    :param construction: construction to be used for the surface
    """
    for obj in idf_f.idfobjects['BuildingSurface:Detailed']:
        if obj.Surface_Type == surface and obj.Outside_Boundary_Condition == boundary:
            setattr(obj, 'Construction_Name', construction)

    return idf_f

def define_building_surfaces(idf_f, building_construction):
    """
    Function to set the building surface elements.
    :param idf_file: idf filename path,
    :param building_construction: dict of construction for floor, roof, internal walls, exterior walls
    :param subarchetype: name of subarchetype, like masonry/concrete/wood
    """

    idf_f = set_surface_element(idf_f, 'Floor', 'Ground', building_construction['Floor'].Name)
    idf_f = set_surface_element(idf_f, 'Wall', 'Outdoors', building_construction['Ext_wall'].Name)
    idf_f = set_surface_element(idf_f, 'Wall', 'Surface', building_construction['Int_wall'].Name)
    idf_f = set_surface_element(idf_f, 'Roof', 'Outdoors', building_construction['Roof'].Name)


    return idf_f

# Defining masonry version
# Reading in the idf file for the generic archetype
filename = 'SFH-small'
filepath = 'data/archetype/new_archetypes/'+filename+'.idf'
idff = idf.read_idf(filepath)

# Defining material subtypes
masonry = {'Floor': idff.newidfobject("Construction", Name="FLOOR_CONSTRUCTION-standard-RES0",
                 Outside_Layer="floor_consol_layer",
                 Layer_2="Concrete_10cm",
                 Layer_3="Reinforcement_1perc_10cm",
                 Layer_4 = "Carpet_n_pad"),

            'Roof': idff.newidfobject("Construction", Name="ROOF_CONSTRUCTION-standard-RES0",
                 Outside_Layer="Metal_surface",
                 Layer_2="OSB_1/2in",
                 Layer_3 = "ceil_consol_layer-en-standard",
                 Layer_4 = "Drywall_1/2in"),

            'Ext_wall': idff.newidfobject("Construction", Name="EXT_WALL_CONSTRUCTION-standard-RES0",
                 Outside_Layer="Stucco_1in",
                 Layer_2="Bldg_paper_felt",
                 Layer_3="sheathing_consol_layer",
                 Layer_4="Brick - fired clay - 1600 kg/m3 - 230mm",
                 Layer_5="wall_consol_layer-en-standard",
                 Layer_6="Drywall_1/2in"),

            'Int_wall': idff.newidfobject("Construction", Name="INT_WALL_CONSTRUCTION-standard-RES0",
                 Outside_Layer="Cement_plaster_0.012",
                 Layer_2="Brick - fired clay - 1600 kg/m3 - 102mm",
                 Layer_3="Cement_plaster_0.012")}

idff = define_building_surfaces(idff, masonry)
idff.savecopy('data/archetype/new_archetypes/'+filename+'-masonry.idf')

# Defining concrete version
filename = 'SFH-small'
filepath = 'data/archetype/new_archetypes/'+filename+'.idf'
idff = idf.read_idf(filepath)


concrete = {'Floor': idff.newidfobject("Construction", Name="FLOOR_CONSTRUCTION-standard-RES0",
                 Outside_Layer="floor_consol_layer",
                 Layer_2="Concrete_10cm",
                 Layer_3="Reinforcement_1perc_10cm",
                 Layer_4 = "Carpet_n_pad"),

            'Roof': idff.newidfobject("Construction", Name="ROOF_CONSTRUCTION-standard-RES0",
                 Outside_Layer="Concrete_15cm",
                 Layer_2 = "Reinforcement_1perc_15cm",
                 Layer_3 = "ceil_consol_layer-en-standard"),

            'Ext_wall': idff.newidfobject("Construction", Name="EXT_WALL_CONSTRUCTION-standard-RES0",
                 Outside_Layer="Stucco_1in",
                 Layer_2="Bldg_paper_felt",
                 Layer_3="sheathing_consol_layer",
                 Layer_4="Concrete_15cm",
                 Layer_5="Reinforcement_1perc_15cm",
                 Layer_6 = "wall_consol_layer-en-standard",
                 Layer_7="Drywall_1/2in"),

            'Int_wall': idff.newidfobject("Construction", Name="INT_WALL_CONSTRUCTION-standard-RES0",
                 Outside_Layer="Cement_plaster_0.012",
                 Layer_2="Brick - fired clay - 1600 kg/m3 - 102mm",
                 Layer_3="Cement_plaster_0.012")}

idff = define_building_surfaces(idff, concrete)
idff.savecopy('data/archetype/new_archetypes/'+filename+'-concrete.idf')

# Defining wooden version
filename = 'SFH-small'
filepath = 'data/archetype/new_archetypes/'+filename+'.idf'
idff = idf.read_idf(filepath)


wood = {'Floor': idff.newidfobject("Construction", Name="FLOOR_CONSTRUCTION-standard-RES0",
                 Outside_Layer="floor_consol_layer",
                 Layer_2="Concrete_10cm",
                 Layer_3="Reinforcement_1perc_10cm",
                 Layer_4 = "Carpet_n_pad"),

            'Roof': idff.newidfobject("Construction", Name="ROOF_CONSTRUCTION-standard-RES0",
                 Outside_Layer="Metal_surface",
                 Layer_2="OSB_1/2in",
                 Layer_3 = "ceil_consol_layer-en-standard",
                 Layer_4 = "Drywall_1/2in"),

            'Ext_wall': idff.newidfobject("Construction", Name="EXT_WALL_CONSTRUCTION-standard-RES0",
                 Outside_Layer="Stucco_1in",
                 Layer_2="Bldg_paper_felt",
                 Layer_3="sheathing_consol_layer",
                 Layer_4="OSB_5/8in",
                 Layer_5 = "wall_consol_layer-en-standard",
                 Layer_6="Drywall_1/2in"),

            'Int_wall': idff.newidfobject("Construction", Name="INT_WALL_CONSTRUCTION-standard-RES0",
                 Outside_Layer="Drywall_1/2in",
                 Layer_2="OSB_5/8in",
                 Layer_3="Drywall_1/2in")}

idff = define_building_surfaces(idff, wood)
idff.savecopy('data/archetype/new_archetypes/'+filename+'-wood.idf')

