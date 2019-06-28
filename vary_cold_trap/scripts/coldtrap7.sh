#!/bin/bash
#!/bin/bash
#!/bin/bash
#!/bin/bash

#SBATCH --job-name=coldtrap7

#SBATCH --account=vsm
#SBATCH --partition=vsm

#SBATCH --nodes=1
#SBATCH --time=100:00:00
#SBATCH --mem=500G

#SBATCH --ntasks=28
#SBATCH --exclusive

#SBATCH --workdir=/gscratch/vsm/mcurr/abiotic_oxygen/vary_cold_trap/scripts

ulimit -s unlimited
module load icc_18
module load parallel-20170722

python run_experiment.py -place /gscratch/vsm/mcurr/abiotic_oxygen/vary_cold_trap/smart_outputs/cold_trap_0_006723357536499335 -pt_fl ../pt_fls/cold_trap_0_006723357536499335.pt
