#!/bin/bash

if [[ "$1" == nbft* ]] && [[ "$2" == "up" ]]; then
    systemctl start nvmf-connect-nbft.service
fi
