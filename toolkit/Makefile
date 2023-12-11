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
##help:var:CONFIG_FILE:<config_path>=Path to image configuration file to use. Will add package dependencies and define final image generated.
CONFIG_FILE             ?=
CONFIG_BASE_DIR         ?= $(dir $(CONFIG_FILE))
PACKAGE_BUILD_LIST      ?=
##help:var:PACKAGE_REBUILD_LIST:<spec_list>=List of space-separated spec folders to force rebuild. Must not overlap with "PACKAGE_IGNORE_LIST". Example: PACKAGE_REBUILD_LIST="kernel go which".
PACKAGE_REBUILD_LIST    ?=
##help:var:PACKAGE_IGNORE_LIST:<spec_list>=List of space-separated spec folders to ignore during the build. Must not overlap with "PACKAGE_REBUILD_LIST", may overlap with "PACKAGE_BUILD_LIST". Example: PACKAGE_IGNORE_LIST="zlib".
PACKAGE_IGNORE_LIST     ?=
##help:var:SRPM_PACK_LIST:<spec_list>=List of space-separated spec folders inside "SPECS_DIR" to analyze for the build. If empty, all items inside the "SPECS_DIR" will be analyzed. Example: SRPM_PACK_LIST="kernel go which".
SRPM_PACK_LIST          ?=
##help:var:TEST_RUN_LIST:<spec_list>=List of space-separated spec folders to consider for package tests. Specs from the listed folders MUST contain the "%check" section. If empty, all testable items from "SRPM_PACK_LIST" will be considered. Will not re-test previously built packages. Example: TEST_RUN_LIST="libguestfs zlib".
TEST_RUN_LIST           ?=
##help:var:TEST_RERUN_LIST:<spec_list>=List of space-separated spec folders to force running a package test for. Specs from the listed folders MUST contain the "%check" section. Must not overlap with "TEST_IGNORE_LIST". Example: TEST_RERUN_LIST="libguestfs zlib".
TEST_RERUN_LIST         ?=
##help:var:TEST_IGNORE_LIST:<spec_list>=List of space-separated spec folders to ignore for package tests. Must not overlap with "TEST_RERUN_LIST", may overlap with "TEST_RUN_LIST". Example: TEST_IGNORE_LIST="acl".
TEST_IGNORE_LIST        ?=

######## SET INCREMENTAL BUILD FLAGS ########

# Logic to auto configure build options for optimized builds
# These will set the default values for: REBUILD_TOOLS, MAX_CPU, REBUILD_TOOLCHAIN, DELTA_BUILD, INCREMENTAL_TOOLCHAIN, ALLOW_TOOLCHAIN_DOWNLOAD_FAIL, and CLEAN_TOOLCHAIN_CONTAINERS
include $(SCRIPTS_DIR)/incremental_building.mk

######## SET REMAINING FLAGS ########

UPDATE_TOOLCHAIN_LIST                ?= n
REBUILD_PACKAGES                     ?= y
DOWNLOAD_SRPMS                       ?= n
ALLOW_SRPM_DOWNLOAD_FAIL             ?= n
RUN_CHECK                            ?= n
USE_PREVIEW_REPO                     ?= n
DISABLE_UPSTREAM_REPOS               ?= n
DISABLE_DEFAULT_REPOS                ?= n
TOOLCHAIN_CONTAINER_ARCHIVE          ?=
TOOLCHAIN_ARCHIVE                    ?=
TOOLCHAIN_SOURCES_ARCHIVE            ?=
CACHE_DIR                            ?=
PACKAGE_CACHE_SUMMARY                ?=
IMAGE_CACHE_SUMMARY                  ?=
INITRD_CACHE_SUMMARY                 ?=
PACKAGE_ARCHIVE                      ?=
PACKAGE_BUILD_RETRIES                ?= 1
CHECK_BUILD_RETRIES                  ?= 1
REFRESH_WORKER_CHROOT                ?= y
# Set to 0 to use the number of logical CPUs.
CONCURRENT_PACKAGE_BUILDS            ?= 0
# Set to 0 to print all available results.
NUM_OF_ANALYTICS_RESULTS             ?= 10
CLEANUP_PACKAGE_BUILDS               ?= y
USE_PACKAGE_BUILD_CACHE              ?= y
REBUILD_DEP_CHAINS                   ?= y
HYDRATED_BUILD                       ?= n
TARGET_ARCH                          ?=
ALLOW_TOOLCHAIN_REBUILDS             ?= n
RESOLVE_CYCLES_FROM_UPSTREAM         ?= n
IGNORE_VERSION_TO_RESOLVE_SELFDEP    ?= n
CACHED_PACKAGES_ARCHIVE              ?=
USE_CCACHE                           ?= n

