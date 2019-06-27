import project_tools
import numpy as np

o2_abundance = 0.2
loc = 'upper'
cold_traps = np.logspace(-3, 0, 30)
for cold_trap in cold_traps:
    fl_name = 'cold_trap_%s.pt' % str(cold_trap).replace('.', '_')
    project_tools.make_pt_fl(loc, o2_abundance, '../pt_fls/' + fl_name, cold_trap)

# add an atmosphere with no oxygen
project_tools.make_pt_fl(o2_loc='mixed', o2_mixing_ratio=0., place='../pt_fls/no_oxygen.pt')
