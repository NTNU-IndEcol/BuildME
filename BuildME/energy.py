"""
Energy demand algorithm for the RECC building model

Copyright: Niko Heeren, 2019
"""
import os
import subprocess
import shutil
import platform
from BuildME import settings


def perform_energy_calculation(out_dir, ep_dir, epw_path, keep_all):
    """
    Copies the required EnergyPlus files and initiates the energy demand simulation
    :param out_dir: output folder directory
    :param ep_dir: EnergyPlus directory
    :param epw_path: path to the EPW file with weather data
    :param keep_all: boolean indicating whether to keep all simulation files (incl. the .eso file)
    """
    copy_files(out_dir, ep_dir, epw_path)
    run_energyplus_single(out_dir)
    if not keep_all:
        delete_ep_files(out_dir)
    return


def perform_energy_calculation_mp(args):
    """
    Copies the required EnergyPlus files and initiates the energy demand simulation (with multiprocessing)
    :param args: arguments (out_dir - output folder directory,
                            ep_dir - EnergyPlus directory,
                            epw_path - path to the EPW file with weather data,
                            keep_all - boolean indicating whether to keep all simulation files (incl. the .eso file)
                            q - multiprocessing Queue object,
                            no - iteration number)
    """
    out_dir, ep_dir, epw_path, keep_all, q, no = args
    copy_files(out_dir, ep_dir, epw_path)
    run_energyplus_single(out_dir)
    if not keep_all:
        delete_ep_files(out_dir)
    q.put(no)
    return


def get_exec_files():
    """
    Gets the names of the files needed for energy simulation depending on the operating system
    :returns: ep_exec_files: a list of the filenames
    """
    ep_version = settings.ep_version
    # Checking OS and define files to copy to the temporary folders
    plf = platform.system()
    if plf == 'Windows':
        ep_exec_files = ["energyplus.exe", "Energy+.idd", "EPMacro.exe", "ExpandObjects.exe",
                         "PreProcess/GrndTempCalc/Basement.exe", "PreProcess/GrndTempCalc/BasementGHT.idd",
                         "PreProcess/GrndTempCalc/Slab.exe", "PreProcess/GrndTempCalc/SlabGHT.idd",
                         "PostProcess/ReadVarsESO.exe", "energyplusapi.dll"
                         ]
    elif plf == 'Darwin':  # i.e. macOS
        ep_exec_files = ["energyplus", "energyplus-%s" % ep_version, "Energy+.idd", "EPMacro", "ExpandObjects",
                         "libenergyplusapi.%s.dylib" % ep_version,  # required by energyplus
                         "libgfortran.5.dylib", "libquadmath.0.dylib", 'libgcc_s.1.dylib',  # required by ExpandObjects
                         "PreProcess/GrndTempCalc/Basement", "PreProcess/GrndTempCalc/BasementGHT.idd",
                         "PreProcess/GrndTempCalc/Slab", "PreProcess/GrndTempCalc/SlabGHT.idd",
                         "PostProcess/ReadVarsESO"
                         ]
    elif plf == 'Linux':
        ep_exec_files = ["energyplus", "energyplus-%s" % ep_version, "Energy+.idd", "EPMacro", "ExpandObjects",
                         "libenergyplusapi.so.%s" % ep_version,  # required by energyplus
                         "PreProcess/GrndTempCalc/Basement", "PreProcess/GrndTempCalc/BasementGHT.idd",
                         "PreProcess/GrndTempCalc/Slab", "PreProcess/GrndTempCalc/SlabGHT.idd",
                         "PostProcess/ReadVarsESO"
                         ]
    else:
        raise NotImplementedError('OS is not supported! %s' % plf)
    return ep_exec_files


