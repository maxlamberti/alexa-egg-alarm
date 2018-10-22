#!/bin/bash

git submodule foreach git pull origin master

source venv/bin/activate

if [ $1 = "all" ]; then
    zappa update dev
    zappa update production_eu
    zappa update production_us
    zappa update production_au
else
    for var in "$@"
    do
        zappa update ${var}
    done
fi