#!/bin/bash

for ((i=1; i<=$1; i++));
do
  pred_time=$(python3 ml_predict.py | awk -F' ' '{ print $4 }')
  echo "Prediction completed in $pred_time ms"
done 
echo "$1 predictions done"
