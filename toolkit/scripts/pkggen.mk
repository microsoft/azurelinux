# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Contains:
#	- Package dependency calculations
#	- Package builds

$(call create_folder,$(RPMS_DIR))
$(call create_folder,$(CACHED_RPMS_DIR))
$(call create_folder,$(PKGBUILD_DIR))
$(call create_folder,$(CHROOT_DIR))

######## PACKAGE DEPENDENCY CALCULATIONS ########

# Resources
pkggen_local_repo           = $(MANIFESTS_DIR)/package/local.repo
graphpkgfetcher_cloned_repo = $(MANIFESTS_DIR)/package/fetcher.repo

# SPECs and Built RPMs
build_specs     = $(shell find $(BUILD_SPECS_DIR)/ -type f -name '*.spec')
build_spec_dirs = $(foreach spec,$(build_specs),$(dir $(spec)))
pkggen_rpms     = $(shell find $(RPMS_DIR)/*  2>/dev/null )

# Pkggen workspace
cache_working_dir      = $(PKGBUILD_DIR)/tdnf_cache_worker
rpmbuilding_logs_dir   = $(LOGS_DIR)/pkggen/rpmbuilding
rpm_cache_files        = $(shell find $(CACHED_RPMS_DIR)/)
validate-pkggen-config = $(STATUS_FLAGS_DIR)/validate-image-config-pkggen.flag

# Outputs
specs_file        = $(PKGBUILD_DIR)/specs.json
graph_file        = $(PKGBUILD_DIR)/graph.dot
cached_file       = $(PKGBUILD_DIR)/cached_graph.dot
preprocessed_file = $(PKGBUILD_DIR)/preprocessed_graph.dot
built_file        = $(PKGBUILD_DIR)/built_graph.dot

logging_command = --log-file=$(LOGS_DIR)/pkggen/workplan/$(notdir $@).log --log-level=$(LOG_LEVEL)
$(call create_folder,$(LOGS_DIR)/pkggen/workplan)
$(call create_folder,$(rpmbuilding_logs_dir))

.PHONY: clean-workplan clean-cache graph-cache analyze-built-graph
graph-cache: $(cached_file)
clean: clean-workplan clean-cache
clean-workplan:
	rm -rf $(PKGBUILD_DIR)
	rm -rf $(LOGS_DIR)/pkggen/workplan
clean-cache:
	rm -rf $(CACHED_RPMS_DIR)
	rm -f $(validate-pkggen-config)
	@echo Verifying no mountpoints present in $(cache_working_dir)
	$(SCRIPTS_DIR)/safeunmount.sh "$(cache_working_dir)" && \
	rm -rf $(cache_working_dir)

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

# Parse all specs in $(BUILD_SPECS_DIR) and generate a specs.json file encoding all dependency information
$(specs_file): $(chroot_worker) $(BUILD_SPECS_DIR) $(build_specs) $(build_spec_dirs) $(go-specreader)
	$(go-specreader) \
		--dir $(BUILD_SPECS_DIR) \
		--build-dir $(BUILD_DIR)/spec_parsing \
		--srpm-dir $(BUILD_SRPMS_DIR) \
		--rpm-dir $(RPMS_DIR) \
		--dist-tag $(DIST_TAG) \
		--worker-tar $(chroot_worker) \
		$(if $(filter y,$(RUN_CHECK)),--run-check) \
		$(logging_command) \
		--output $@

# Convert the dependency information in the json file into a graph structure
$(graph_file): $(specs_file) $(go-grapher)
	$(go-grapher) \
		--input $(specs_file) \
		$(logging_command) \
		--output $@

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

ifeq ($(USE_PREVIEW_REPO),y)
graphpkgfetcher_extra_flags += --use-preview-repo
endif

ifeq ($(STOP_ON_FETCH_FAIL),y)
graphpkgfetcher_extra_flags += --stop-on-failure
endif

$(cached_file): $(graph_file) $(go-graphpkgfetcher) $(chroot_worker) $(pkggen_local_repo) $(depend_REPO_LIST) $(REPO_LIST) $(shell find $(CACHED_RPMS_DIR)/) $(pkggen_rpms)
	mkdir -p $(CACHED_RPMS_DIR)/cache && \
	$(go-graphpkgfetcher) \
		--input=$(graph_file) \
		--output-dir=$(CACHED_RPMS_DIR)/cache \
		--rpm-dir=$(RPMS_DIR) \
		--tmp-dir=$(cache_working_dir) \
		--tdnf-worker=$(chroot_worker) \
		--tls-cert=$(TLS_CERT) \
		--tls-key=$(TLS_KEY) \
		$(foreach repo, $(pkggen_local_repo) $(graphpkgfetcher_cloned_repo) $(REPO_LIST),--repo-file=$(repo) ) \
		$(graphpkgfetcher_extra_flags) \
		$(logging_command) \
		--input-summary-file=$(PACKAGE_CACHE_SUMMARY) \
		--output-summary-file=$(PKGBUILD_DIR)/graph_external_deps.json \
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

.PHONY: build-packages clean-build-packages hydrate-rpms compress-rpms clean-compress-rpms compress-srpms clean-compress-srpms

# Execute the package build scheduler.
build-packages: $(RPMS_DIR)

clean: clean-build-packages clean-compress-rpms clean-compress-srpms
clean-build-packages:
	rm -rf $(RPMS_DIR)
	rm -rf $(LOGS_DIR)/pkggen/failures.txt
	rm -rf $(rpmbuilding_logs_dir)
	rm -rf $(STATUS_FLAGS_DIR)/build-rpms.flag
	@echo Verifying no mountpoints present in $(CHROOT_DIR)
	$(SCRIPTS_DIR)/safeunmount.sh "$(CHROOT_DIR)" && \
	rm -rf $(CHROOT_DIR)
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

$(STATUS_FLAGS_DIR)/build-rpms.flag: $(preprocessed_file) $(chroot_worker) $(go-scheduler) $(go-pkgworker) $(depend_STOP_ON_PKG_FAIL) $(CONFIG_FILE) $(depend_CONFIG_FILE)
	$(go-scheduler) \
		--input="$(preprocessed_file)" \
		--output="$(built_file)" \
		--workers="$(CONCURRENT_PACKAGE_BUILDS)" \
		--work-dir="$(CHROOT_DIR)" \
		--worker-tar="$(chroot_worker)" \
		--repo-file="$(pkggen_local_repo)" \
		--rpm-dir="$(RPMS_DIR)" \
		--srpm-dir="$(SRPMS_DIR)" \
		--cache-dir="$(CACHED_RPMS_DIR)/cache" \
		--build-logs-dir="$(rpmbuilding_logs_dir)" \
		--dist-tag="$(DIST_TAG)" \
		--distro-release-version="$(RELEASE_VERSION)" \
		--distro-build-number="$(BUILD_NUMBER)" \
		--rpmmacros-file="$(TOOLCHAIN_MANIFESTS_DIR)/macros.override" \
		--build-attempts="$(PACKAGE_BUILD_RETRIES)" \
		--build-agent="chroot-agent" \
		--build-agent-program="$(go-pkgworker)" \
		--ignored-packages="$(PACKAGE_IGNORE_LIST)" \
		--packages="$(PACKAGE_BUILD_LIST)" \
		--rebuild-packages="$(PACKAGE_REBUILD_LIST)" \
		--image-config-file="$(CONFIG_FILE)" \
		--reserved-file-list-file="$(TOOLCHAIN_MANIFEST)" \
		$(if $(CONFIG_FILE),--base-dir="$(CONFIG_BASE_DIR)") \
		$(if $(filter y,$(RUN_CHECK)),--run-check) \
		$(if $(filter y,$(STOP_ON_PKG_FAIL)),--stop-on-failure) \
		$(if $(filter-out y,$(USE_PACKAGE_BUILD_CACHE)),--no-cache) \
		$(if $(filter-out y,$(CLEANUP_PACKAGE_BUILDS)),--no-cleanup) \
		$(logging_command) && \
	touch $@

# use temp tarball to avoid tar warning "file changed as we read it"
# that can sporadically occur when tarball is the dir that is compressed
compress-rpms:
	tar -I $(ARCHIVE_TOOL) -cvp -f $(BUILD_DIR)/temp_rpms_tarball.tar.gz -C $(RPMS_DIR)/.. $(notdir $(RPMS_DIR))
	mv $(BUILD_DIR)/temp_rpms_tarball.tar.gz $(pkggen_archive)

# use temp tarball to avoid tar warning "file changed as we read it"
# that can sporadically occur when tarball is the dir that is compressed
compress-srpms:
	tar -I $(ARCHIVE_TOOL) -cvp -f $(BUILD_DIR)/temp_srpms_tarball.tar.gz -C $(SRPMS_DIR)/.. $(notdir $(SRPMS_DIR))
	mv $(BUILD_DIR)/temp_srpms_tarball.tar.gz $(srpms_archive)

# Seed the RPMs folder with the any missing files from the archive.
hydrate-rpms:
	$(if $(PACKAGE_ARCHIVE),,$(error Must set PACKAGE_ARCHIVE=))
	@echo Updating missing RPMs from $(PACKAGE_ARCHIVE) into $(RPMS_DIR)
	tar -I $(ARCHIVE_TOOL) -xf $(PACKAGE_ARCHIVE) -C $(RPMS_DIR) --strip-components 1 --skip-old-files --touch --checkpoint=100000 --checkpoint-action=echo="%T"
