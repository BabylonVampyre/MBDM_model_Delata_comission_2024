#!/bin/bash

#SBATCH --job-name="Sobol_nopolicy"
#SBATCH --time=00:20:00
#SBATCH --ntasks=10
#SBATCH --cpus-per-task=1
#SBATCH --partition=compute
#SBATCH --mem-per-cpu=4GB
#SBATCH --account=education-tpm-msc-epa

module load 2023r1
module load openmpi
module load python
module load py-numpy
module load py-scipy
module load py-pandas
module load py-mpi4py
module load py-copy
module load py-pip


pip install --user --upgrade ema_workbench
pip install --user networkx


mpiexec -n 1 python3 GSA_sobol.py