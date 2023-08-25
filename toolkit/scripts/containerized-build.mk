# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Contains:
#	- Container env for building RPMs

######## CONTAINER ENV ########

# General targets
.PHONY: containerized-rpmbuild containerized-rpmbuild-help clean-containerized-rpmbuild

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
containerized_build_args += -bm "$(BUILD_MOUNT)"
endif

ifeq ($(ENABLE_REPO),y)
containerized_build_args += -r
endif

containerized-rpmbuild:
	$(SCRIPTS_DIR)/containerized-build/create_container_build.sh $(containerized_build_args)

containerized-rpmbuild-help:
	$(SCRIPTS_DIR)/containerized-build/create_container_build.sh -h

clean: clean-containerized-rpmbuild

clean-containerized-rpmbuild:
	$(SCRIPTS_DIR)/containerized-build/containerized-build_clean.sh $(BUILD_DIR)
