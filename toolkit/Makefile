# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Contains:
#   - Definitions
#   - High Level Targets
#   - Submake Includes

######## DEFINITIONS ########

toolkit_root := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
SCRIPTS_DIR  ?= $(toolkit_root)/scripts

# Build targets
ifeq ($(origin CONFIG_FILE), undefined)
CONFIG_FILE             = $(toolkit_root)/imageconfigs/core-efi.json
$(warning CONFIG_FILE is undefined, defaulting to toolkit's core-efi.json.)
endif
CONFIG_BASE_DIR         ?= $(dir $(CONFIG_FILE))
PACKAGE_BUILD_LIST      ?=
PACKAGE_REBUILD_LIST    ?=
PACKAGE_IGNORE_LIST     ?=
SRPM_PACK_LIST          ?=

######## SET INCREMENTAL BUILD FLAGS ########

# Logic to auto configure build options for optimized builds
# These will set the default values for: REBUILD_TOOLS, USE_CCACHE, REBUILD_TOOLCHAIN, DELTA_BUILD, INCREMENTAL_TOOLCHAIN, ALLOW_TOOLCHAIN_DOWNLOAD_FAIL, and CLEAN_TOOLCHAIN_CONTAINERS
include $(SCRIPTS_DIR)/incremental_building.mk

######## SET REMAINING FLAGS ########

UPDATE_TOOLCHAIN_LIST           ?= n
REBUILD_PACKAGES                ?= y
DOWNLOAD_SRPMS                  ?= n
ALLOW_SRPM_DOWNLOAD_FAIL        ?= n
RUN_CHECK                       ?= n
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
CHECK_BUILD_RETRIES             ?= 1
REFRESH_WORKER_CHROOT           ?= y
# Set to 0 to use the number of logical CPUs.
CONCURRENT_PACKAGE_BUILDS       ?= 0
# Set to 0 to print all available results.
NUM_OF_ANALYTICS_RESULTS        ?= 10
CLEANUP_PACKAGE_BUILDS          ?= y
USE_PACKAGE_BUILD_CACHE         ?= y
REBUILD_DEP_CHAINS              ?= y
HYDRATED_BUILD                  ?= n
TARGET_ARCH                     ?=
ALLOW_TOOLCHAIN_REBUILDS        ?= n

# Folder defines
TOOLS_DIR        ?= $(toolkit_root)/tools
TOOL_BINS_DIR    ?= $(toolkit_root)/out/tools
PREVIEW_REPO     ?= $(toolkit_root)/repos/mariner-official-preview.repo
RESOURCES_DIR    ?= $(toolkit_root)/resources

PROJECT_ROOT     ?= $(realpath $(toolkit_root)/..)
BUILD_DIR        ?= $(PROJECT_ROOT)/build
OUT_DIR          ?= $(PROJECT_ROOT)/out
SPECS_DIR        ?= $(PROJECT_ROOT)/SPECS
CCACHE_DIR       ?= $(PROJECT_ROOT)/ccache

# Sub-folder defines
LOGS_DIR           ?= $(BUILD_DIR)/logs
PKGBUILD_DIR       ?= $(BUILD_DIR)/pkg_artifacts
CACHED_RPMS_DIR    ?= $(BUILD_DIR)/rpm_cache
BUILD_SRPMS_DIR    ?= $(BUILD_DIR)/INTERMEDIATE_SRPMS
MACRO_DIR          ?= $(BUILD_DIR)/macros
BUILD_SPECS_DIR    ?= $(BUILD_DIR)/INTERMEDIATE_SPECS
STATUS_FLAGS_DIR   ?= $(BUILD_DIR)/make_status
CHROOT_DIR         ?= $(BUILD_DIR)/worker/chroot
IMAGEGEN_DIR       ?= $(BUILD_DIR)/imagegen
TOOLCHAIN_RPMS_DIR ?= $(BUILD_DIR)/toolchain_rpms

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

CA_CERT     ?=
TLS_CERT    ?=
TLS_KEY     ?=

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

# Set the variables for build number, distro tag, etc
include $(SCRIPTS_DIR)/build_tag.mk

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

######## VARIABLE PRINTING ########

# Some common version information that is useful to gather. Generally should be run with the Make flag --quiet
get-version: printvar-RELEASE_VERSION
get-dist-tag: printvar-DIST_TAG
get-release-major: printvar-RELEASE_MAJOR_ID

# Make an easy way to print out the build variables. These must be the last entries in the makefile so that all other
# files have their variables inluded

# Print out all variables to stdout, either or of the form "<VALUE>" or the verbose form "varname: <VALUE>"
#   printvar-all-vars
#   printvar-verbose-all-vars

# Print a specific variable to stdout, using the same format as above
#   printvar-*
#   printvar-verbose-*

# Use these targets like so:  `my-var=$(make printvar-MY_VAR --quiet)`
# The --quiet flag is important to avoid printing extra output
.PHONY: printvar-all-vars printvar-verbose-all-vars

# Gather the variables we want to print out, removing any automatic .* variables, and the self reference, along with special characters that may interfere with Make
sanitize_variables = $(subst ',,$(subst ",,$(subst `,,$(subst \#,,$(subst $$,,$(subst :,,$1))))))
interesting_variables  = $(filter-out .% interesting_variables, $(sort $(call sanitize_variables,$(.VARIABLES))))

printvar-all-vars: $(foreach var,$(interesting_variables),printvar-$(var))
printvar-all-vars: ;
printvar-verbose-all-vars: $(foreach var,$(interesting_variables),printvar-verbose-$(var))
printvar-verbose-all-vars: ;

printvar-%: ; $(info $($(subst printvar-,,$@)))
	@: # We want to supress 'make: Nothing to be done for ...' so execute a command so make thinks it has done something
printvar-verbose-%: ; $(info $(subst printvar-verbose-,,$@): $($(subst printvar-verbose-,,$@)))
	@: # We want to supress 'make: Nothing to be done for ...' so execute a command so make thinks it has done something
