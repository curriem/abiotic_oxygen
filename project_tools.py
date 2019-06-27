import numpy as np
import os

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

def run_smart2(pt_fl, place, R=100000):

    # make the directory for the smart run
    try:
        os.mkdir(place)
    except OSError:
        pass

    # load pt file (relative import frim photochem directory)
    atm = smart.interface.Atmosphere.from_pt('../pt_fls/'+ptfile, atm_dir=place)

    # Set atmosphere parameters
    atm.set_dataframe_from_profiles()
    atm.write_atm()

    sim = smart.interface.Smart(tag='case', atmosphere=atm)
    sim.smartin.source = 3 # solar and thermal sources
    sim.smartin.out_format = 1 # no transit calculations

    # set the star as TRAPPIST-1
    sim.smartin.spec = '../../specs/TRAPPIST-1.dat'
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
