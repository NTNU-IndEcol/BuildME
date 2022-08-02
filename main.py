import subprocess
import sys

from BuildME import settings, pre, idf, material, energy, simulate, __version__


def run_new():
    """Run new simulation from scratch"""

    print("Running new simulation...")
    # Some pre-processing
    pre.validate_ep_version()
    pre.create_mmv_variants(comb=settings.debug_combinations)

    # Creating the scenario combinations based on energy standard and a resource efficiency strategy
    #   as specified in settings.combinations
    fnames, run = simulate.create_combinations(settings.debug_combinations)

    # Deletes exisitng folders that contains simulation results
    # simulate.nuke_folders(fnames)  # deletes only the folder with the case you try to simulate

    # Copy scenarios .idf to ./tmp
    print("%i scenario combinations created" % len(fnames))
    simulate.copy_scenario_files(fnames, run)

    # Create run file for HPC
    # simulate.create_sq_job(fnames)

    # simulate.calculate_energy()
    simulate.calculate_energy_mp()
    print("Energy simulations done")
    simulate.calculate_materials(run, fnames)
    print("Material extraction done")

    res_energy = simulate.collect_energy(fnames)
    print("Energy results collected")
    res_mat = simulate.load_material(fnames)
    print("Material results collected")

    simulate.save_ei_result(run, res_energy, res_mat)
    simulate.save_mi_result(run, res_mat)
    simulate.cleanup(fnames, run)
    print("Done.")


def continue_previous(run_eplus=False):
    """
    Continue a previous simulation. Assumes that scenarios were created and ./tmp folder was created. Will load latest
    subfolder (using the name) in the .tmp/ folder. This is especially useful when the energy simulation has already
    been performed successfully, because this is the most time-consuming step.
    :param run_eplus: If True, energy simulation will be performed
    :return: None
    """

    # Find and load last simulation
    print("Continuing previous simulation...")
    fnames, run = simulate.find_last_run()
    fnames = simulate.load_run_data_file(fnames)
    if run_eplus:
        # if energy simulation was not successful yet
        simulate.calculate_energy()
        print("Energy simulations done")
    simulate.calculate_materials(run, fnames)
    print("Material extraction done")

    res_energy = simulate.collect_energy(fnames)
    print("Energy results collected")
    res_mat = simulate.load_material(fnames)
    print("Material results collected")

    simulate.save_ei_result(run, res_energy, res_mat)
    simulate.save_mi_result(run, res_mat)
    simulate.cleanup(fnames, run)
    print("Done.")


if __name__ == "__main__":
    print("Welcome to BuildME v%s" % __version__)
    if 'darwin' in sys.platform:
        print('Running \'caffeinate\' on MacOSX to prevent the system from sleeping')
        subprocess.Popen('caffeinate')
    # Only run either of the following functions
    run_new()
    # continue_previous()
