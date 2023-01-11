# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Contains:
#   - Definitions
#   - High Level Targets
#   - Submake Includes

######## DEFINITIONS ########

# Build targets
ifeq ($(origin CONFIG_FILE), undefined)
CONFIG_FILE             = $(toolkit_root)/imageconfigs/core-efi.json
$(warning CONFIG_FILE is undefined, defaulting to toolkit's core-efi.json.)
endif
CONFIG_BASE_DIR        ?= $(dir $(CONFIG_FILE))
PACKAGE_BUILD_LIST     ?=
PACKAGE_REBUILD_LIST   ?=
PACKAGE_IGNORE_LIST    ?=
SRPM_PACK_LIST         ?=

REBUILD_TOOLCHAIN               ?= n
INCREMENTAL_TOOLCHAIN           ?= n
ALLOW_TOOLCHAIN_DOWNLOAD_FAIL   ?= n
UPDATE_TOOLCHAIN_LIST           ?= n
REBUILD_PACKAGES                ?= y
DOWNLOAD_SRPMS                  ?= n
ALLOW_SRPM_DOWNLOAD_FAIL        ?= n
REBUILD_TOOLS                   ?= n
RUN_CHECK                       ?= n
USE_CCACHE                      ?= n
USE_PREVIEW_REPO                ?= n
DISABLE_UPSTREAM_REPOS          ?= n
TOOLCHAIN_CONTAINER_ARCHIVE     ?=
TOOLCHAIN_ARCHIVE               ?=
TOOLCHAIN_SOURCES_ARCHIVE       ?=
CACHE_DIR                       ?=
PACKAGE_CACHE_SUMMARY           ?=
IMAGE_CACHE_SUMMARY             ?=
INITRD_CACHE_SUMMARY            ?=
PACKAGE_ARCHIVE                 ?=
PACKAGE_BUILD_RETRIES           ?= 1
REFRESH_WORKER_CHROOT           ?= y
# Set to 0 to use the number of logical CPUs.
CONCURRENT_PACKAGE_BUILDS       ?= 0
# Set to 0 to print all available results.
NUM_OF_ANALYTICS_RESULTS        ?= 10
CLEANUP_PACKAGE_BUILDS          ?= y
USE_PACKAGE_BUILD_CACHE         ?= y
REBUILD_DEP_CHAINS              ?= y
HYDRATED_BUILD                  ?= n
DELTA_BUILD                     ?= n
TARGET_ARCH                     ?=

# Folder defines
toolkit_root     := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
TOOLS_DIR        ?= $(toolkit_root)/tools
TOOL_BINS_DIR    ?= $(toolkit_root)/out/tools
PREVIEW_REPO     ?= $(toolkit_root)/repos/mariner-official-preview.repo
RESOURCES_DIR    ?= $(toolkit_root)/resources
SCRIPTS_DIR      ?= $(toolkit_root)/scripts

PROJECT_ROOT     ?= $(realpath $(toolkit_root)/..)
BUILD_DIR        ?= $(PROJECT_ROOT)/build
OUT_DIR          ?= $(PROJECT_ROOT)/out
SPECS_DIR        ?= $(PROJECT_ROOT)/SPECS
CCACHE_DIR       ?= $(PROJECT_ROOT)/ccache

# Sub-folder defines
LOGS_DIR         ?= $(BUILD_DIR)/logs
PKGBUILD_DIR     ?= $(BUILD_DIR)/pkg_artifacts
CACHED_RPMS_DIR  ?= $(BUILD_DIR)/rpm_cache
BUILD_SRPMS_DIR  ?= $(BUILD_DIR)/INTERMEDIATE_SRPMS
MACRO_DIR        ?= $(BUILD_DIR)/macros
BUILD_SPECS_DIR  ?= $(BUILD_DIR)/INTERMEDIATE_SPECS
STATUS_FLAGS_DIR ?= $(BUILD_DIR)/make_status
CHROOT_DIR       ?= $(BUILD_DIR)/worker/chroot
IMAGEGEN_DIR     ?= $(BUILD_DIR)/imagegen

RPMRC_DIR        ?= $(MACRO_DIR)/usr/lib/rpm

PKGGEN_DIR       ?= $(TOOLS_DIR)/pkggen
TOOLKIT_BINS_DIR ?= $(TOOLS_DIR)/toolkit_bins

MANIFESTS_DIR      ?= $(RESOURCES_DIR)/manifests
META_USER_DATA_DIR ?= $(RESOURCES_DIR)/assets/meta-user-data
SSH_KEY_FILE       ?=

TOOLCHAIN_MANIFESTS_DIR      ?= $(MANIFESTS_DIR)/package

RPMS_DIR        ?= $(OUT_DIR)/RPMS
SRPMS_DIR       ?= $(OUT_DIR)/SRPMS
IMAGES_DIR      ?= $(OUT_DIR)/images

# If toolchain RPMs are being rebuilt locally, they belong with the other RPMs
ifeq ($(REBUILD_TOOLCHAIN),y)
   toolchain_rpms_dir := $(RPMS_DIR)
else
   toolchain_rpms_dir := $(CACHED_RPMS_DIR)/cache
endif

# External source server
SOURCE_URL         ?= https://cblmarinerstorage.blob.core.windows.net/sources/core

PACKAGE_URL_LIST   ?= https://packages.microsoft.com/cbl-mariner/$(RELEASE_MAJOR_ID)/prod/base/$(build_arch)
PACKAGE_URL_LIST   += https://packages.microsoft.com/cbl-mariner/$(RELEASE_MAJOR_ID)/prod/base/debuginfo/$(build_arch)
PACKAGE_URL_LIST   += https://packages.microsoft.com/cbl-mariner/$(RELEASE_MAJOR_ID)/prod/Microsoft/$(build_arch)
REPO_LIST          ?=
SRPM_URL_LIST      ?= https://packages.microsoft.com/cbl-mariner/$(RELEASE_MAJOR_ID)/prod/base/srpms

ifeq ($(USE_PREVIEW_REPO),y)
   PACKAGE_URL_LIST   += https://packages.microsoft.com/cbl-mariner/$(RELEASE_MAJOR_ID)/preview/base/$(build_arch)
   PACKAGE_URL_LIST   += https://packages.microsoft.com/cbl-mariner/$(RELEASE_MAJOR_ID)/preview/base/debuginfo/$(build_arch)
   PACKAGE_URL_LIST   += https://packages.microsoft.com/cbl-mariner/$(RELEASE_MAJOR_ID)/preview/Microsoft/$(build_arch)
   SRPM_URL_LIST      += https://packages.microsoft.com/cbl-mariner/$(RELEASE_MAJOR_ID)/preview/base/srpms
   ifneq ($(wildcard $(PREVIEW_REPO)),)
      override REPO_LIST += $(PREVIEW_REPO)
   else
      $(warning )
      $(warning ######################### WARNING #########################)
      $(warning 'USE_PREVIEW_REPO=y' set but '$(PREVIEW_REPO)' is missing. Regenerate toolkit's 'repos' directory. Remove 'USE_PREVIEW_REPO' for core builds.)
      $(warning ######################### WARNING #########################)
      $(warning )
   endif
endif

ifneq ($(strip $(SRPM_PACK_LIST)),)
LOCAL_SPECS = $(wildcard $(addprefix $(SPECS_DIR)/*/,$(addsuffix .spec,$(strip SRPM_PACK_LIST))))
else # Empty pack list, build all under $(SPECS_DIR)
LOCAL_SPECS = $(shell find $(SPECS_DIR)/ -type f -name '*.spec')
endif

LOCAL_SPEC_DIRS = $(foreach spec,$(LOCAL_SPECS),$(dir $(spec)))

CA_CERT     ?=
TLS_CERT    ?=
TLS_KEY     ?=

# Build defines
DIST_TAG           ?= .cm2
# Running 'git' as the owner of the repo, so it doesn't complain about the repo not belonging to root.
BUILD_NUMBER       ?= $(shell runuser -u $$(stat -c "%U" $(PROJECT_ROOT)) -- git rev-parse --short HEAD)
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

# panic,fatal,error,warn,info,debug,trace
LOG_LEVEL          ?= info
STOP_ON_WARNING    ?= n
STOP_ON_PKG_FAIL   ?= n
STOP_ON_FETCH_FAIL ?= n

######## HIGH LEVEL TARGETS ########

.PHONY: all clean
all: toolchain go-tools chroot-tools

######## SUBMAKE INCLUDES ########

# Misc function defines
# Variable prerequisite tracking
include $(SCRIPTS_DIR)/utils.mk

# Bootstrap the toolchain's compilers and other tools with:
#   toolchain, raw-toolchain, clean-toolchain, check-manifests, check-x86_64-manifests, check-aarch64-manifests
include $(SCRIPTS_DIR)/toolchain.mk

# go utilities with:
#   go-tools, clean-go-tools, go-tidy-all (tidy go utilities before committing) go-test-coverage
# chroot worker with:
#   chroot-tools clean-chroot-tools
# macro definitions with:
#   macro-tools clean-macro-tools
include $(SCRIPTS_DIR)/tools.mk

# Create SRPMS from local SPECS with:
#   input-srpms, clean-input-srpms
include $(SCRIPTS_DIR)/srpm_pack.mk

# Expand local SRPMS into sources and SPECS with:
#   expand-specs clean-expand-specs
include $(SCRIPTS_DIR)/srpm_expand.mk

# Create a package build workplan with:
#   workplan, clean-workplan clean-cache
# Build a package with:
#   build-packages clean-build-packages
# Either create or consume compressed folders of rpms with:
#   hydrate-rpms, compress-rpms, clean-compress-rpms, compress-srpms, clean-compress-srpms
include $(SCRIPTS_DIR)/pkggen.mk

# Create images with:
#   image, iso, clean-imggen
include $(SCRIPTS_DIR)/imggen.mk

# Create self contained toolkit archive contianing all the required tools with:
#   package-toolkit, clean-package-toolkit
include $(SCRIPTS_DIR)/toolkit.mk

# Each component provides specific clean implementations which clean depends on.
# They are guaranteed to run first and will verify there are no existing mount points
# left after a chroot.
clean:
	rm -rf $(OUT_DIR)
	rm -rf $(BUILD_DIR)
	rm -rf $(toolkit_root)/out

# output version number
get-version:
	@echo $(RELEASE_VERSION)
