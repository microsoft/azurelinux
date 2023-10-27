# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Contains:
#	- Tools to fully hydrate the rpm cache from upstream repos with the any versions that match local .spec files

.PHONY: pre-cache clean-precache

precache_state_dir = $(CACHED_RPMS_DIR)/precache
precache_downloaded_files = $(precache_state_dir)/downloaded_files.txt
repo_urls_file = $(precache_state_dir)/repo_urls.txt
precache_chroot_dir = $(precache_state_dir)/chroot
precache_logs_path = $(LOGS_DIR)/precache/precache.log

$(call create_folder,$(precache_state_dir))
$(call create_folder,$(remote_rpms_cache_dir))

clean-cache: clean-precache
clean: clean-precache
clean-precache:
	@echo Verifying no mountpoints present in $(precache_chroot_dir)
	$(SCRIPTS_DIR)/safeunmount.sh "$(precache_chroot_dir)" && \
	rm -rf $(precache_state_dir)

# We always want to run the precache script, it will decide if it needs to download anything and update the flag file if
# it does, so add the phony target as a dependency to the flag file
.PHONY: precache_always_run_phony
pre-cache: $(STATUS_FLAGS_DIR)/precache.flag
$(STATUS_FLAGS_DIR)/precache.flag: $(go-precacher) $(chroot_worker) $(rpms_snapshot) precache_always_run_phony 
	@if [ "$(DISABLE_UPSTREAM_REPOS)" = "y" ]; then \
		echo "ERROR: Upstream repos are disabled (DISABLE_UPSTREAM_REPOS=y), cannot precache RPMs"; \
		exit 1; \
	fi
	$(go-precacher) \
		--snapshot "$(rpms_snapshot)" \
		--output-dir "$(remote_rpms_cache_dir)" \
		--output-summary-file "$(precache_downloaded_files)" \
		--repo-urls-file "$(repo_urls_file)" \
		$(foreach url,$(PACKAGE_URL_LIST), --repo-url "$(url)") \
		$(foreach repofile,$(REPO_LIST), --repo-file "$(repofile)") \
		--worker-tar $(chroot_worker) \
		--worker-dir $(precache_chroot_dir) \
		--log-file=$(precache_logs_path) \
		--log-level=$(LOG_LEVEL) \
		--cpu-prof-file=$(PROFILE_DIR)/precacher.cpu.pprof \
		--mem-prof-file=$(PROFILE_DIR)/precacher.mem.pprof \
		--trace-file=$(PROFILE_DIR)/precacher.trace \
		$(if $(filter y,$(ENABLE_CPU_PROFILE)),--enable-cpu-prof) \
		$(if $(filter y,$(ENABLE_MEM_PROFILE)),--enable-mem-prof) \
		$(if $(filter y,$(ENABLE_TRACE)),--enable-trace) \
		--timestamp-file=$(TIMESTAMP_DIR)/precacher.jsonl && \
	if [ ! -f $@ ] || [ -s "$(precache_downloaded_files)" ]; then \
		touch $@; \
	fi
