#!/bin/bash

# installing python requirements
echo "Installing python packages"
pip install -q -r requirements.txt

#downloading dataset
echo "Downloading dataset"
dataset_dir=$(pwd)/dataset
root_dir=$(pwd)

if [ -d "$dataset_dir" ]
then
  echo "Directory $dataset_dir already exists"
else
  mkdir $dataset_dir
  echo "Directory $dataset_dir created"
fi

if [ -f "$dataset_dir/mortality.zip" ]
then
  echo "Dataset already exists. Skip downloading"
else
  cd $dataset_dir

  export KAGGLE_USERNAME="jegorh"
  export KAGGLE_KEY="ec9aab331b8cc4701be23d5c1301f5ba"
  env KAGGLE_USERNAME="jegorh" KAGGLE_KEY="ec9aab331b8cc4701be23d5c1301f5ba" kaggle datasets download -d cdc/mortality

  unzip mortality.zip
  cd $root_dir
  echo "Done unzipping data"
fi

# running python scripts
echo "Running python"
python3 $root_dir/main.py $dataset_dir $root_dir/output
