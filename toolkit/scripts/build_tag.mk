# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Contains:
#	- Tags which define the current build

######## BUILD DEFINES ########

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

##help:var:DIST_NAME_ABRV:<dist_name_abrv>=Basis of the distro macros. The abbreviation of the distro name and the major version are encoded into the go tools so that they can be used to create the distro specific macro '<DIST_NAME_ABRV> <dist_major_version_number>', where 'dist_major_version_number' is the major version number extracted from '<RELEASE_MAJOR_ID>'.
DIST_NAME_ABRV       ?= azl
dist_major_version_number := $(shell echo $(RELEASE_MAJOR_ID) | cut -d'.' -f1)
DIST_VERSION_MACRO := $(DIST_NAME_ABRV) $(dist_major_version_number)

##help:var:DIST_TAG:<dist_tag>=Distribution tag, defines the "dist" macro used by the specs. Default: '.<DIST_NAME_ABRV><dist_major_version_number>' e.g., ".azl3"
DIST_TAG            ?= .$(DIST_NAME_ABRV)$(dist_major_version_number)
