#!/bin/bash

set -e # stop on errors

if [ -z "$RG" ]
then
      echo "Resource Group Name Not Set. Set the env variable with the following command:"
      echo "export RG = \"rg-name\" "
      return 1
else
     echo "Creating $RG resource group for this project"
fi


set -x # print commands when they are executed

az group create --name $RG --location eastus
