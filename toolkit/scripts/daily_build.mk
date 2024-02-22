# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Contains:
#	- Rules to update manifests
#	- Mechanism to update DAILY_BUILD_ID

TOOLCHAIN_MANIFEST ?= $(TOOLCHAIN_MANIFESTS_DIR)/toolchain_$(build_arch).txt
WORKER_CHROOT_MANIFEST = $(TOOLCHAIN_MANIFESTS_DIR)/pkggen_core_$(build_arch).txt

lkg_workdir = $(BUILD_DIR)/daily_build_id

######## CONFIGURE FLAGS ########

# DAILY_BUILD_ID is the main point of entry. It can be one of 'lkg', 'lkg-force', or <build-id>. Based on this selection 'LKG_MANIFESTS' and 'FORCE_MANIFEST_UPDATES' are selected by default. They may be overwritten if desired.

# LKG_MANIFESTS will update the manifest files to match the commit in the LKG file. This does not make sense for arbitrary build-ids however, so only default to 'y' for 'lkg' or 'lkg-force'

# PKG_MANIFEST_OVERWRITE will ignore local changes to the manifests and replace them with the LKG version.

##help:var:DAILY_BUILD_ID:{'lkg','lkg-force',<build_id>}='lkg' will auto select latest daily build repo. Unless LKG_MANIFESTS='n' is used, unmodifed manifests will be udpated to match. 'lkg-force' will overwrite changes. An explicit ID of the daily build repo can also be used.
DAILY_BUILD_ID ?=

##help:var:LKG_MANIFESTS:{y,n}='y' will auto update the manifests to the latest daily build if used in conjunction with DAILY_BUILD_ID='lkg' or 'lkg-force'.
ifneq (, $(filter $(DAILY_BUILD_ID),lkg lkg-force))
LKG_MANIFESTS ?= y
else
LKG_MANIFESTS ?= n
endif

##help:var:FORCE_MANIFEST_UPDATES:{y,n}='n' will not overwrite the manifests if they have local changes. 'y' will overwrite the manifests. Defaults to 'y' if DAILY_BUILD_ID='lkg-force'.
PKG_MANIFEST_OVERWRITE ?= $(if $(filter lkg-force,$(DAILY_BUILD_ID)),y,n)

######## CALCULATE LKG ID ########

ifneq (, $(filter $(DAILY_BUILD_ID),lkg lkg-force))
$(warning Auto detecting DAILY_BUILD_ID based on the latest known good build)
override DAILY_BUILD_ID := $(shell $(SCRIPTS_DIR)/get_lkg_id.sh $(lkg_workdir))
ifneq ($(.SHELLSTATUS),0)
$(error Failed to auto detect DAILY_BUILD_ID)
endif # .SHELLSTATUS
endif # DAILY_BUILD_ID

######## MANIFEST UPDATE ########

# Update the toolchain manifests
.PHONY: update-toolchain-manifests
ifeq ($(LKG_MANIFESTS),y)
.PHONY: update_manifest_always_run_phony
update-toolchain-manifests: $(TOOLCHAIN_MANIFEST) $(WORKER_CHROOT_MANIFEST)
$(call create_folder,$(lkg_workdir))
force_manifest_updates=$(if $(filter y,$(PKG_MANIFEST_OVERWRITE)),true,false)
$(TOOLCHAIN_MANIFEST) $(WORKER_CHROOT_MANIFEST): update_manifest_always_run_phony
	$(SCRIPTS_DIR)/update_manifest.sh $@ $(build_arch) $(lkg_workdir) $(force_manifest_updates)
else # LKG_MANIFEST y
update-toolchain-manifest:
endif


######## DAILY BUILD ID ########

ifneq ($(DAILY_BUILD_ID),)
   $(warning Using Daily Build $(DAILY_BUILD_ID))
   # Ensure build_arch is set
   ifeq ($(build_arch),)
      $(error build_arch must be set when using DAILY_BUILD_ID)
   endif
   # build_arch cannot be directly used because Azure storage do not support container names with '_' char
   ifeq ($(build_arch),x86_64)
      # The actual repo is found at <URL>/, while a duplicate copy of all the rpms can be found at <URL>/built_rpms_all/
      # Include both so that the tools that expect a valid repo work, while the tools that expect a basic URL also work.
      override PACKAGE_URL_LIST   := https://mariner3dailydevrepo.blob.core.windows.net/daily-repo-$(DAILY_BUILD_ID)-x86-64/built_rpms_all \
                                       https://mariner3dailydevrepo.blob.core.windows.net/daily-repo-$(DAILY_BUILD_ID)-x86-64
      override SRPM_URL_LIST      := https://mariner3dailydevrepo.blob.core.windows.net/daily-repo-$(DAILY_BUILD_ID)-x86-64/SRPMS
   else
      override PACKAGE_URL_LIST   := https://mariner3dailydevrepo.blob.core.windows.net/daily-repo-$(DAILY_BUILD_ID)-aarch64/built_rpms_all \
                                       https://mariner3dailydevrepo.blob.core.windows.net/daily-repo-$(DAILY_BUILD_ID)-aarch64
      override SRPM_URL_LIST      := https://mariner3dailydevrepo.blob.core.windows.net/daily-repo-$(DAILY_BUILD_ID)-aarch64/SRPMS
   endif
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
