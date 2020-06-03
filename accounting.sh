#!/usr/bin/bash

for i in {1..1000}
do
echo "Cycle $i "
  condor_ce_history  -cons '((GridJobStatus =?= "COMPLETED") && (JobStartDate =!= undefined) && (RoutedToJobId =?= undefined) && (RoutedFromJobId =!= undefined))'   > accounting-`date +"%m-%d-%y_%H-%M"`.dat
  gzip -9 accounting-`date +"%m-%d-%y_%H-%M"`.dat
  echo Done
  sleep 40000 
done
