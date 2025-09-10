# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Contains:
#	- Container env for building RPMs

######## CONTAINER ENV ########

# General targets
.PHONY: containerized-rpmbuild containerized-rpmbuild-help

containerized_build_args :=
ifneq ($(MODE),)
containerized_build_args += -m ${MODE}
endif

ifneq ($(REPO_PATH),)
containerized_build_args += -p ${REPO_PATH}
endif

ifneq ($(VERSION),)
containerized_build_args += -v ${VERSION}
endif

ifneq ($(MOUNTS),)
containerized_build_args += -mo "$(MOUNTS)"
endif

ifneq ($(BUILD_MOUNT),)
containerized_build_args += -b ${BUILD_MOUNT}
endif

ifneq ($(EXTRA_PACKAGES),)
containerized_build_args += -ep "$(EXTRA_PACKAGES)"
endif

ifeq ($(ENABLE_REPO),y)
containerized_build_args += -r
endif

ifeq ($(KEEP_CONTAINER),y)
containerized_build_args += -k
endif

ifeq ($(QUIET),y)
containerized_build_args += -q
endif

containerized_tool_reqs := go-depsearch go-downloader go-grapher go-specreade go-srpmpacker

##help:target:containerized-rpmbuild=Launch containerized shell for inner-loop RPM building/testing.
containerized-rpmbuild: $(no_repo_acl) toolchain input-srpms graph chroot-tools $(containerized_tool_reqs)
	$(SCRIPTS_DIR)/containerized-build/create_container_build.sh $(containerized_build_args) -nr

containerized-rpmbuild-help:
	$(SCRIPTS_DIR)/containerized-build/create_container_build.sh -h
