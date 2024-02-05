#!/bin/bash

# cleanup symlinks created by the toolkit that are not needed for base images
rm -rf /srv

# cleanup any logs that may have been created during the build
rm -rf /var/log/*
