# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Contains:
#	- Tags which define the current build

######## BUILD DEFINES ########

DIST_TAG           ?= .cm2
# Running 'git' as the owner of the repo, so it doesn't complain about the repo not belonging to root.
BUILD_NUMBER       ?= $(call shell_real_build_only, if [ -n "$$UID" ] && [ "$$UID" -eq 0 ]; then runuser -u $$(stat -c "%U" $(PROJECT_ROOT)) -- git rev-parse --short HEAD; else git rev-parse --short HEAD; fi)
# an empty BUILD_NUMBER breaks the build later on
ifeq ($(BUILD_NUMBER),)
   BUILD_NUMBER = non-git
endif
# Staticly define BUILD_NUMBER so it is set only once
BUILD_NUMBER := $(BUILD_NUMBER)
RELEASE_MAJOR_ID   ?= 2.0
# use minor ID defined in file (if exist) otherwise define it
# note this file must be single line
ifneq ($(wildcard $(OUT_DIR)/version-minor-id.config),)
   RELEASE_MINOR_ID ?= .$(shell cat $(OUT_DIR)/version-minor-id.config)
else
   RELEASE_MINOR_ID ?= .$(shell date +'%Y%m%d.%H%M')
endif
RELEASE_VERSION    ?= $(RELEASE_MAJOR_ID)$(RELEASE_MINOR_ID)

# Re-assign RELEASE_VERSION so it is set statically only once
# This is to prevent the version from changing as time passes during the build
RELEASE_VERSION := $(RELEASE_VERSION)

# Image tag - empty by default. Does not apply to the initrd.
IMAGE_TAG          ?=
