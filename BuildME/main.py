
import pandas as pd
import numpy as np
from tqdm import tqdm
import encodings

from BuildME import settings, idf, material, energy, simulate, __version__

#creating the corresponding .idf file given an energy standard and a resource efficiency strategy and copy file into folder
simulation_files = simulate.create_combinations(settings.testing_combinations)

#deletes exisitng folders that contains simulation results
simulate.nuke_folders(simulation_files) #deletes only the folder with the case you try to simulate

#copy scenarios .idf to the correct folder
simulate.copy_scenario_files(simulation_files)
# create run file
#simulate.create_sq_job(simulation_files)

#simulate.calculate_energy()
simulate.calculate_materials(simulation_files)

#res_energy = simulate.collect_energy(simulation_files)
res_mat = simulate.load_material(simulation_files)

#simulate.save_ei_result(res_energy, res_mat)
#simulate.save_mi_result(res_mat)

#simulate.save_ei_for_odym(res_energy)
#simulate.save_ei_for_odym(res_mat)

floor_area = res_mat['PL_HR_standard_RES2.1_Poland_2015']['floor_area_wo_basement']
energy_intensity = {k: v / floor_area for k, v in res_mat['PL_HR_standard_RES2.1_Poland_2015'].items()}
''''''
simulate.save_ei_result(res_energy, res_mat)
simulate.save_mi_result(res_mat)
fname = [x for x in tqdm(simulation_files, leave=True)][0]
idff = idf.read_idf('data/archetype/ES/HR.idf')
res = ['USA', 'MFH', 'non-standard']
en_replace = pd.read_excel('./data/replace.xlsx', index_col=[0, 1, 2], sheet_name='en-standard')
idf_f = simulate.apply_rule_from_excel(idff, ['USA', 'HR', 'standard'], en_replace)
xls_values = en_replace.loc(axis=0)[[res[0]], [res[1]], [res[2]]]
    if not 'RES' in res[2]:
        assert len(xls_values) > 0, "Did not find an energy replacement for '%s" % res
    for xls_value in xls_values.iterrows():
        if xls_value[1]['Value'] == 'skip':
            print("bam")
            continue
        for idfobj in idff.idfobjects[xls_value[1]['idfobject'].upper()]:
            #print(idfobj)
            #print(xls_value[1].Name)
            if idfobj.Name not in ('*', xls_value[1].Name):
                print(idfobj.Name)
                continue
            setattr(idfobj, xls_value[1]['objectfield'], xls_value[1]['Value'])

for idfobj in idff.idfobjects[xls_value[1]['idfobject'].upper()]:
    print(idfobj)
    if idfobj.Name not in ('*', xls_value[1].Name):
        continue
    setattr(idfobj, xls_value[1]['objectfield'], xls_value[1]['Value']

#ener = res_energy['USA_MFH_standard_RES0_5A_2015']
#ener = {k: a/10e6 for k,a in ener.items()}
#ener_m2 = {k: a/2174 for k,a in ener.items()}

#mat = res_mat['USA_MFH_standard_RES0_8_2015']
#res_mat_m2 = {k: a/2174 for k,a in mat.items()}

print("Extracting materials and surfaces...")
    if not simulation_files:
        simulation_files = simulate.load_run_data_file(simulate.find_last_run())
    fallback_materials = material.load_material_data()
    tq = tqdm(simulation_files, desc='Initiating...', leave=True)
    for folder in tq:
        tq.set_description(folder)
        run_path = os.path.join(settings.tmp_path, folder)
        idff = material.read_idf(os.path.join(run_path, 'in.idf'))
        materials = material.read_materials(idff)
        materials_dict = material.make_materials_dict(materials)



        densities = material.make_mat_density_dict(materials_dict, fallback_materials)
        constructions = material.read_constructions(idff)
        mat_vol_m2 = material.calc_mat_vol_m2(constructions, materials_dict, fallback_materials)


        #works until here

        surfaces = material.get_surfaces_with_zone_multiplier(idff, simulation_files[folder]['energy_standard'][2],
                                         simulation_files[folder]['RES'][2])

        mat_vol_bdg = material.calc_mat_vol_bdg(surfaces, mat_vol_m2)
        total_material_mass = material.calc_mat_mass_bdg(mat_vol_bdg, densities)

        odym_mat = simulate.translate_to_odym_mat(total_material_mass)
        surface_areas = material.calc_surface_areas(surfaces)

        res = odym_mat
        res['floor_area_wo_basement'] = surface_areas['floor_area_wo_basement']
        res['footprint_area'] = surface_areas['footprint_area']

        #ER HER NÅ!
        loadbeam = simulate.add_surrogate_beams(simulation_files[folder]['RES'][2], res['floor_area_wo_basement'])
        if loadbeam[0] in res:
            res[loadbeam[0]] += loadbeam[1]
        else:
            res[loadbeam[0]] = loadbeam[1]
        if 'RES2.1' in simulation_files[folder]['RES'][2]:
            postbeam = simulate.add_surrogate_beams(simulation_files[folder]['RES'][2], surface_areas['ext_wall'])
            res[postbeam[0]] += postbeam[1]
        material.save_materials(res, run_path)

        # TODO: ALT KJØRER, MEN SE OM JEG FINNER NOE DATA FOR BEAMS REQUIRED!!
'''