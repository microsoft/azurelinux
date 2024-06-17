# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Contains:
#	- Create a preview repo file
#	- Configuration for getting preview packages

# Ensure USE_PREVIEW_REPO is set to 'y', else this file is not needed.
ifneq ($(USE_PREVIEW_REPO),y)
$(error USE_PREVIEW_REPO is not set to 'y' but preview.mk is included)
endif

######## REPO FILE MANAGEMENT/CREATION ########

preview_repo        := $(toolkit_root)/repos/azurelinux-official-preview.repo
# Intentionally not using $(SPECS) here to avoid issues with custom SPECS directories
preview_repo_source := $(PROJECT_ROOT)/SPECS/azurelinux-repos/azurelinux-official-preview.repo

# Stop immediately if the preview repo file is missing and cannot be created.
ifeq ($(wildcard $(preview_repo_source))$(wildcard $(preview_repo)),)
    $(warning )
    $(warning ######################### ERROR #########################)
    $(warning 'USE_PREVIEW_REPO=y' is set but all of the following failed:)
    $(warning - packaged default '$(preview_repo)' is missing)
    $(warning - backup source    '$(preview_repo_source)' is missing)
    $(warning ######################### ERROR #########################)
    $(error )
endif

# Copy the preview repo file to the expected repo location, but only if we  have a target to copy from.
ifeq ($(wildcard $(preview_repo_source)),)
$(preview_repo): ;
else
$(preview_repo): $(preview_repo_source)
	@echo "Regenerating preview repo file from '$<' to '$@'"
	mkdir -p $(dir $@)
	cp $< $@
endif

######## VARIABLE CONFIGURATION ########

override PACKAGE_URL_LIST   += https://packages.microsoft.com/azurelinux/$(RELEASE_MAJOR_ID)/preview/base/$(build_arch)
override PACKAGE_URL_LIST   += https://packages.microsoft.com/azurelinux/$(RELEASE_MAJOR_ID)/preview/base/debuginfo/$(build_arch)
override PACKAGE_URL_LIST   += https://packages.microsoft.com/azurelinux/$(RELEASE_MAJOR_ID)/preview/ms-oss/$(build_arch)
override SRPM_URL_LIST      += https://packages.microsoft.com/azurelinux/$(RELEASE_MAJOR_ID)/preview/base/srpms
override REPO_LIST += $(preview_repo)
