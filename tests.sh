INIT_BATCH=(5 50)
INIT_EPOCHS=(50 500)
EPOCHS_PER_BATCH=(10 100)
GAME_BATCH=(50 200)
LR=(0.000001 0.0000001 0.00000001 0.000000001)

COMMAND="sbatch ./run_single_test"

echo "python3 ia/gen_dataset.py"
echo $COMMAND

for i in "${INIT_BATCH[@]}"
do
    echo "$COMMAND"" -ib ""$i"
done

for i in "${INIT_EPOCHS[@]}"
do
    echo "$COMMAND"" -ie ""$i"
done

for i in "${EPOCHS_PER_BATCH[@]}"
do
    echo "$COMMAND"" -eb ""$i"
done

for i in "${GAME_BATCH[@]}"
do
    echo "$COMMAND"" -gb ""$i"
done

for i in "${LR[@]}"
do
    echo "$COMMAND"" -lr ""$i"
done