# Tracing & Profiling support: https://go.dev/doc/diagnostics
ENABLE_CPU_PROFILE              ?= n
ENABLE_MEM_PROFILE              ?= n
ENABLE_TRACE                    ?= n

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
CCACHE_CONFIG    ?= $(RESOURCES_DIR)/manifests/package/ccache-configuration.json

# Sub-folder defines
LOGS_DIR           ?= $(BUILD_DIR)/logs
PKGBUILD_DIR       ?= $(BUILD_DIR)/pkg_artifacts
CACHED_RPMS_DIR    ?= $(BUILD_DIR)/rpm_cache
REPO_QUERY_DIR     ?= $(BUILD_DIR)/repo_query
BUILD_SRPMS_DIR    ?= $(BUILD_DIR)/INTERMEDIATE_SRPMS
MACRO_DIR          ?= $(BUILD_DIR)/macros
BUILD_SPECS_DIR    ?= $(BUILD_DIR)/INTERMEDIATE_SPECS
STATUS_FLAGS_DIR   ?= $(BUILD_DIR)/make_status
CHROOT_DIR         ?= $(BUILD_DIR)/worker/chroot
IMAGEGEN_DIR       ?= $(BUILD_DIR)/imagegen
TOOLCHAIN_RPMS_DIR ?= $(BUILD_DIR)/toolchain_rpms
TIMESTAMP_DIR      ?= $(BUILD_DIR)/timestamp
PROFILE_DIR        ?= $(BUILD_DIR)/profile

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

# Note on order of precedence: When a variable is passed from the commandline (i.e., make PACKAGE_URL_LIST="my list"), append
# assignments do not take affect without using 'override'. This means that all of the following PACKAGE_URL_LIST values will
# be ignored if the user sets any value.
##help:var:PACKAGE_URL_LIST:<urls_list>=Space-separated list of URLs to download toolchain RPM packages from, used to populate the toolchain packages if `REBUILD_TOOLCHAIN=n'. The URLs will replace the default set of URLs. Print default list with 'make -s printvar-PACKAGE_URL_LIST'.
PACKAGE_URL_LIST   ?= https://packages.microsoft.com/cbl-mariner/$(RELEASE_MAJOR_ID)/prod/base/$(build_arch)
PACKAGE_URL_LIST   += https://packages.microsoft.com/cbl-mariner/$(RELEASE_MAJOR_ID)/prod/base/debuginfo/$(build_arch)
PACKAGE_URL_LIST   += https://packages.microsoft.com/cbl-mariner/$(RELEASE_MAJOR_ID)/prod/Microsoft/$(build_arch)
REPO_LIST          ?=
SRPM_URL_LIST      ?= https://packages.microsoft.com/cbl-mariner/$(RELEASE_MAJOR_ID)/prod/base/srpms

ifneq ($(DAILY_BUILD_ID),)
   $(warning Using Daily Build $(DAILY_BUILD_ID))
   override PACKAGE_URL_LIST   := https://mariner3dailydevrepo.blob.core.windows.net/daily-repo-$(DAILY_BUILD_ID)-$(build_arch)/built_rpms_all
   override SRPM_URL_LIST      := https://mariner3dailydevrepo.blob.core.windows.net/daily-repo-$(DAILY_BUILD_ID)-$(build_arch)/SRPMS
else
   ifeq ($(USE_PREVIEW_REPO),y)
      override PACKAGE_URL_LIST   += https://packages.microsoft.com/cbl-mariner/$(RELEASE_MAJOR_ID)/preview/base/$(build_arch)
      override PACKAGE_URL_LIST   += https://packages.microsoft.com/cbl-mariner/$(RELEASE_MAJOR_ID)/preview/base/debuginfo/$(build_arch)
      override PACKAGE_URL_LIST   += https://packages.microsoft.com/cbl-mariner/$(RELEASE_MAJOR_ID)/preview/Microsoft/$(build_arch)
      override SRPM_URL_LIST      += https://packages.microsoft.com/cbl-mariner/$(RELEASE_MAJOR_ID)/preview/base/srpms
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
endif

CA_CERT     ?=
TLS_CERT    ?=
TLS_KEY     ?=

