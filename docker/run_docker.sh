#!/bin/bash

#Want to bring this repo into the container
#Get location of this script
SCRIPT_LOC=$(readlink -f $0)
SCRIPT_FOLDER=$(dirname $SCRIPT_LOC)
REPO_LOC=$SCRIPT_FOLDER/.. #need to go one path back as this is in the docker folder

docker run --rm -it --name basicwebsite --volume $REPO_LOC:/home/user/basic_website alpine/basic_website bash
