# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Contains:
#	- Container env for building RPMs

######## CONTAINER ENV ########

# General targets
.PHONY: containerized-rpmbuild blah neha

neha:
	if [ ! -z $(MODE) ]; then \
		echo not empty; \
	fi;
	@echo $(foo)

blah:
	$(if $(MODE),)
	@echo i m here
	$(endif)
	@echo  run_container_args is ***** **** $(MYARGS)
	$(SCRIPTS_DIR)/containerized-build/create_container_build.sh -p $(REPO_PATH) $(MYARGS)

containerized-rpmbuild:
	$(SCRIPTS_DIR)/containerized-build/create_container_build.sh -p $(REPO_PATH) -m $(MODE) -v $(VERSION)