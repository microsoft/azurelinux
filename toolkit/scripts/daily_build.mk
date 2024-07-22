# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Contains:
#	- Configuration for getting daily build packages

# DAILY_BUILD_ID and DAILY_BUILD REPO while similar are mutually exclusive.
#
# DAILY_BUILD_ID is points the build tools to the latest daily built
# packages as part of a tight local workflow.  The DAILY_BUILD_ID argument
# takes the form: V-v-YYYYMMDD where V-v is the Major-Minor branch
#
# DAILY_BUILD_REPO also points to the latest daily built packages.  However
# this is intended for internal teams to access the packages at build time and
# runtime.  The argument takes the form of a repo file supplied by the
# Azure Linux Team's daily artifact feed.  The repo file may be provisioned
# in a downstream image so that it has access to the repo at runtime.  The
# DAILY_BUILD_REPO argument takes a path to the daily-mariner.repo file.
#
# their pipelines on a daily basis. The repo file may be provisioned to their image
ifneq ($(DAILY_BUILD_ID),)
   ifneq ($(DAILY_BUILD_REPO),)
      $(error DAILY_BUILD_ID and DAILY_BUILD_REPO are mutually exclusive.)
   endif
endif

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
      override PACKAGE_URL_LIST   += https://mariner3dailydevrepo.blob.core.windows.net/daily-repo-$(DAILY_BUILD_ID)-x86-64/built_rpms_all \
                                       https://mariner3dailydevrepo.blob.core.windows.net/daily-repo-$(DAILY_BUILD_ID)-x86-64
      override SRPM_URL_LIST      += https://mariner3dailydevrepo.blob.core.windows.net/daily-repo-$(DAILY_BUILD_ID)-x86-64/SRPMS
   else
      override PACKAGE_URL_LIST   += https://mariner3dailydevrepo.blob.core.windows.net/daily-repo-$(DAILY_BUILD_ID)-aarch64/built_rpms_all \
                                       https://mariner3dailydevrepo.blob.core.windows.net/daily-repo-$(DAILY_BUILD_ID)-aarch64
      override SRPM_URL_LIST      += https://mariner3dailydevrepo.blob.core.windows.net/daily-repo-$(DAILY_BUILD_ID)-aarch64/SRPMS
   endif
endif

ifeq ($(USE_PREVIEW_REPO),y)
   # Configure the preview repo
   include $(SCRIPTS_DIR)/preview.mk
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
