"""
Energy demand algorithm for the RECC building model

Copyright: Niko Heeren, 2019
"""
import datetime
import shutil
import os
import subprocess

import pandas as pd

from BuildME import settings




def launch_ep():
    pass


def cleanup_post_sim():
    pass


def gather_files_to_copy(idf, epw, ep_files=settings.ep_exec_files, check=True):
    """
    Collect the neccessary files for copy_files() and check if they exist
    :param idf: The IDF file in question
    :param epw: EPW file in question
    :param ep_files: the e+ files needed for the worker to run
    :param check:
    :return:
    """
    # 1. necessary e+ executable files
    copy_list = [os.path.join(settings.ep_path, f) for f in ep_files]
    # 2. idf e+ input file
    copy_list.append(os.path.join(settings.archetypes, idf))
    # 3. epw climate file
    copy_list.append(os.path.join(settings.climate_files, epw))
    if check:
        bad_news = [f for f in copy_list if not os.path.exists(f)]
        assert len(bad_news) == 0, "The following files do not exist: %s" % bad_news
    return copy_list


def get_timestamp_path():
    return datetime.datetime.now().strftime("%y%m%d-%H%M%S.%f")


def copy_files(copy_list, tmp_run_path=None, create_dir=True):
    """
    Copies the files to the desired location.
    I guess symlinks could work too, but let's be nice to Windows folks :-P
    :param copy_list: List of files that should be copied, e.g. created with gather_files_to_copy()
    :param tmp_run_path: the subfolder for the simulation run
    :param create_dir: Switch allowing to create new folders
    :param assert_exists: Check if the folder exists
    """
    if not tmp_run_path:
        tmp_run_path = get_timestamp_path()
    run_folder = os.path.join(settings.tmp_path, tmp_run_path)
    if create_dir:
        os.makedirs(run_folder)
    for file in copy_list:
        basename = os.path.basename(file)
        if os.path.splitext(file)[-1] == '.idf':
            basename = 'in.idf'
        elif os.path.splitext(file)[-1] == '.epw':
            basename = 'in.epw'
        shutil.copy2(file, os.path.join(run_folder, basename))
    return tmp_run_path


def delete_ep_files(copy_list, tmp_run_path):
    """
    Deletes the e+ files after simulation, skips input and weather file
    :param tmp_folder:
    :param ep_files:
    """
    run_folder = os.path.join(settings.tmp_path, tmp_run_path)
    for f in copy_list:
        if os.path.basename(f)[-4:] in ['.idf', '.epw']:
            continue
        os.remove(os.path.basename(f))


def delete_temp_folder(tmp_run_path, verbose=False):
    """
    Delete the temporary folder *completely*
    :param tmp_run_path: foldername to delete
    :param verbose: Switch to print a delete confirmation
    """

    # This syntax ensures that this is a subfolder of settings.tmp_path
    shutil.rmtree(os.path.join(settings.tmp_path, tmp_run_path))
    if verbose:
        print("Deleted '%s'" % tmp_run_path)


def run_energyplus_single(tmp_path):
    """
    Runs the model single-threaded
    See docs/energyplus.md for more info
    :param idf_file:
    :param epw_file:
    :return:
    """
    # 1. Run `./ExpandObjects`
    os.chdir(os.path.join(settings.tmp_path, tmp_path))
    # for exec in ['./ExpandObjects', './Basement', './energyplus']:
    with open("log_ExpandObjects.txt", 'w') as log_file:
        subprocess.call('./ExpandObjects', shell=True, stdout=log_file, stderr=log_file)
    if os.path.exists('BasementGHTIn.idf'):
        with open("log_Basement.txt", 'w') as log_file:
            pass
            subprocess.call('./Basement', shell=True, stdout=log_file, stderr=log_file)
    with open('merged.idf', 'w') as merged_idf:
        with open('expanded.idf', 'r') as expanded_idf:
            merged_idf.write(expanded_idf.read())
        with open('EPObjects.txt', 'r') as epobjects:
            merged_idf.write(epobjects.read())
    with open("log_energyplus.txt", 'w+') as log_file:
        subprocess.call('./energyplus -r merged.idf', shell=True, stdout=log_file, stderr=log_file)
        log_file.seek(0)
        assert log_file.readlines()[-1] == 'EnergyPlus Completed Successfully.\n'
        log_file.close()


def ep_result_collector(ep_path):
    results_to_collect = ("Heating:EnergyTransfer [J](Hourly)",	"Cooling:EnergyTransfer [J](Hourly)",
                          # Note the trailing whitespace at the end of "InteriorEquipment:Electricity [J](Hourly) "
                          "InteriorLights:Electricity [J](Hourly)", "InteriorEquipment:Electricity [J](Hourly) ")
    ep_file = os.path.join(ep_path, 'eplusout.csv')
    ep_out = pd.read_csv(ep_file)
    results = ep_out.loc[:, results_to_collect].sum()
    results.to_csv(os.path.join(ep_path, 'energy_intensity.csv'))
    return results




