INIT_BATCH=(1 5 10 50)
INIT_EPOCHS=(50 100 500 1000)
LR=(0.000001 0.0000001 0.00000001 0.000000001)
LRPT=(0.000001 0.0000001 0.00000001 0.000000001)
EPOCHS_PER_BATCH=(10 100)
GAME_BATCH=(50 200)


COMMAND="sbatch ./run_single_test.sh -pt_test"

echo "python3 ia/gen_dataset.py && ("
echo $COMMAND

for i in "${INIT_BATCH[@]}"
do
    echo "$COMMAND"" -ib ""$i"
done

for i in "${INIT_EPOCHS[@]}"
do
    echo "$COMMAND"" -ie ""$i"
done

for i in "${LRPT[@]}"
do
    echo "$COMMAND"" -lrpt ""$i"
done

#for i in "${LR[@]}"
#do
#    echo "$COMMAND"" -lr ""$i"
#done
#
#for i in "${EPOCHS_PER_BATCH[@]}"
#do
#    echo "$COMMAND"" -eb ""$i"
#done
#
#for i in "${GAME_BATCH[@]}"
#do
#    echo "$COMMAND"" -gb ""$i"
#done

echo ")"
