INIT_EPOCHS=(100 1000)
EPOCHS_PER_BATCH=(5 20)
GAME_BATCH=(50 200)
LR=(0.001 0.0001 0.00001)

COMMAND="python ia/main.py -n"

echo "python ia/gen_dataset.py"
echo $COMMAND

for i in "${INIT_EPOCHS[@]}"
do
    echo "$COMMAND"" -ie ""$i"" --name ie""$i"
done

for i in "${EPOCHS_PER_BATCH[@]}"
do
    echo "$COMMAND"" -eb ""$i"" --name eb""$i"
done

for i in "${GAME_BATCH[@]}"
do
    echo "$COMMAND"" -gb ""$i"" --name gb""$i"
done

for i in "${LR[@]}"
do
    echo "$COMMAND"" -lr ""$i"" --name lr""$i"
done
