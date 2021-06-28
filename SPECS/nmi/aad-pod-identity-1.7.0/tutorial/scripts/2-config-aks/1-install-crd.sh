#!/bin/bash

cd "${0%/*}"

set -e
set -x

kubectl apply -f ../../../../crd/azureAssignedIdentityCrd.yaml
kubectl apply -f ../../../../crd/azureIdentityBindingCrd.yaml
kubectl apply -f ../../../../crd/azureIdentityCrd.yaml