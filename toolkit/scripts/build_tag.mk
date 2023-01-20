# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Contains:
#	- Tags which define the current build

######## BUILD DEFINES ########

DIST_TAG           ?= .cm2
# Running 'git' as the owner of the repo, so it doesn't complain about the repo not belonging to root.
BUILD_NUMBER       ?= $(call shell_real_build_only, runuser -u $$(stat -c "%U" $(PROJECT_ROOT)) -- git rev-parse --short HEAD)
# an empty BUILD_NUMBER breaks the build later on
ifeq ($(BUILD_NUMBER),)
   BUILD_NUMBER = non-git
endif
RELEASE_MAJOR_ID   ?= 2.0
# use minor ID defined in file (if exist) otherwise define it
# note this file must be single line
ifneq ($(wildcard $(OUT_DIR)/version-minor-id.config),)
   RELEASE_MINOR_ID ?= .$(shell cat $(OUT_DIR)/version-minor-id.config)
else
   RELEASE_MINOR_ID ?= .$(shell date +'%Y%m%d.%H%M')
endif
RELEASE_VERSION    ?= $(RELEASE_MAJOR_ID)$(RELEASE_MINOR_ID)

# Image tag - empty by default. Does not apply to the initrd.
IMAGE_TAG          ?=
