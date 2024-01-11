#!/bin/bash

_main() {
    { 
        source /etc/profile.d/conda.sh;
        conda create -y -n pytorch
        conda activate pytorch;
    } >> /dev/null
    "$@"
}

_main "$@"
