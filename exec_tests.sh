python3 ia/gen_dataset.py
sbatch ./run_single_test
sbatch ./run_single_test -ib 5
sbatch ./run_single_test -ib 50
sbatch ./run_single_test -ie 50
sbatch ./run_single_test -ie 500
sbatch ./run_single_test -eb 10
sbatch ./run_single_test -eb 100
sbatch ./run_single_test -gb 50
sbatch ./run_single_test -gb 200
sbatch ./run_single_test -lr 0.000001
sbatch ./run_single_test -lr 0.0000001
sbatch ./run_single_test -lr 0.00000001
sbatch ./run_single_test -lr 0.000000001
