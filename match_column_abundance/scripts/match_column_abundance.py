import numpy as np
import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument('-pt_fl', dest='pt_fl', type=str)
# parser.add_argument('-molecule', dest='molecule', type=str)
# args = parser.parse_args()

def calculate_ni(p, T, fi):

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

match_factors = np.arange(0, 0.1, 0.0000001)

pt_fl_earth = '../../earth_standard_icrccm_vmix.pt'
pt_fl_bulge = '/Users/mcurr/abiotic_oxygen/vary_cold_trap/pt_fls/cold_trap_0_1.pt'

pt_data_earth = np.genfromtxt(pt_fl_earth, skip_header=1)
pt_data_bulge = np.genfromtxt(pt_fl_bulge, skip_header=1)
new_pt_data = np.copy(pt_data_earth)

earth_pressure = pt_data_earth[:, 0]
earth_temperature = pt_data_earth[:, 1]
earth_f_o2 = pt_data_earth[:, 8]

bulge_pressure = pt_data_bulge[:, 0]
bulge_temperature = pt_data_bulge[:, 1]
bulge_f_o2 = pt_data_bulge[:, 8]

bulge_ni = calculate_ni(bulge_pressure, bulge_temperature, bulge_f_o2)

abs_sub_list = []
for match_factor in match_factors:
    modified_earth_f_o2 = earth_f_o2 * match_factor
    modified_earth_ni = calculate_ni(earth_pressure, earth_temperature, modified_earth_f_o2)
    abs_sub_list.append(abs(modified_earth_ni - bulge_ni))

min_match_factor_arg = np.argmin(abs_sub_list)
min_match_factor = match_factors[min_match_factor_arg]

min_earth_f_o2 = earth_f_o2 * min_match_factor

min_earth_ni = calculate_ni(earth_pressure, earth_temperature, min_earth_f_o2)

print 'earth:', min_earth_ni
print 'o2 bulge:', bulge_ni
print 'earth factor:', min_match_factor

new_earth_f_o2 = pt_data_earth[:, 8] * min_match_factor
new_pt_data[:, 8] = new_earth_f_o2

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
np.savetxt('../pt_fls/modified_earth_%s.pt' % str(min_match_factor).replace('.', '_'), new_pt_data, delimiter='   ', header=header, comments='')
