# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Contains:
#	- Create a preview repo file
#	- Create a daily build repo file

######## REPO FILE MANAGEMENT/CREATION ########

# Handle creating the preview repo file if it is missing

ifeq ($(USE_PREVIEW_REPO),y)
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
endif

# Generate the daily build repo file if DAILY_BUILD_ID is set

ifneq ($(DAILY_BUILD_ID),)
# The repo file for daily builds is generated from a template file as needed
daily_build_repo_source := $(MANIFESTS_DIR)/package/daily_build_repo.repo.template
daily_build_repo := $(daily_lkg_workdir)/daily_build.repo
override REPO_LIST += $(daily_build_repo)

# Ensure daily_build_repo_name was generated correctly
ifeq ($(daily_build_repo_name),)
    $(error daily_build_repo_name must be non-empty when using DAILY_BUILD_ID)
endif

# Copy the daily build repo file and replace the placeholder with the actual daily build ID
$(daily_build_repo): $(daily_build_repo_source) $(STATUS_FLAGS_DIR)/daily_build_id.flag
	@echo "Regenerating daily build repo file from '$<' to '$@'"
	mkdir -p $(dir $@)
	sed 's|{{.DAILY_REPO_NAME}}|$(daily_build_repo_name)|g' $< > $@
endif