##help:var:LOG_LEVEL:{panic,fatal,error,warn,info,debug,trace}=Set logging level for toolkit.
# panic,fatal,error,warn,info,debug,trace
LOG_LEVEL          ?= info
STOP_ON_WARNING    ?= n
STOP_ON_PKG_FAIL   ?= n
STOP_ON_FETCH_FAIL ?= n

######## HIGH LEVEL TARGETS ########

.PHONY: all clean
all: toolchain go-tools chroot-tools

######## SUBMAKE INCLUDES ########

# General help information used by 'help' target; this should be included first so
# its help will be displayed at the top of the help output.
include $(SCRIPTS_DIR)/help.mk

# Misc function defines
# Variable prerequisite tracking
include $(SCRIPTS_DIR)/utils.mk

# Set up for the timestamp feature
include $(SCRIPTS_DIR)/timestamp.mk

# Profiling & Tracing feature
include $(SCRIPTS_DIR)/profile.mk

# Set the variables for build number, distro tag, etc
include $(SCRIPTS_DIR)/build_tag.mk

# go utilities with:
#   go-tools, clean-go-tools, go-tidy-all (tidy go utilities before committing) go-test-coverage
include $(SCRIPTS_DIR)/tools.mk

# Bootstrap the toolchain's compilers and other tools with:
#   toolchain, raw-toolchain, clean-toolchain, check-manifests, check-x86_64-manifests, check-aarch64-manifests
include $(SCRIPTS_DIR)/toolchain.mk

# chroot worker with:
#   chroot-tools clean-chroot-tools
# macro definitions with:
#   macro-tools clean-macro-tools
include $(SCRIPTS_DIR)/chroot.mk

# Create SRPMS from local SPECS with:
#   input-srpms, clean-input-srpms
include $(SCRIPTS_DIR)/srpm_pack.mk

# Create local build env for building RPMs with:
#   containerized-rpmbuild containerized-rpmbuild-help
include $(SCRIPTS_DIR)/containerized-build.mk

# Expand local SRPMS into sources and SPECS with:
#   expand-specs clean-expand-specs
include $(SCRIPTS_DIR)/srpm_expand.mk

# Create self contained toolkit archive contianing all the required tools with:
#   package-toolkit, clean-package-toolkit
include $(SCRIPTS_DIR)/toolkit.mk

# Fill the cache with rpms from the package server without using package manager or chroot with:
#   pre-cache
include $(SCRIPTS_DIR)/precache.mk

# Run repo query under chroot with:
# repo-query
include $(SCRIPTS_DIR)/repoquerywrapper.mk

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

# Add make targets for sodiff to determine if additional packages are required to be recompiled:
#  sodiff-check, build-summary, build-package-summary, fake-built-packages-list, sodiff-setup
include $(SCRIPTS_DIR)/analysis.mk

##help:target:clean=Clean all built files.
# Each component provides specific clean implementations which clean depends on.
# They are guaranteed to run first and will verify there are no existing mount points
# left after a chroot.
clean:
	rm -rf $(OUT_DIR)
	rm -rf $(BUILD_DIR)
	rm -rf $(toolkit_root)/out

######## VARIABLE PRINTING ########

# Display Makefile usage help; please consult $(SCRIPTS_DIR)/help.mk for documentation
# on the format of the comment annotations being extracted here.
.PHONY: help
help:
	@sed -ne '/@sed/!s/##help:desc://p' $(MAKEFILE_LIST)
	@sed -ne '/@sed/!s/##help:target-heading://p' $(MAKEFILE_LIST)
	@grep -h "^##help:target:" $(MAKEFILE_LIST) | sed -e "s/^##help:target:\([^=]\+\)=\(.*\)/\1|\2/" | sort | awk -F'|' '{ printf("  \033[3m%-26s\033[0m %s\n", $$1, $$2)}'
	@sed -ne '/@sed/!s/##help:var-heading://p' $(MAKEFILE_LIST)
	@grep -h "^##help:var:" $(MAKEFILE_LIST) | sed -e "s/^##help:var:\([^:]\+\):\([^=]*\)=\(.*\)/\1|\2|\3/" | sort | awk -F'|' '{ printf("  \033[92;3m%s\033[0m=%s\n      %s\n\n", $$1, $$2, $$3) }'
	@sed -ne '/@sed/!s/##help:example-heading://p' $(MAKEFILE_LIST)
	@grep -h "^##help:example:" $(MAKEFILE_LIST) | sed -e "s/^##help:example:\(.*\)/  \1/"

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
