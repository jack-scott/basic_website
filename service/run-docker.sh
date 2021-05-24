#!/bin/bash
docker build -t my-python-app . && docker run --network="host" -it --rm --name my-running-app my-python-app
