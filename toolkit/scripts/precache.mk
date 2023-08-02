# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Contains:
#	- Tools to fully hydrate the rpm cache from upstream repos with the any versions that match local .spec files

.PHONY: pre-cache

downloaded_files = $(CACHED_RPMS_DIR)/precache/downloaded_files.txt
precached_state_dir = $(CACHED_RPMS_DIR)/precache

# We always want to run the precache script, it will decide if it needs to download anything and update the flag file if
# it does, so add the phony target as a dependency to the flag file
.PHONY: precache_always_run_phony
pre-cache: $(STATUS_FLAGS_DIR)/precache.flag
$(STATUS_FLAGS_DIR)/precache.flag: $(SCRIPTS_DIR)/precache.sh $(rpms_snapshot) precache_always_run_phony 
	[ -f $@ ] || touch $@ # Create the flag file if it doesn't exist in case we don't download anything
	$(SCRIPTS_DIR)/precache.sh "$(rpms_snapshot)" "$(precached_state_dir)" "$(CACHED_RPMS_DIR)/cache" "$(downloaded_files)" $(PACKAGE_URL_LIST) && \
	if [ -s "$(downloaded_files)" ]; then \
		touch $@; \
	fi