import logging.config
from BuildME import settings, pre, idf, material, energy, simulate, __version__

logger = logging.getLogger('BuildME')


def run_new():
    """Run new simulation from scratch"""

    logging.info("Running new simulation...")
    # Some pre-processing
    pre.validate_ep_version()
    pre.create_mmv_variants(comb=settings.debug_combinations)

    # Creating the scenario combinations based on energy standard and a resource efficiency strategy
    #   as specified in settings.combinations
    fnames, run = simulate.create_combinations(settings.debug_combinations)

    # Deletes exisitng folders that contains simulation results
    # simulate.nuke_folders(fnames)  # deletes only the folder with the case you try to simulate

    # Copy scenarios .idf to ./tmp
    simulate.copy_scenario_files(fnames, run)

    # Create run file for HPC
    # simulate.create_sq_job(fnames)

    simulate.calculate_energy()
    simulate.calculate_materials(run, fnames)

    res_energy = simulate.collect_energy(fnames)
    res_mat = simulate.load_material(fnames)

    simulate.save_ei_result(run, res_energy, res_mat)
    simulate.save_mi_result(run, res_mat)


def continue_previous(run_eplus=False):
    """
    Continue a previous simulation. Assumes that scenarios were created and ./tmp folder was created. Will load latest
    subfolder (using the name) in the .tmp/ folder. This is especially useful when the energy simulation has already
    been performed successfully, because this is the most time-consuming step.
    :param run_eplus: If True, energy simulation will be performed
    :return: None
    """

    # Find and load last simulation
    logging.info("Continuing previous simulation...")
    fnames, run = simulate.find_last_run()
    fnames = simulate.load_run_data_file(fnames)
    if run_eplus:
        # if energy simulation was not successful yet
        simulate.calculate_energy()
    simulate.calculate_materials(run, fnames)

    res_energy = simulate.collect_energy(fnames)
    res_mat = simulate.load_material(fnames)

    simulate.save_ei_result(run, res_energy, res_mat)
    simulate.save_mi_result(run, res_mat)


if __name__ == "__main__":
    logging.config.dictConfig(settings.LOGGING_CONFIG)
    logging.info("BuildME is starting...")
    # Only run either of the following functions
    # run_new()
    continue_previous()
    logging.info("Done.")
