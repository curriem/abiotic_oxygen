#!/bin/bash
#!/bin/bash
#!/bin/bash
#!/bin/bash

#SBATCH --job-name=o2_col

#SBATCH --account=vsm
#SBATCH --partition=vsm

#SBATCH --nodes=1
#SBATCH --time=100:00:00
#SBATCH --mem=500G

#SBATCH --ntasks=28
#SBATCH --exclusive

#SBATCH --workdir=/gscratch/vsm/mcurr/abiotic_oxygen/match_column_abundance/scripts

ulimit -s unlimited
module load icc_18
module load parallel-20170722

python run_experiment.py -place ../smart_outputs/cold_trap_0_1 -pt_fl ../pt_fls/cold_trap_0_1.pt
python run_experiment.py -place ../smart_outputs/earth -pt_fl ../pt_fls/earth_standard_icrccm_vmix.pt
