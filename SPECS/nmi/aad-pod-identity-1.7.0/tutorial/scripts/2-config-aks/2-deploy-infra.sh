#!/bin/bash

cd "${0%/*}"

set -e
set -x

kubectl apply -f ../../../../deploy/infra/deployment.yaml