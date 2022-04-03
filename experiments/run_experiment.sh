#!/bin/bash

mkdir -p ./pickles
mkdir -p ./logs
PICKLES_FOLDER_PATH=$(pwd)/pickles
LOGS_FOLDER_PATH=$(pwd)/logs
source $1 $2
