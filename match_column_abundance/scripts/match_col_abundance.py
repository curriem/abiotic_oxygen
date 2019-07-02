import numpy as np


def column_abundance(p, T, fi):
    # pi = ni * k * T
    # ni = pi / (k * T)
    # k = 1.381e-23 J/K (joules per kelvin)
    # k = 1.381e-23 kg m^2 / s^2 / K
    # 1 Pa = 1 N/m^2 = 1 kg / (m s^2)
    # k = 1.381e-23 Pa / m / K
    # k = 1.381e-23 Pa / m / K * (1 bar / 100000 Pa)
    # k = 1.381e-28 bar / m / K
    # T [K]
    # p [bar]
    #
    k = 1.381E-23 # J/K (joules per kelvin)

    pi = p * fi
    pi *= 100000 # convert bars to pascals

    ni = pi / (k * T)

    return sum(ni)

earth_factor = 0.0013
pt_fl_earth = '../../earth_standard_icrccm_vmix.pt'

pt_data_earth = np.genfromtxt(pt_fl_earth, skip_header=1)

earth_pressure = pt_data_earth[:, 0]
earth_temperature = pt_data_earth[:, 1]
earth_f_o2 = pt_data_earth[:, 8] * earth_factor


