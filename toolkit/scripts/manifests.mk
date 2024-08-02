# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Contains:
#   - Optional mechanisms for regenerating the toolchain manifests

TOOLCHAIN_MANIFEST           ?= $(TOOLCHAIN_MANIFESTS_DIR)/toolchain_$(build_arch).txt
WORKER_CHROOT_MANIFEST       ?= $(TOOLCHAIN_MANIFESTS_DIR)/pkggen_core_$(build_arch).txt

# We use the contents of the manifests to derive some makefile recipes so we need to ensure they are up to date. It
# is not sufficient to add a recipe to update the manifests, they must be updated prior to the makefile being parsed
# sicne we use them as input to create recipes. A shell command is used to update the manifests if they are out of date.
ifeq ($(DAILY_BUILD_ID_UPDATE_MANIFESTS),y)
    ifneq ($(DAILY_BUILD_ID),)
        $(call create_folder,$(daily_lkg_workdir))

        manifest_exit_status := $(call shell_real_build_only, $(SCRIPTS_DIR)/update_manifest.sh $(TOOLCHAIN_MANIFEST) $(build_arch) $(daily_lkg_workdir) $(DAILY_BUILD_ID) 1>&2 ; echo $$?)
        ifneq ($(manifest_exit_status),0)
            $(error Failed to auto update manifest '$(TOOLCHAIN_MANIFEST)' with DAILY_BUILD_ID '$(DAILY_BUILD_ID)')
        endif

        manifest_exit_status := $(call shell_real_build_only, $(SCRIPTS_DIR)/update_manifest.sh $(WORKER_CHROOT_MANIFEST) $(build_arch) $(daily_lkg_workdir) $(DAILY_BUILD_ID) 1>&2 ; echo $$?)
        ifneq ($(manifest_exit_status),0)
            $(error Failed to auto update manifest '$(WORKER_CHROOT_MANIFEST) with DAILY_BUILD_ID '$(DAILY_BUILD_ID)')
        endif
    endif
endif
