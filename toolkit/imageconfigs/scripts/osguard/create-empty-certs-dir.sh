#!/bin/bash
# Script to create the ca-certificates directory to allow safe migration
# from Ubuntu hosts to Azure Linux hosts and avoid a creation of this directory
# at runtime under /usr

# Create the ca-certificates directory
mkdir -p /usr/local/share/ca-certificates
