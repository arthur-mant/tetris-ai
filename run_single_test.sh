#!/bin/bash
#SBATCH -t 3-00:00:00
#SBATCH --job-name=TETRIS
#SBATCH -p gpu
#SBATCH --gres=gpu:1	
#SBATCH -c 8
#SBATCH --mem-per-cpu=50G
#SBATCH --qos=high

module load libraries/cuda/11.8
export XLA_FLAGS=--xla_gpu_cuda_data_dir=/cluster/libraries/cuda/11.8
export HDF5_USE_FILE_LOCKING='FALSE'

pipenv run python ~/tetris-ia/ia/main.py $@
