# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Contains:
#	- Tags which define the current build

######## BUILD DEFINES ########

DIST_TAG           ?= .cm2
# Running 'git' as the owner of the repo, so it doesn't complain about the repo not belonging to root.
GIT_COMMIT_ID := $(call shell_real_build_only, if [ -n "$$UID" ] && [ "$$UID" -eq 0 ]; then runuser -u $$(stat -c "%U" $(PROJECT_ROOT)) -- git rev-parse --short HEAD; else git rev-parse --short HEAD; fi)
BUILD_NUMBER ?= $(GIT_COMMIT_ID)
# an empty BUILD_NUMBER breaks the build later on
ifeq ($(BUILD_NUMBER),)
   BUILD_NUMBER = non-git
endif
# Staticly define BUILD_NUMBER so it is set only once
BUILD_NUMBER := $(BUILD_NUMBER)
RELEASE_MAJOR_ID   ?= 3.0
DATETIME_AS_VERSION := $(shell date +'%Y%m%d.%H%M')
# use minor ID defined in file (if exist) otherwise define it
# note this file must be single line
ifneq ($(wildcard $(OUT_DIR)/version-minor-id.config),)
   RELEASE_MINOR_ID ?= .$(shell cat $(OUT_DIR)/version-minor-id.config)
else
   RELEASE_MINOR_ID ?= .$(DATETIME_AS_VERSION)
endif
RELEASE_VERSION    ?= $(RELEASE_MAJOR_ID)$(RELEASE_MINOR_ID)

# Re-assign RELEASE_VERSION so it is set statically only once
# This is to prevent the version from changing as time passes during the build
RELEASE_VERSION := $(RELEASE_VERSION)

# Image tag - empty by default. Does not apply to the initrd.
IMAGE_TAG          ?=

# Mariner Image Customizer version.
# This is using semantic versioning.
#
# IMAGE_CUSTOMIZER_VERSION should have the format:
#
#   <major>.<minor>.<patch>
#
# and should hold the value of the next (or current) official release, not the previous official
# release.
IMAGE_CUSTOMIZER_VERSION ?= 0.1.0
IMAGE_CUSTOMIZER_VERSION_PREVIEW ?= -dev.$(DATETIME_AS_VERSION)+$(GIT_COMMIT_ID)
IMAGE_CUSTOMIZER_FULL_VERSION := $(IMAGE_CUSTOMIZER_VERSION)$(IMAGE_CUSTOMIZER_VERSION_PREVIEW)
