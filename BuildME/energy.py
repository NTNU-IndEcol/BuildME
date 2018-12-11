"""
Energy demand algorithm for the RECC building model
"""

import shutil
import os
import subprocess

import settings

__author__ = "Niko Heeren"
__email__ = "niko.heeren@gmail.com"
__license__ = "MIT"
__copyright__ = "Niko Heeren"
__version__ = "0.1"
__status__ = "ALPHA"



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


def copy_files(copy_list, tmp_run_path, create_dir=True, assert_exists=True):
    """
    Copies the files to the desired location.
    I guess symlinks could work too, but let's be nice to Windows folks :-P
    :param copy_list: List of files that should be copied, e.g. created with gather_files_to_copy()
    :param tmp_run_path: the subfolder for the simulation run
    :param create_dir: Switch allowing to create new folders
    :param assert_exists: Check if the folder exists
    """

    run_folder = os.path.join(settings.tmp_path, tmp_run_path)
    if assert_exists:
        assert not os.path.exists(run_folder), "Folder already exists: %s" % run_folder
    if create_dir:
        os.makedirs(run_folder)
    for file in copy_list:
        basename = os.path.basename(file)
        if os.path.splitext(file)[-1] == '.idf':
            basename = 'in.idf'
        elif os.path.splitext(file)[-1] == '.epw':
            basename = 'in.epw'
        shutil.copy2(file, os.path.join(run_folder, basename))


def delete_ep_files(tmp_folder, ep_files=settings.ep_exec_files):
    """
    Deletes the e+ files after simulation
    :param tmp_folder:
    :param ep_files:
    """
    for f in ep_files:
        os.remove(os.path.join(settings.tmp_path, tmp_folder, f))




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
    log_file = open("log_ExpandObjects.txt", 'w')
    subprocess.call('./ExpandObjects', shell=True, stdout=log_file, stderr=log_file)
    log_file.close()
    if os.path.exists('BasementGHTIn.idf'):
        log_file = open("log_Basement.txt", 'w')
        # subprocess.call('./Basement', shell=True, stdout=f, stderr=f)
        log_file.close()
    merged_idf = open('merged.idf', 'w')
    merged_idf.write(open('expanded.idf', 'r').read())
    merged_idf.write(open('EPObjects.txt', 'r').read())
    merged_idf.close()
    log_file = open("log_energyplus.txt", 'r+')
    subprocess.call('./energyplus -r merged.idf', shell=True, stdout=log_file, stderr=log_file)
    log_file.seek(0)
    assert log_file.readlines()[-1] == 'EnergyPlus Completed Successfully.\n'
    log_file.close()





