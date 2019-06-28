import project_tools
import numpy as np
import glob
import sys

place = '/gscratch/vsm/mcurr/abiotic_oxygen/vary_cold_trap/smart_outputs/'
pt_fl_dir = sys.argv[1]
def chunks(L, n):
    """ Yield successive n-sized chunks from L.
    """
    for i in xrange(0, len(L), n):
        yield L[i:i+n]

name = 'coldtrap'

pt_fls = glob.glob(pt_fl_dir + '/*')
len_chunks = 5

pt_fls_chunks = np.array(list(chunks(pt_fls, len_chunks)))

for n, chunk in enumerate(pt_fls_chunks):
        runfiles = []
        for pt_file in chunk:
            pt_file_name = pt_file.split('/')[-1]
            print pt_file
            temp_place = place + pt_file_name.split('.')[0]
            runfile = 'run_experiment.py -place %s -pt_fl %s' % (temp_place, pt_file)
            runfiles.append(runfile)


        project_tools.write_slurm_script_python(runfiles,
                                                name=name+str(n+1),
                                                subname=name+str(n+1)+'.sh',
                                                workdir='./',
                                                walltime='100:00:00')
