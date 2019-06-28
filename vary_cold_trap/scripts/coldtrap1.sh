#!/bin/bash
#!/bin/bash
#!/bin/bash
#!/bin/bash

#SBATCH --job-name=coldtrap1

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

python run_experiment.py -place /gscratch/vsm/mcurr/abiotic_oxygen/vary_cold_trap/smart_outputs/cold_trap_0_4893900918477494 -pt_fl ../pt_fls/cold_trap_0_4893900918477494.pt
python run_experiment.py -place /gscratch/vsm/mcurr/abiotic_oxygen/vary_cold_trap/smart_outputs/cold_trap_0_14873521072935117 -pt_fl ../pt_fls/cold_trap_0_14873521072935117.pt
python run_experiment.py -place /gscratch/vsm/mcurr/abiotic_oxygen/vary_cold_trap/smart_outputs/cold_trap_0_001 -pt_fl ../pt_fls/cold_trap_0_001.pt
python run_experiment.py -place /gscratch/vsm/mcurr/abiotic_oxygen/vary_cold_trap/smart_outputs/cold_trap_0_0012689610031679222 -pt_fl ../pt_fls/cold_trap_0_0012689610031679222.pt
python run_experiment.py -place /gscratch/vsm/mcurr/abiotic_oxygen/vary_cold_trap/smart_outputs/cold_trap_0_057361525104486784 -pt_fl ../pt_fls/cold_trap_0_057361525104486784.pt
