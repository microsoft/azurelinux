#!/bin/bash

set -e # stop on errors
set -x # print commands when they are executed


# this scripts sets up your azure subscription to enable AKS

az provider register -n Microsoft.Network
az provider register -n Microsoft.Storage
az provider register -n Microsoft.Compute
az provider register -n Microsoft.ContainerService
