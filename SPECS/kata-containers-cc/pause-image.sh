#!/bin/bash

set -o errexit

sudo crictl pull --pod-config runtime.yaml mcr.microsoft.com/oss/kubernetes/pause:3.6
