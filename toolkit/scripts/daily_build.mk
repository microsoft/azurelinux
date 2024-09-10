# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Contains:
#	- Configuration for getting daily build packages

# DAILY_BUILD_ID and DAILY_BUILD_REPO while similar are mutually exclusive.
#
# DAILY_BUILD_ID is points the build tools to the latest daily built
# packages as part of a tight local workflow.  The DAILY_BUILD_ID argument
# takes the form: V-v-YYYYMMDD where V-v is the Major-Minor branch or
# may be 'lkg' which will auto-detect the latest valid build.
#
# DAILY_BUILD_REPO also points to the latest daily built packages.  However
# this is intended for internal teams to access the packages at build time and
# runtime.  The argument takes the form of a repo file supplied by the
# Azure Linux Team's daily artifact feed.  The repo file may be provisioned
# in a downstream image so that it has access to the repo at runtime.  The
# DAILY_BUILD_REPO argument takes a path to the daily-mariner.repo file.

##help:var:DAILY_BUILD_ID:{'lkg',<build_id>}='lkg' will auto select latest daily build repo. An explicit ID of the form 'V-v-YYYYMMDD' where V-v is the Major-Minor branch is also supported.
DAILY_BUILD_ID ?=
##help:var:DAILY_BUILD_ID_UPDATE_MANIFESTS={y,n}=Update the toolchain manifests when using DAILY_BUILD_ID to match the daily build repo.
DAILY_BUILD_ID_UPDATE_MANIFESTS ?= y
##help:var:DAILY_BUILD_REPO={path to daily.repo}=Path to the daily build repo file to use.
DAILY_BUILD_REPO ?=

daily_lkg_workdir = $(BUILD_DIR)/daily_build_id

ifneq ($(DAILY_BUILD_ID),)
   ifneq ($(DAILY_BUILD_REPO),)
      $(error DAILY_BUILD_ID and DAILY_BUILD_REPO are mutually exclusive.)
   endif
endif

ifneq ($(DAILY_BUILD_ID),)
    ifeq ($(DAILY_BUILD_ID),lkg)
        $(call create_folder,$(daily_lkg_workdir))

        override DAILY_BUILD_ID := $(shell $(SCRIPTS_DIR)/get_lkg_id.sh $(daily_lkg_workdir))
        ifneq ($(.SHELLSTATUS),0)
            $(error Failed to auto detect DAILY_BUILD_ID)
        endif
    endif

    $(warning Using Daily Build $(DAILY_BUILD_ID))
    # Ensure build_arch is set
    ifeq ($(build_arch),)
       $(error build_arch must be set when using DAILY_BUILD_ID)
    endif
    # build_arch cannot be directly used because Azure storage do not support container names with '_' char
    daily_build_repo_name := $(subst _,-,daily-repo-$(DAILY_BUILD_ID)-$(build_arch))
    # The actual repo is found at <URL>/, while a duplicate copy of all the rpms can be found at <URL>/built_rpms_all/
    # Include both so that the tools that expect a valid repo work, while the tools that expect a basic URL also work.
    # The ordering is important, we want to always take the daily build versions of packages first since they are NOT
    # the same files as the official packages and will fail checksum validation.
    override PACKAGE_URL_LIST := https://mariner3dailydevrepo.blob.core.windows.net/$(daily_build_repo_name)/built_rpms_all \
                                    https://mariner3dailydevrepo.blob.core.windows.net/$(daily_build_repo_name) \
                                    $(PACKAGE_URL_LIST)
    override SRPM_URL_LIST    := https://mariner3dailydevrepo.blob.core.windows.net/$(daily_build_repo_name)/SRPMS \
                                    $(SRPM_URL_LIST)
endif

ifneq ($(DAILY_BUILD_REPO),)
   PACKAGE_ROOT := $(shell grep -m 1 "baseurl" $(DAILY_BUILD_REPO) | sed 's|baseurl=||g')
   $(warning )
   $(warning ######################### WARNING #########################)
   $(warning Using a Daily Build Repo at following location:)
   $(warning $(PACKAGE_ROOT))
   $(warning ######################### WARNING #########################)
   $(warning )
   override PACKAGE_URL_LIST  += $(PACKAGE_ROOT)/built_rpms_all
   override SRPM_URL_LIST     += $(PACKAGE_ROOT)/SRPMS
   override REPO_LIST         += $(DAILY_BUILD_REPO)
endif

# This does not use $(depend_DAILY_BUILD_ID) because that mechanism will not detect the conversion of "lkg" to a
# specific daily build ID since utils.mk runs before daily_build.mk.
.PHONY: daily_build_id_always_run_phony
$(STATUS_FLAGS_DIR)/daily_build_id.flag: daily_build_id_always_run_phony
	@if [ ! -f $@ ]; then \
		echo "Initializing daily build ID sanitization"; \
		touch $@; \
	fi && \
	if [ "$$(cat $@)" = "$(DAILY_BUILD_ID)" ]; then \
		exit 0; \
	fi && \
	echo "#### Daily build ID changed ('$$(cat $@)' -> '$(DAILY_BUILD_ID)') ####" && \
	echo $(DAILY_BUILD_ID) > $@
