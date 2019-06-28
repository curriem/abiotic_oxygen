#!/bin/bash
#!/bin/bash
#!/bin/bash
#!/bin/bash

#SBATCH --job-name=coldtrap3

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

python run_experiment.py -place /gscratch/vsm/mcurr/abiotic_oxygen/vary_cold_trap/smart_outputs/cold_trap_0_04520353656360243 -pt_fl ../pt_fls/cold_trap_0_04520353656360243.pt
python run_experiment.py -place /gscratch/vsm/mcurr/abiotic_oxygen/vary_cold_trap/smart_outputs/cold_trap_0_09236708571873861 -pt_fl ../pt_fls/cold_trap_0_09236708571873861.pt
python run_experiment.py -place /gscratch/vsm/mcurr/abiotic_oxygen/vary_cold_trap/smart_outputs/cold_trap_0_6210169418915616 -pt_fl ../pt_fls/cold_trap_0_6210169418915616.pt
python run_experiment.py -place /gscratch/vsm/mcurr/abiotic_oxygen/vary_cold_trap/smart_outputs/cold_trap_0_0020433597178569417 -pt_fl ../pt_fls/cold_trap_0_0020433597178569417.pt
python run_experiment.py -place /gscratch/vsm/mcurr/abiotic_oxygen/vary_cold_trap/smart_outputs/cold_trap_0_01373823795883263 -pt_fl ../pt_fls/cold_trap_0_01373823795883263.pt
