#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

_main() {
    { 
        source /etc/profile.d/conda.sh;
        conda create -y -n pytorch
        conda activate pytorch;
    } >> /dev/null
    "$@"
}

_main "$@"
