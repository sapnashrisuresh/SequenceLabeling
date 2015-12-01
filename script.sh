#!/bin/bash
j=0

#replace the directory path for training/testing files here
for filename in ./data/test/*; do
	j=$[$j+1]
done

i=0

#replace the split size here
len=$(($j * 100/100))


#replace the directory path for training/testing files here
#run the baseline and advanced feature set separately
for filename in ./data/test/*; do
	if [ $i -lt $len ]; then
		python3 ./advanced_features.py $filename >> test_adv100.txt
		i=$[$i+1]
	else
		python3 ./advanced_features.py $filename >> train_adv25.txt
		i=$[$i+1]
	fi
done