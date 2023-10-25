# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Contains:
#	- Package dependency calculations
#	- Package builds

$(call create_folder,$(RPMS_DIR))
$(call create_folder,$(CACHED_RPMS_DIR))
$(call create_folder,$(PKGBUILD_DIR))
$(call create_folder,$(CHROOT_DIR))
$(call create_folder,$(CCACHE_DIR))

######## PACKAGE DEPENDENCY CALCULATIONS ########

# Resources
pkggen_local_repo           = $(MANIFESTS_DIR)/package/local.repo
graphpkgfetcher_cloned_repo = $(MANIFESTS_DIR)/package/fetcher.repo

# SPECs and Built RPMs
build_specs     = $(call shell_real_build_only, find $(SPECS_DIR)/ -type f -name '*.spec')
build_spec_dirs = $(foreach spec,$(build_specs),$(dir $(spec)))
pkggen_rpms     = $(call shell_real_build_only, find $(RPMS_DIR)/*  2>/dev/null )

# Pkggen workspace
cache_working_dir      = $(PKGBUILD_DIR)/tdnf_cache_worker
grapher_working_dir    = $(PKGBUILD_DIR)/grapher_cache_worker
parse_working_dir      = $(BUILD_DIR)/spec_parsing
rpmbuilding_logs_dir   = $(LOGS_DIR)/pkggen/rpmbuilding
remote_rpms_cache_dir  = $(CACHED_RPMS_DIR)/cache
cached_remote_rpms     = $(call shell_real_build_only, find $(remote_rpms_cache_dir))
validate-pkggen-config = $(STATUS_FLAGS_DIR)/validate-image-config-pkggen.flag

# Outputs
specs_file        = $(PKGBUILD_DIR)/specs.json
graph_file        = $(PKGBUILD_DIR)/graph.dot
cached_file       = $(PKGBUILD_DIR)/cached_graph.dot
preprocessed_file = $(PKGBUILD_DIR)/preprocessed_graph.dot
built_file        = $(PKGBUILD_DIR)/built_graph.dot
output_csv_file   = $(PKGBUILD_DIR)/build_state.csv

logging_command = --log-file=$(LOGS_DIR)/pkggen/workplan/$(notdir $@).log --log-level=$(LOG_LEVEL)
$(call create_folder,$(LOGS_DIR)/pkggen/workplan)
$(call create_folder,$(rpmbuilding_logs_dir))

.PHONY: clean-workplan clean-cache clean-cache-worker clean-grapher-cache-worker clean-spec-parse clean-ccache graph graph-cache graph-preprocessed analyze-built-graph workplan
##help:target:parsed-specs=Parse package specs and generate a specs.json file encoding all dependency information.
parse-specs: $(specs_file)
##help:target:graph-cache=Resolve package dependencies and cache the results.
graph-cache: $(cached_file)
##help:target:graph=Create the initial package build graph.
workplan graph: $(graph_file)
graph-preprocessed: $(preprocessed_file)

clean: clean-workplan clean-cache clean-spec-parse
clean-workplan: clean-cache clean-spec-parse clean-grapher-cache-worker
	rm -rf $(PKGBUILD_DIR)
	rm -rf $(LOGS_DIR)/pkggen/workplan
clean-grapher-cache-worker:
	$(SCRIPTS_DIR)/safeunmount.sh "$(grapher_working_dir)" && \
	rm -rf $(grapher_working_dir)
clean-cache-worker:
	$(SCRIPTS_DIR)/safeunmount.sh "$(cache_working_dir)" && \
	rm -rf $(cache_working_dir)
clean-cache: clean-cache-worker
	rm -rf $(CACHED_RPMS_DIR)
	rm -f $(validate-pkggen-config)
	@echo Verifying no mountpoints present in $(cache_working_dir)
clean-spec-parse:
	@echo Verifying no mountpoints present in $(parse_working_dir)
	$(SCRIPTS_DIR)/safeunmount.sh "$(parse_working_dir)" && \
	rm -rf $(parse_working_dir)
	rm -rf $(specs_file)
clean-ccache:
	rm -rf $(CCACHE_DIR)

# Optionally generate a summary of any blocked packages after a build.
analyze-built-graph: $(go-graphanalytics)
	if [ -f $(build_file) ]; then \
		$(go-graphanalytics) \
			--input=$(built_file) \
			--max-results=$(NUM_OF_ANALYTICS_RESULTS) \
			$(logging_command); \
	else \
		echo "No built graph to analyze"; \
		exit 1; \
	fi

# Parse specs in $(SPECS_DIR) and generate a specs.json file encoding all dependency information
# We look at the same pack list as the srpmpacker tool via the target $(srpm_pack_list_file), which
# is build from the contents of $(SRPM_PACK_LIST) if it is set. We only parse the spec files we will
# actually pack.
$(specs_file): $(chroot_worker) $(SPECS_DIR) $(build_specs) $(build_spec_dirs) $(go-specreader) $(depend_SPECS_DIR) $(srpm_pack_list_file) $(depend_RUN_CHECK)
	$(go-specreader) \
		--dir $(SPECS_DIR) \
		$(if $(SRPM_PACK_LIST),--spec-list=$(srpm_pack_list_file)) \
		--build-dir $(parse_working_dir) \
		--srpm-dir $(BUILD_SRPMS_DIR) \
		--rpm-dir $(RPMS_DIR) \
		--toolchain-manifest="$(TOOLCHAIN_MANIFEST)" \
		--toolchain-rpms-dir="$(TOOLCHAIN_RPMS_DIR)" \
		--dist-tag $(DIST_TAG) \
		--worker-tar $(chroot_worker) \
		$(if $(filter y,$(RUN_CHECK)),--run-check) \
		$(logging_command) \
		--cpu-prof-file=$(PROFILE_DIR)/specreader.cpu.pprof \
		--mem-prof-file=$(PROFILE_DIR)/specreader.mem.pprof \
		--trace-file=$(PROFILE_DIR)/specreader.trace \
		$(if $(filter y,$(ENABLE_CPU_PROFILE)),--enable-cpu-prof) \
		$(if $(filter y,$(ENABLE_MEM_PROFILE)),--enable-mem-prof) \
		$(if $(filter y,$(ENABLE_TRACE)),--enable-trace) \
		--timestamp-file=$(TIMESTAMP_DIR)/specreader.jsonl \
		$(if $(TARGET_ARCH),--target-arch="$(TARGET_ARCH)") \
		--output $@

ifeq ($(RESOLVE_CYCLES_FROM_UPSTREAM),y)
   ifeq ($(DISABLE_UPSTREAM_REPOS),y)
      $(error RESOLVE_CYCLES_FROM_UPSTREAM requires upstream repos to be enabled. Please set DISABLE_UPSTREAM_REPOS=n)
   endif
endif

# Convert the dependency information in the json file into a graph structure
# We require all the toolchain RPMs to be available here to help resolve unfixable cyclic dependencies
$(graph_file): $(specs_file) $(go-grapher) $(toolchain_rpms) $(TOOLCHAIN_MANIFEST) $(pkggen_local_repo) $(graphpkgfetcher_cloned_repo) $(chroot_worker) $(depend_REPO_LIST)
	$(go-grapher) \
		--input $(specs_file) \
		$(logging_command) \
		--cpu-prof-file=$(PROFILE_DIR)/grapher.cpu.pprof \
		--mem-prof-file=$(PROFILE_DIR)/grapher.mem.pprof \
		--trace-file=$(PROFILE_DIR)/grapher.trace \
		$(if $(filter y,$(ENABLE_CPU_PROFILE)),--enable-cpu-prof) \
		$(if $(filter y,$(ENABLE_MEM_PROFILE)),--enable-mem-prof) \
		$(if $(filter y,$(ENABLE_TRACE)),--enable-trace) \
		--timestamp-file=$(TIMESTAMP_DIR)/grapher.jsonl \
		--output $@ \
		$(if $(filter y,$(RESOLVE_CYCLES_FROM_UPSTREAM)), --resolve-cycles-from-upstream) \
		$(if $(filter y,$(USE_PREVIEW_REPO)), --use-preview-repo) \
		$(if $(filter y,$(DISABLE_DEFAULT_REPOS)), --disable-default-repos) \
		$(if $(filter y,$(IGNORE_VERSION_TO_RESOLVE_SELFDEP)), --ignore-version-to-resolve-selfdep) \
		--output-dir=$(CACHED_RPMS_DIR)/cache \
		--rpm-dir=$(RPMS_DIR) \
		--toolchain-rpms-dir=$(TOOLCHAIN_RPMS_DIR) \
		--tls-cert=$(TLS_CERT) \
		--tls-key=$(TLS_KEY) \
		--tmp-dir=$(grapher_working_dir) \
		--tdnf-worker=$(chroot_worker) \
		$(foreach repo, $(pkggen_local_repo) $(graphpkgfetcher_cloned_repo) $(REPO_LIST), --repo-file=$(repo))

# We want to detect changes in the RPM cache, but we are not responsible for directly rebuilding any missing files.
$(CACHED_RPMS_DIR)/%: ;

# Remove any packages which don't need to be built, and flag any for rebuild if
# their dependencies are updated.
ifneq ($(CONFIG_FILE),)
# If an optional config file is passed, validate it and any files it includes. The target should always depend
# on the value of $(CONFIG_FILE) however, so keep $(depend_CONFIG_FILE) always.
# Actual validation is handled in imggen.mk
$(cached_file): $(validate-pkggen-config)
endif

graphpkgfetcher_extra_flags :=

graphpkgfetcher_extra_flags :=
ifeq ($(DISABLE_UPSTREAM_REPOS),y)
graphpkgfetcher_extra_flags += --disable-upstream-repos
endif

ifeq ($(DISABLE_DEFAULT_REPOS),y)
graphpkgfetcher_extra_flags += --disable-default-repos
endif

ifeq ($(USE_PREVIEW_REPO),y)
graphpkgfetcher_extra_flags += --use-preview-repo
endif

ifeq ($(STOP_ON_FETCH_FAIL),y)
graphpkgfetcher_extra_flags += --stop-on-failure
endif

ifeq ($(DELTA_FETCH),y)
graphpkgfetcher_extra_flags += --ignored-packages="$(PACKAGE_IGNORE_LIST)"
graphpkgfetcher_extra_flags += --packages="$(PACKAGE_BUILD_LIST)"
graphpkgfetcher_extra_flags += --rebuild-packages="$(PACKAGE_REBUILD_LIST)"
graphpkgfetcher_extra_flags += --image-config-file="$(CONFIG_FILE)"
graphpkgfetcher_extra_flags += --ignored-tests="$(TEST_IGNORE_LIST)"
graphpkgfetcher_extra_flags += --tests="$(TEST_RUN_LIST)"
graphpkgfetcher_extra_flags += --rerun-tests="$(TEST_RERUN_LIST)"
graphpkgfetcher_extra_flags += $(if $(filter y,$(SKIP_MISSING_TESTS_IN_LISTS)),--skip-missing-requested-tests)
graphpkgfetcher_extra_flags += --try-download-delta-rpms
graphpkgfetcher_extra_flags += $(if $(CONFIG_FILE),--base-dir="$(CONFIG_BASE_DIR)")
$(cached_file): $(depend_CONFIG_FILE) $(depend_PACKAGE_BUILD_LIST) $(depend_PACKAGE_REBUILD_LIST) $(depend_PACKAGE_IGNORE_LIST) $(depend_TEST_RUN_LIST) $(depend_TEST_RERUN_LIST) $(depend_TEST_IGNORE_LIST)
endif

ifeq ($(PRECACHE),y)
# Use highly parallel downlader to fully hydrate the cache before trying to use the package manager to download packages
$(cached_file): $(STATUS_FLAGS_DIR)/precache.flag
endif

$(cached_file): $(graph_file) $(go-graphpkgfetcher) $(chroot_worker) $(pkggen_local_repo) $(depend_REPO_LIST) $(REPO_LIST) $(cached_remote_rpms) $(TOOLCHAIN_MANIFEST) $(toolchain_rpms)
	mkdir -p $(remote_rpms_cache_dir) && \
	$(go-graphpkgfetcher) \
		--input=$(graph_file) \
		--output-dir=$(remote_rpms_cache_dir) \
		--rpm-dir=$(RPMS_DIR) \
		--toolchain-rpms-dir="$(TOOLCHAIN_RPMS_DIR)" \
		--tmp-dir=$(cache_working_dir) \
		--tdnf-worker=$(chroot_worker) \
		--toolchain-manifest=$(TOOLCHAIN_MANIFEST) \
		--tls-cert=$(TLS_CERT) \
		--tls-key=$(TLS_KEY) \
		$(foreach repo, $(pkggen_local_repo) $(graphpkgfetcher_cloned_repo) $(REPO_LIST),--repo-file=$(repo) ) \
		$(graphpkgfetcher_extra_flags) \
		$(logging_command) \
		--input-summary-file=$(PACKAGE_CACHE_SUMMARY) \
		--output-summary-file=$(PKGBUILD_DIR)/graph_external_deps.json \
		--cpu-prof-file=$(PROFILE_DIR)/graphpkgfetcher.cpu.pprof \
		--mem-prof-file=$(PROFILE_DIR)/graphpkgfetcher.mem.pprof \
		--trace-file=$(PROFILE_DIR)/graphpkgfetcher.trace \
		$(if $(filter y,$(ENABLE_CPU_PROFILE)),--enable-cpu-prof) \
		$(if $(filter y,$(ENABLE_MEM_PROFILE)),--enable-mem-prof) \
		$(if $(filter y,$(ENABLE_TRACE)),--enable-trace) \
		--timestamp-file=$(TIMESTAMP_DIR)/graph_cache.jsonl \
		--output=$(cached_file) && \
	touch $@

$(preprocessed_file): $(cached_file) $(go-graphPreprocessor)
	$(go-graphPreprocessor) \
		--input=$(cached_file) \
		$(if $(filter y,$(HYDRATED_BUILD)),--hydrated-build) \
		$(logging_command) \
		--output=$@ && \
	touch $@

######## PACKAGE BUILD ########

pkggen_archive	= $(OUT_DIR)/rpms.tar.gz
srpms_archive  	= $(OUT_DIR)/srpms.tar.gz

.PHONY: build-packages clean-build-packages hydrate-rpms compress-rpms clean-compress-rpms compress-srpms clean-compress-srpms clean-build-packages-workers

##help:target:build-packages=Build .rpm packages selected by PACKAGE_(RE)BUILD_LIST= and IMAGE_CONFIG=.
# Execute the package build scheduler.
build-packages: $(RPMS_DIR)

clean: clean-build-packages clean-compress-rpms clean-compress-srpms
clean-build-packages-workers:
	@echo Verifying no mountpoints present in $(CHROOT_DIR)
	$(SCRIPTS_DIR)/safeunmount.sh "$(CHROOT_DIR)"/* && \
	rm -rf $(CHROOT_DIR)
clean-build-packages: clean-build-packages-workers
	rm -rf $(RPMS_DIR)
	rm -rf $(LOGS_DIR)/pkggen/failures.txt
	rm -rf $(rpmbuilding_logs_dir)
	rm -rf $(STATUS_FLAGS_DIR)/build-rpms.flag
clean-compress-rpms:
	rm -rf $(pkggen_archive)
clean-compress-srpms:
	rm -rf $(srpms_archive)

ifeq ($(REBUILD_PACKAGES),y)
$(RPMS_DIR): $(STATUS_FLAGS_DIR)/build-rpms.flag
	@touch $@
	@echo Finished updating $@
else
$(RPMS_DIR):
	@touch $@
endif

$(STATUS_FLAGS_DIR)/build-rpms.flag: $(no_repo_acl) $(preprocessed_file) $(chroot_worker) $(go-scheduler) $(go-pkgworker) $(depend_STOP_ON_PKG_FAIL) $(CONFIG_FILE) $(depend_CONFIG_FILE) $(depend_PACKAGE_BUILD_LIST) $(depend_PACKAGE_REBUILD_LIST) $(depend_PACKAGE_IGNORE_LIST) $(depend_MAX_CASCADING_REBUILDS) $(depend_TEST_RUN_LIST) $(depend_TEST_RERUN_LIST) $(depend_TEST_IGNORE_LIST) $(pkggen_rpms) $(srpms) $(BUILD_SRPMS_DIR)
	$(go-scheduler) \
		--input="$(preprocessed_file)" \
		--output="$(built_file)" \
		--output-build-state-csv-file="$(output_csv_file)" \
		--workers="$(CONCURRENT_PACKAGE_BUILDS)" \
		--work-dir="$(CHROOT_DIR)" \
		--worker-tar="$(chroot_worker)" \
		--repo-file="$(pkggen_local_repo)" \
		--rpm-dir="$(RPMS_DIR)" \
		--toolchain-rpms-dir="$(TOOLCHAIN_RPMS_DIR)" \
		--srpm-dir="$(SRPMS_DIR)" \
		--cache-dir="$(remote_rpms_cache_dir)" \
		--ccache-dir="$(CCACHE_DIR)" \
		--build-logs-dir="$(rpmbuilding_logs_dir)" \
		--dist-tag="$(DIST_TAG)" \
		--distro-release-version="$(RELEASE_VERSION)" \
		--distro-build-number="$(BUILD_NUMBER)" \
		--rpmmacros-file="$(TOOLCHAIN_MANIFESTS_DIR)/macros.override" \
		--build-attempts="$(PACKAGE_BUILD_RETRIES)" \
		--check-attempts="$(CHECK_BUILD_RETRIES)" \
		$(if $(MAX_CASCADING_REBUILDS),--max-cascading-rebuilds="$(MAX_CASCADING_REBUILDS)") \
		--build-agent="chroot-agent" \
		--build-agent-program="$(go-pkgworker)" \
		--ignored-packages="$(PACKAGE_IGNORE_LIST)" \
		--packages="$(PACKAGE_BUILD_LIST)" \
		--rebuild-packages="$(PACKAGE_REBUILD_LIST)" \
		--ignored-tests="$(TEST_IGNORE_LIST)" \
		--tests="$(TEST_RUN_LIST)" \
		--rerun-tests="$(TEST_RERUN_LIST)" \
		$(if $(filter y,$(SKIP_MISSING_TESTS_IN_LISTS)),--skip-missing-requested-tests) \
		--image-config-file="$(CONFIG_FILE)" \
		--cpu-prof-file=$(PROFILE_DIR)/scheduler.cpu.pprof \
		--mem-prof-file=$(PROFILE_DIR)/scheduler.mem.pprof \
		--trace-file=$(PROFILE_DIR)/scheduler.trace \
		$(if $(filter y,$(ENABLE_CPU_PROFILE)),--enable-cpu-prof) \
		$(if $(filter y,$(ENABLE_MEM_PROFILE)),--enable-mem-prof) \
		$(if $(filter y,$(ENABLE_TRACE)),--enable-trace) \
		--timestamp-file=$(TIMESTAMP_DIR)/scheduler.jsonl \
		--toolchain-manifest="$(TOOLCHAIN_MANIFEST)" \
		$(if $(CONFIG_FILE),--base-dir="$(CONFIG_BASE_DIR)") \
		$(if $(filter y,$(STOP_ON_PKG_FAIL)),--stop-on-failure) \
		$(if $(filter-out y,$(USE_PACKAGE_BUILD_CACHE)),--no-cache) \
		$(if $(filter-out y,$(CLEANUP_PACKAGE_BUILDS)),--no-cleanup) \
		$(if $(filter y,$(DELTA_BUILD)),--optimize-with-cached-implicit) \
		$(if $(filter y,$(USE_CCACHE)),--use-ccache) \
		$(if $(filter y,$(ALLOW_TOOLCHAIN_REBUILDS)),--allow-toolchain-rebuilds) \
		--max-cpu="$(MAX_CPU)" \
		$(logging_command) && \
	touch $@

##help:target:compress-rpms=Compresses all RPMs in `../out/RPMS` into `../out/rpms.tar.gz`. See `hydrate-rpms` target.
# use temp tarball to avoid tar warning "file changed as we read it"
# that can sporadically occur when tarball is the dir that is compressed
compress-rpms:
	tar -cvp -f $(BUILD_DIR)/temp_rpms_tarball.tar.gz -C $(RPMS_DIR)/.. $(notdir $(RPMS_DIR))
	mv $(BUILD_DIR)/temp_rpms_tarball.tar.gz $(pkggen_archive)

##help:target:compress-srpms=Compresses all SRPMs in `../out/SRPMS` into `../out/srpms.tar.gz`.
# use temp tarball to avoid tar warning "file changed as we read it"
# that can sporadically occur when tarball is the dir that is compressed
compress-srpms:
	tar -cvp -f $(BUILD_DIR)/temp_srpms_tarball.tar.gz -C $(SRPMS_DIR)/.. $(notdir $(SRPMS_DIR))
	mv $(BUILD_DIR)/temp_srpms_tarball.tar.gz $(srpms_archive)

# Seed the cached RPMs folder files from the archive.
hydrate-cached-rpms:
	$(if $(CACHED_PACKAGES_ARCHIVE),,$(error Must set CACHED_PACKAGES_ARCHIVE=<path>))
	@mkdir -p $(remote_rpms_cache_dir)
	@echo Unpacking cache RPMs from $(CACHED_PACKAGES_ARCHIVE) into $(remote_rpms_cache_dir)
	@tar -xf $(CACHED_PACKAGES_ARCHIVE) -C $(remote_rpms_cache_dir) --strip-components 1 --skip-old-files --touch --checkpoint=100000 --checkpoint-action=echo="%T"
# The cached RPMs directory has a flat structure, so we need to move the RPMs into the cache's root directory.
	@find $(remote_rpms_cache_dir) -mindepth 2 -name "*.rpm" -exec mv {} $(remote_rpms_cache_dir) \;
	@find $(remote_rpms_cache_dir) -mindepth 1 -type d -and ! -name repodata -exec rm -fr {} +

##help:target:hydrate-rpms=Hydrates the `../out/RPMS` directory from `rpms.tar.gz`. See `compress-rpms` target.
# Seed the RPMs folder with the any missing files from the archive.
hydrate-rpms:
	$(if $(PACKAGE_ARCHIVE),,$(error Must set PACKAGE_ARCHIVE=<path>))
	@echo Unpacking RPMs from $(PACKAGE_ARCHIVE) into $(RPMS_DIR)
	tar -xf $(PACKAGE_ARCHIVE) -C $(RPMS_DIR) --strip-components 1 --skip-old-files --touch --checkpoint=100000 --checkpoint-action=echo="%T"
