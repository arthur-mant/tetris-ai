#!/bin/bash
#SBATCH -t 3-00:00:00
#SBATCH -o out.txt
#SBATCH --job-name=NOME_JOB
srun python ~/tetris-ia/ia/main.py
