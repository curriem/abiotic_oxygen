import numpy as np
import os
import smart
import multiprocessing
import stat
NCPU = multiprocessing.cpu_count()


def make_pt_fl(o2_loc, o2_mixing_ratio, place, cold_trap=0.1):

    ref_pt = '../../earth_standard_icrccm_vmix.pt'
    header = ["Press",
              "Temp",
              "H2O",
              "CO2",
              "O3",
              "N2O",
              "CO",
              "CH4",
              "O2"]

    header = "        ".join(header)

    ref_pt_data = np.genfromtxt(ref_pt, skip_header=1)
    new_pt_data = np.copy(ref_pt_data)

    ref_p = ref_pt_data[:, 0]
    ref_o2 = ref_pt_data[:, 8]

    if o2_loc == 'upper':
        new_o2 = np.ones_like(ref_o2)
        new_o2[ref_p > cold_trap] = 0
        new_o2[ref_p <= cold_trap] = o2_mixing_ratio

    elif o2_loc == 'mixed':
        new_o2 = o2_mixing_ratio * np.ones_like(ref_o2)

    new_pt_data[:, 8] = new_o2

    #new_pt_fl_name = o2_loc + '_oxygen_' + str(o2_mixing_ratio).replace('.', '_') + '_trop_' + str(cold_trap).replace('.', '_') + '.pt'

    np.savetxt(place, new_pt_data, delimiter='   ', header=header, comments='')

def run_smart(pt_fl, place, R=100000):

    # make the directory for the smart run
    try:
        os.mkdir(place)
    except OSError:
        pass

    # load pt file (relative import frim photochem directory)
    atm = smart.interface.Atmosphere.from_pt('../pt_fls/'+pt_fl, atm_dir=place)

    # Set atmosphere parameters
    atm.set_dataframe_from_profiles()
    atm.write_atm()

    sim = smart.interface.Smart(tag='case', atmosphere=atm)
    sim.smartin.source = 3 # solar and thermal sources
    sim.smartin.out_format = 1 # no transit calculations

    # set the star as TRAPPIST-1
    sim.smartin.spec = '../../star_data/TRAPPIST-1.dat'
    sim.smartin.spec_skip = 5
    sim.smartin.spec_unit = 2 # Set unit to W/m^2/um
    sim.smartin.radstar = 0.121 # times sun radius

    # set the planet as TRAPPIST-1e
    sim.smartin.r_AU = 0.02916
    sim.smartin.radius = 0.915 * 6371.
    sim.smartin.grav = 0.930 * 9.8

    sim.lblin.radius = 0.915 * 6371.
    sim.lblin.grav = 0.930 * 9.8

    sim.set_run_in_place(place=place)

    wlmin = 0.4
    wlmax = 1.5
    sim.smartin.minwn = 1e4 / wlmax
    sim.smartin.maxwn = 1e4 / wlmin
    sim.lblin.minwn = 1e4 / wlmax
    sim.lblin.maxwn = 1e4 / wlmin

    # include transit spectroscopy
    sim.smartin.out_format = 9
    sim.smartin.itrnst = 2 # ray tracing

    sim.smartin.irefract = 1 # turn on refraction

 # modify resolution of spectrum
    delt_nu = 1e4 / ((wlmax - wlmin)/2 * R)
    sim.smartin.FWHM = delt_nu
    sim.smartin.sample_res = delt_nu

    # set to run on this machine
    sim.set_executables_automatically()

    # generate LBLABC scripts
    sim.gen_lblscripts()

    # run LBLABC on all but two CPUs on machine
    sim.run_lblabc(ncpu=NCPU)

    #sim.tag = sim.tag + '_' + tag + '_' + 'R' + str(R)

    # run SMART
    sim.write_smart(write_file=True)
    sim.run_smart()

    return

def write_slurm_script_python(runfiles, name="smart_run", subname="smart_submit.csh",
                       workdir = "",
                       nodes = 1, mem = "500G", walltime = "0", ntasks = 28,
                       account = "vsm", submit = False, rm_after_submit = False,
                       preamble = ['module load icc_18',
                                   'module load parallel-20170722']):
    """
    Write a hyak SLURM bash script for simple python scripts

    Parameters
    ----------
    runfiles : array of strs
        Array of all python scripts to run
    name : str
        Name of the job
    subname : str
        Name of the bash submission script to generate
    workdir : str
        Working directory
    nodes : int
        Number of nodes
    mem : str
        Requested memory
    walltime : str
        Walltime to allow simulation to run for ("0" is indefinite)
    ntasks : int
        Number of processors to allow usage of
    account : str
        Name of account and partition on hyak
    submit : bool
        Set to submit the job
    rm_after_submit : bool
        Set to remove script immediately after submission
    preamble : list
        Bash statements to call before running python script
        (e.g. ['module load icc_18', 'source activate my_root'])
    """
# Get absolute path of workdir
    abs_place = os.path.abspath(workdir)

    newfile = os.path.join(abs_place, subname)

    f = open(newfile, 'w')

    f.write('#!/bin/bash\n')
    f.write('#!/bin/bash\n')
    f.write('#!/bin/bash\n')
    f.write('#!/bin/bash\n')
    f.write('\n')
    f.write('#SBATCH --job-name=%s\n' %name)
    f.write('\n')
    f.write('#SBATCH --account=%s\n' %account)
    f.write('#SBATCH --partition=%s\n' %account)
    f.write('\n')
    f.write('#SBATCH --nodes=%i\n' %nodes)
    ###SBATCH --ntasks-per-node=28 ### not necessarily required, so I'm not using it in this one
    f.write('#SBATCH --time=%s\n' %walltime)  ### this basically allows it to run for 365 days. Note it seems to otherwise only accept hours:mins:sec
    f.write('#SBATCH --mem=%s\n' %mem) ### apparently you only get the memory you ask for
    f.write('\n')
    f.write('#SBATCH --ntasks=%i\n' %ntasks)
    f.write('#SBATCH --exclusive\n')
    f.write('\n')
    f.write('#SBATCH --workdir=%s\n' %abs_place)
    f.write('\n')
    f.write('ulimit -s unlimited\n')

    # Loop over preamble statements
    for i in range(len(preamble)):
        f.write('%s\n' %preamble[i])

    f.write('\n')

    for runfile in runfiles:
        f.write('python %s\n' %runfile)

    f.close()

    # Set permissions to allow execute
    st = os.stat(newfile)
    os.chmod(newfile, st.st_mode | stat.S_IEXEC)

    # Submit the run to the queue?
    if submit:

        subprocess.check_call(["sbatch", "-p", "vsm", "-A", "vsm", newfile])

        # Delete the bash script after submitting
        if rm_after_submit:

            os.system('rm %s' %newfile)

    return
