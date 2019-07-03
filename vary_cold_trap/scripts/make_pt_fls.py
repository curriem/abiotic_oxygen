import project_tools
import numpy as np

cold_traps = np.arange(0, 1., 0.1)
o2_factors = np.arange(0, 0.5, 0.05)

for cold_trap in cold_traps:
    for o2_factor in o2_factors:


        fl_name = 'trop_%s_o2_%s.pt' % (str(cold_trap).replace('.', '_'), str(o2_factor).replace('.', '_'))
        project_tools.make_pt_fl('upper', o2_factor, '../pt_fls/' + fl_name, cold_trap)
