import subprocess
import sys

from BuildME import settings, batch, simulate, __version__


def run(run_new=True, run_eplus=True):
    if run_new:
        print("Running new simulation...")
        # Creating the scenario combinations
        combinations = settings.debug_combinations
        batch_simulation, run = batch.create_batch_simulation(combinations)
    else:
        print("Continuing previous simulation...")
        batch_simulation = batch.find_and_load_last_run()
    # Performing simulations
    if run_eplus:
        simulate.calculate_energy(batch_simulation, parallel=True)
        simulate.aggregate_energy(batch_simulation, unit='kWh')
        print("Energy simulations done")
    simulate.calculate_materials(batch_simulation)
    print("Material extraction done")

    # Postprocessing
    simulate.aggregate_materials(batch_simulation)
    simulate.calculate_intensities(batch_simulation)
    simulate.collect_results(batch_simulation)
    # simulate.weighing_climate_region(batch_simulation)
    # simulate.cleanup(batch_simulation, archive=True, del_temp=True)
    print("Done.")


if __name__ == "__main__":
    print("Welcome to BuildME v%s" % __version__)
    if 'darwin' in sys.platform:
        print('Running \'caffeinate\' on MacOSX to prevent the system from sleeping')
        subprocess.Popen('caffeinate')
    run(run_new=True, run_eplus=True)
