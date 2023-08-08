# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Contains:
#	- Tools to fully hydrate the rpm cache from upstream repos with the any versions that match local .spec files

.PHONY: pre-cache

precache_state_dir = $(CACHED_RPMS_DIR)/precache
precache_downloaded_files = $(precache_state_dir)/downloaded_files.txt

$(call create_folder,$(precache_state_dir))

# We always want to run the precache script, it will decide if it needs to download anything and update the flag file if
# it does, so add the phony target as a dependency to the flag file
.PHONY: precache_always_run_phony
pre-cache: $(STATUS_FLAGS_DIR)/precache.flag
$(STATUS_FLAGS_DIR)/precache.flag: $(go-precacher) $(rpms_snapshot) precache_always_run_phony 
	@if [ "$(DISABLE_UPSTREAM_REPOS)" = "y" ]; then \
		echo "ERROR: Upstream repos are disabled (DISABLE_UPSTREAM_REPOS=y), cannot precache rpms"; \
		exit 1; \
	fi
	[ -f $@ ] || touch $@ # Create the flag file if it doesn't exist in case we don't download anything
	#$(SCRIPTS_DIR)/precache.sh "$(rpms_snapshot)" "$(precached_state_dir)" "$(CACHED_RPMS_DIR)/cache" "$(downloaded_files)" $(PACKAGE_URL_LIST) && \
	$(go-precacher) \
		--snapshot "$(rpms_snapshot)" \
		--output-dir "$(CACHED_RPMS_DIR)/cache" \
		--output-summary-file "$(precache_downloaded_files)" \
		$(foreach url,$(PACKAGE_URL_LIST), --repo-url "$(url)") \
		--log-file=$(SRPM_BUILD_LOGS_DIR)/precacher.log \
		--log-level=$(LOG_LEVEL) \
		--cpu-prof-file=$(PROFILE_DIR)/precacher.cpu.pprof \
		--mem-prof-file=$(PROFILE_DIR)/precacher.mem.pprof \
		--trace-file=$(PROFILE_DIR)/precacher.trace \
		$(if $(filter y,$(ENABLE_CPU_PROFILE)),--enable-cpu-prof) \
		$(if $(filter y,$(ENABLE_MEM_PROFILE)),--enable-mem-prof) \
		$(if $(filter y,$(ENABLE_TRACE)),--enable-trace)  && \
	if [ -s "$(precache_downloaded_files)" ]; then \
		touch $@; \
	fi
