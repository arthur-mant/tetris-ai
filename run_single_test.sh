#!/bin/bash
#SBATCH -t 3-00:00:00
#SBATCH -o out.txt
#SBATCH -e err.txt
#SBATCH --job-name=TETRIS
#SBATCH -p gpu
#SBATCH --gres=gpu:1	
#SBATCH -c 8
#SBATCH --mem=32G 
#SBATCH --qos=high

module load libraries/cuda/11.8
export XLA_FLAGS=--xla_gpu_cuda_data_dir=/cluster/libraries/cuda/11.8
pipenv run python ~/tetris-ia/ia/main.py -pt
