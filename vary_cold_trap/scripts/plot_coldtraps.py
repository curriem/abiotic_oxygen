import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import smart
import coronagraph
import glob

####### fix plotting default values #######

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 12}

figure = {'figsize' : (14, 16)}

lines = {'linewidth' : 1}

matplotlib.rc('font', **font)
matplotlib.rc('figure', **figure)
matplotlib.rc('lines', **lines)

#############################################

def reduce_R(old_wl, old_flux):
    new_wl, dlam = cg.noise_routines.construct_lam(np.min(old_wl), np.max(old_wl), Res=R)
    new_flux = cg.downbin_spec(old_flux, old_wl, new_wl, dlam=dlam)
    return new_wl, new_flux

### gather pt files ###
cold_trap_pts = glob.glob('../pt_fls/cold_trap*')
no_o2_pt = '../pt_fls/no_oxygen.pt'
#######################

no_oxygen_rad_fl = '../smart_outputs/no_oxygen/case_6666_25000cm_toa.rad'
no_oxygen_rad_data = smart.readsmart.Rad(no_oxygen_rad_fl)
no_oxygen_rad_flux = no_oxygen_rad_data.pflux / no_oxygen_rad_data.sflux

no_oxygen_trnst_fl = '../smart_outputs/no_oxygen/case_6666_25000cm.trnst'
no_oxygen_trnst_data = smart.readsmart.Trnst(no_oxygen_trnst_fl)
no_oxygen_trnst_flux = no_oxygen_trnst_data.tdepth * 1e6

cold_trap_pts = sorted(cold_trap_pts)

band_wlmin = 1.26
band_wlmax = 1.28

plt.figure()
for pt_fl in cold_trap_pts[:1]:
    pt_name = pt_fl.split('/')[-1]
    pt_name = pt_name.split('.')[0]

    rad_fl = '../smart_outputs/' + pt_name + '/case_6666_25000cm_toa.rad'
    rad_data = smart.readsmart.Rad(rad_fl)
    rad_flux = rad_data.pflux / rad_data.sflux

    trnst_fl = '../smart_outputs/' + pt_name + '/case_6666_25000cm.trnst'
    trnst_data = smart.readsmart.Trnst(trnst_fl)
    trnst_flux = trnst_data.tdepth * 1e6

    wl = trnst_flux.lam

    wlrange = (wl > band_wlmin) & (wl < band_wlmax)

    plot_rad_flux = rad_flux[wlrange]
    plot_trnst_flux = trnst_flux[wlrange]
    plot_wl = wl[wlrange]

    plt.plot(plot_wl, plot_rad_flux)

plt.savefig('testing.png')
