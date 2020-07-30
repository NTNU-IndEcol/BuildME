## Running simulations on IDUN HPC@NTNU 
*Andrea Nistad, 30.07.2020* 

This is a description on how to run energyplus simulations on IDUN HPC (from a Windows machine). 
There are definitely smarter and more efficient ways to do this, but it works. 

### Workflow
**1. Ask for access to the IDUN HPC**  
Ask Edgar, Eugen or Radek 

**2. Create the desired scenario combinations and copy idf and .epw files to a temporary folder (named 'tmp' in BuildME)**  
This means running the following commands in BuildME which will create a tmp folder containing a subdirectory for each combination with idf and epw files. 
 
    simulation_files = simulate.create_combinations(settings.combinations)
    simulate.nuke_folders(simulation_files)
    simulate.copy_scenario_files(simulation_files)
**3. Copy the tmp folder to IDUN**   
I did this by opening cmd and typing 

    pscp -r filepath_for_file_you_want_to_copy your_username@idun.hpc.ntnu.no:/lustre1/work/your_username/
Type your password and the files will find their way to your work directory on IDUN. Another option for Windows is to use Bitvise SSH client. 

**4. Log in to IDUN and navigate to your _work_ directory**  
Log in to IDUN using PUTTY (https://www.putty.org/) and navigate to your _work_ directory

**5. If its the first time, build and compile the correct EnergyPlus version**  
I got help with this from Bjørn - please fill in if someone figures out how to do it :-)

**6. Create desired folder structure and symlinks to folders**  
Navigate into the 'tmp' folder. It is desired to run the simulations in parallel to speed up the calculations. For this we create symlinks 
to the subdirectories in the 'tmp' folder. To do this do 
    
    #Count the number of subdirectories in 'tmp' folder 
    #This will be the number of scenarios you want to run
    Ls -d * | wc -l 
    
    #You could also only run a subset of your scenarios, f.ex. only MFH in USA 
    Ls -d USA_MFH_* | wc -l 
    
    #Creating symlinks to the subdirectories filtered above
    Dirno=0
    Sdir=`ls -d *'
    Echo $sdir
    For each in $sdir; do ln -s $each $dirno; let dirno++; done

If you now check your directory you will see your symlinks pointing to the subdirectories

NB! If you want to run a large number of simulations it might be a good idea to divide the 'tmp' folder 
into multiple directories (to have a smaller job to run...) 

**7. Create a .sh script to run simulations in the _same_ folder**  
If the symlinks are created, you are ready to run your simulations in parallel (called array jobs). 
Only thing missing is to create a .sh script within the 'tmp' folder. I used the one below. Note the 
changes required.
 
    batch.sh
    """
    #!/bin/bash

    #SBATCH --job-name=OnePythonTask
    #SBATCH --partition=CPUQ
    #SBATCH --time=06:00:00  #CHANGE! Set the time you think your simulations will take here 
    #SBATCH --ntasks=1 --tasks-per-node=1 # Should be kept as one 
    #SBATCH --array=0-736 #CHANGE! This variable sets the number of simulations you want to run

    ## Set up job environment:
    #set -o errexit  # Exit the script on any error
    #set -o nounset  # Treat any unset variables as an error

    ## Set environment variables
    export MODULPATH=${HOME}/modulefiles:${MODULEPATH}
    export USERWORK=/lustre1/work/${USER}

    echo " ---- echo variables ----"
    echo "OMP_NUM_THREADS: ${OMP_NUM_THREADS}"
    echo "USERWORK       : ${USERWORK}"
    echo "CPUs on node   : ${SLURM_CPUS_ON_NODE}"
    echo "CPUs for the job: ${SLURM_JOBS_CPUS_PER_NODE}"

    export MODULEPATH=${HOME}/modulefiles:${MODULEPATH}
    module --quiet purge  # Reset the modules to the system default
    module load EnergyPlus/9.2.0
    module list
    #source ${EBROOTANACONDA3}/etc/profile.d/conda.sh

    # execute job, call energyplus
    cd ${SLURM_ARRAY_TASK_ID}
    energyplus -r 
 
 **8. Start simulations**  
 Finally! Type 
    
    sbatch batch.sh
 to start your job. And checkout the queue for updates on how its progressing
 
    sq your_username
        
 The results will pop into your folders when the simulations are done 
 
 **9. Collect simulation results and copy back to your computer**  
 You can now collect the eplusout.csv, which contains the simulation results. I create a zip file and
 then copy it back to my computer. 
 To create a zip file on linux do: 
    
    find . -name eplusout.csv -print | zip -@ name_of_zip_folder
        
 Copy it back to your machine by typing the following in your cmd
 
    pscp -r your_username@idun.hpc.ntnu.no:/lustre1/work/your_username/tmp/name_of_zip_folder filepath_to_your_local_directory

 **10. Post-process results on your local machine**   
 I then did the post-processing on my local machine, running
  
    res_energy = simulate.collect_energy(simulation_files)
    res_mat = simulate.load_material(simulation_files)

    simulate.save_ei_result(res_energy, res_mat)
    simulate.save_mi_result(res_mat)