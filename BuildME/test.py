

'''


def add_surrogate_beams(res, area, distance=0.6,):
    res_dict = {'RES0': {'Material': 'construction grade steel', 'vol': .05*.05, 'density': 8050},
                'RES2.1': {'Material': 'wood and wood products', 'vol': .12*.26, 'density': 500},
                'RES2.2': {'Material': 'construction grade steel', 'vol': .04*.04, 'density': 8050},
                'RES2.1+RES2.2': {'Material': 'wood and wood products', 'vol': .12*.20, 'density': 500}}
    side_length = area ** 0.5
    number_beams = side_length / distance + 1
    res_vol = res_dict[res]['vol'] * side_length * number_beams
    mass = res_vol * res_dict[res]['density']
    return res_dict[res]['Material'], mass



res = 'RES0'
number_shear_walls = 4
res_dict = {'RES0': {'Material': 'reinforced concrete'}}
volume_concrete = res_dict[res]['length'] * res_dict[res]['height'] * res_dict[res]['thickness'] * number_shear_walls
mass = volume * res_dict[res]['density']'''



run_idf = 'in.idf'
subprocess.call('energyplus -r %s' % run_idf,shell=True, stdout=log_file, stderr=log_file)




def add_steel_lightwall(res, floor_area, footprint_area, distance=0.4, room_h = 3):
    res_dict = {'RES2.1': {'Material': 'construction grade steel', 'vol': .15 * .0005, 'density': 8050},
                'RES2.1+RES2.2': {'Material': 'construction grade steel', 'vol': .15 * .0005, 'density': 8050}}
    perimeter = footprint_area ** 0.5 * 4
    floors = floor_area/footprint_area

    number_vertical = perimeter / distance + 1
    mass_horizontal_members = res_dict[res]['vol'] * room_h * number_vertical * res_dict[res]['density'] * floors
    mass_vertical_members = res_dict[res]['vol'] * perimeter * 2 * res_dict[res]['density'] * floors # adding at top and bottom

    return res_dict[res]['Material'], mass_horizontal_members+mass_vertical_members











from geomeppy import IDF

idff = idf.read_idf('data/archetype/USA/HR.idf')

def add_surrogate_foundations(number_piles):

    diam_pile = 2 # pile diameter is 0.45
    height_pile = 40 #20 m pile
    density_concrete = 2242.8
    density_steel = 7850

    volume_pile = (diam_pile/2)**2*3.14*height_pile
    mass_concrete_pile = density_concrete*volume_pile*number_piles
    mass_steel_pile = 15*volume_pile*number_piles #number taken from LCA on deep foundations (EU code)
    number_caps = number_piles
    volume_pile_cap = 2/3 #taken from EU code, 2m3
    mass_concrete_cap = density_concrete*volume_pile_cap*number_caps
    mass_steel_cap = 145*volume_pile_cap*number_caps #145 kg/m3 steel for cap

    mass_steel = mass_steel_pile + mass_steel_cap
    mass_concrete = mass_concrete_pile + mass_concrete_cap

    # This results in 1.8 % steel use in foundation. LCA from China yields 3.4 %
    return mass_steel, mass_concrete

share_vol = (calc_material_foundation(200)[0]/7850)/(calc_material_foundation(200)[1]/2243)*100
share_mass = (calc_material_foundation(200)[0])/(calc_material_foundation(200)[1])*100
def add_columns(area):
    mass = calculate

    material = ['concrete', 'steel']
    return material, mass

def add_surrogate_columns(res, floor_area, footprint_area, distance=9, room_h = 3, reinforcement_ratio = 0.01):
    """
    Function to add columns to the perimeter of the building. Dimensions taken from book "Design of Tall Buildings"
    :param res: scenario, RES0, RES2.1 etc.
    :param floor_area: total floor area of building
    :param footprint_area: footprint area of building
    :param distance: spacing between columns in meters
    param room_h: height of room
    :return: returns materials of columns and total mass
    """
    # TODO: check value of concrete density to use
    # TODO: ASSUME 3% reinforcement in columns (have to check) and about 270 kg/m3 concrete
    res_dict = {'RES0': {'Material': {'construction grade steel' : {'vol': 0.03 * .965 * .864 * room_h , 'density': 7850}, 'concrete': {'vol': .965 * .864 * room_h, 'density': 2400 }}}}

    perimeter = footprint_area ** 0.5 * 4
    floors = floor_area/footprint_area
    number_columns = (perimeter / distance + 1)*floors

    concrete_vol = res_dict[res]['Material']['concrete']['vol'] * number_columns
    steel_vol = res_dict[res]['Material']['construction grade steel']['vol'] * number_columns
    mass_concrete = concrete_vol * res_dict[res]['Material']['concrete']['density']
    mass_steel = steel_vol * res_dict[res]['Material']['construction grade steel']['density']

    return dict(zip(['concrete', 'construction grade steel'], [mass_concrete, mass_steel]))

no = add_surrogate_columns('RES0', res_mat['USA_HR_standard_RES0_5A_2015']['floor_area_wo_basement'], res_mat['USA_HR_standard_RES0_5A_2015']['footprint_area'] )

for k,v in no.items():
    print(k)



loadbeam = add_surrogate_beams(fnames[folder]['RES'][2], res['floor_area_wo_basement'])
columns = add_surrogate_columns(fnames[folder]['RES'][2], res['floor_area_wo_basement'], res['footprint_area'])

# Iterating through columns dict with concrete and steel since reinforced concrete
for k,v in columns.items():
    # If concrete and steel already in res, add material value
    if k in res:
        res[k] += v

if loadbeam[0] in res:
    res[loadbeam[0]] += loadbeam[1]
else:
    res[loadbeam[0]] = loadbeam[1]
if 'RES2.1' in fnames[folder]['RES'][2]:
    postbeam = add_surrogate_beams(fnames[folder]['RES'][2], surface_areas['ext_wall'])
    res[postbeam[0]] += postbeam[1]
material.save_materials(res, run_path)