def copy_files(out_dir, ep_dir, epw_path):
    """
    Copies the files needed for energy simulation to the desired location.
    :param out_dir: output folder directory
    :param ep_dir: EnergyPlus directory
    :param epw_path: path to the EPW file with weather data
    """
    # create a list of items to be copied (EnergyPlus executable files, IDF file, EPW file)
    copy_list = [os.path.join(ep_dir, f) for f in get_exec_files()]
    copy_list.append(epw_path)
    # check if all the paths in copy_list exist
    bad_news = [f for f in copy_list if not os.path.exists(f)]
    assert len(bad_news) == 0, "The following files do not exist: %s" % bad_news
    # copy the files to the output directory
    for file in copy_list:
        basename = os.path.basename(file)
        if os.path.splitext(file)[-1] == '.epw':
            basename = 'in.epw'
        shutil.copy2(file, os.path.join(out_dir, basename))
    return


def delete_ep_files(out_dir):
    """
    Deletes the e+ files after simulation
    :param out_dir: output folder directory
    """
    # Files that should be deleted in the temporary folder after successful simulation
    #  'eplusout.eso' is fairly large and not being used by BuildME
    exec_files_to_delete = [os.path.join(out_dir, os.path.basename(f)) for f in get_exec_files()]
    more_files_to_delete = [os.path.join(out_dir, i) for i in ['eplusout.eso']]
    for f in (exec_files_to_delete + more_files_to_delete):
        os.remove(f)
    return


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


def run_energyplus_single(out_dir, verbose=True):
    """
    Runs the energy demand simulation in EnergyPlus
    :param out_dir: output folder directory
    :param verbose: Switch to print a delete confirmation
    """
    # 1. Run `./ExpandObjects`
    cwd = os.getcwd()
    os.chdir(out_dir)
    # for exec in ['./ExpandObjects', './Basement', './energyplus']:

    with open("log_ExpandObjects.txt", 'w') as log_file:
        cmd = out_dir + '/ExpandObjects'
        log_file.write("%s\n\n" % cmd)
        log_file.flush()
        subprocess.call(cmd, shell=True, stdout=log_file, stderr=log_file)
    if os.path.exists('BasementGHTIn.idf'):
        with open("log_Basement.txt", 'w') as log_file:
            cmd = out_dir + '/Basement'
            log_file.write("%s\n\n" % cmd)
            log_file.flush()
            subprocess.call(cmd, shell=True, stdout=log_file, stderr=log_file)
        with open('merged.idf', 'w') as merged_idf:
            with open('expanded.idf', 'r') as expanded_idf:
                merged_idf.write(expanded_idf.read())
            with open('EPObjects.txt', 'r') as epobjects:
                merged_idf.write(epobjects.read())
            run_idf = 'merged.idf'
    elif os.path.exists('GHTIn.idf'):
        with open("log_Slab.txt", 'w') as log_file:
            cmd = out_dir + '/Slab'
            subprocess.call(cmd, shell=True, stdout=log_file, stderr=log_file)
        with open('merged.idf', 'w') as merged_idf:
            with open('expanded.idf', 'r') as expanded_idf:
                merged_idf.write(expanded_idf.read())
            with open('SLABSurfaceTemps.TXT', 'r') as epobjects:
                merged_idf.write(epobjects.read())
        run_idf = 'merged.idf'
    else:
        run_idf = 'expanded.idf'

    if not os.path.exists('expanded.idf'):
        run_idf = 'in.idf'

    with open("log_energyplus.txt", 'w+') as log_file:
        cmd = f'"{os.path.join(out_dir, "energyplus")}" -r {run_idf}'
        log_file.write("%s\n\n" % cmd)
        log_file.flush()
        subprocess.call(cmd, shell=True, stdout=log_file, stderr=log_file)
        log_file.seek(0)
        if log_file.readlines()[-1] != 'EnergyPlus Completed Successfully.\n':
            # print("ERROR: '%s' energy simulation was not successful" % tmp_path)
            raise AssertionError("Energy simulation was not successful in folder '%s'. "
                                 "See files 'log_energyplus.txt' and 'eplusout.err' for details."
                                 % os.path.basename(out_dir))
        log_file.close()
    if verbose:
        print("Energy simulation successful in folder '%s'" % os.path.basename(out_dir))
    os.chdir(cwd)




