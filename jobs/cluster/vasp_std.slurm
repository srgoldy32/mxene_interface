#!/bin/bash
#SBATCH --job-name="Ti2C"
#comment = "bu"
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=24
#SBATCH --export=ALL                                                                                                                                                                   
#SBATCH --time=10:00:00      
#SBATCH -o output
#SBATCH -e error                                                                                                                                                                
# load the necessary modules
export OMP_NUM_THREADS=1

module load mpi/openmpi/gcc/4.1.4
module load libs/scalapack/gcc-ompi/2.1.0
module load compilers/gcc/13
module load apps/vasp/gcc-ompi-pl2/5.4.4


EXE=vasp_std

srun --mpi=pmi2 $EXE

