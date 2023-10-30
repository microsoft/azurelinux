# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Contains:
#	- Toolchain Bootstrapping

######## TOOLCHAIN BOOTSTRAPPING ########

$(call create_folder,$(RPMS_DIR)/$(build_arch))
$(call create_folder,$(RPMS_DIR)/noarch)
$(call create_folder,$(SRPMS_DIR))
$(call create_folder,$(TOOLCHAIN_RPMS_DIR))

toolchain_build_dir = $(BUILD_DIR)/toolchain
toolchain_local_temp = $(toolchain_build_dir)/extract_dir
toolchain_from_repos = $(toolchain_build_dir)/repo_rpms
toolchain_logs_dir = $(LOGS_DIR)/toolchain
toolchain_downloads_logs_dir = $(toolchain_logs_dir)/downloads
toolchain_downloads_manifest = $(toolchain_downloads_logs_dir)/download_manifest.txt
toolchain_log_tail_length = 20
populated_toolchain_chroot = $(toolchain_build_dir)/populated_toolchain
toolchain_sources_dir = $(populated_toolchain_chroot)/usr/src/mariner/SOURCES
populated_toolchain_rpms = $(populated_toolchain_chroot)/usr/src/mariner/RPMS
toolchain_spec_list = $(toolchain_build_dir)/toolchain_specs.txt
toolchain_actual_contents = $(toolchain_build_dir)/actual_archive_contents.txt
toolchain_expected_contents = $(toolchain_build_dir)/expected_archive_contents.txt
raw_toolchain = $(toolchain_build_dir)/toolchain_from_container.tar.gz
final_toolchain = $(toolchain_build_dir)/toolchain_built_rpms_all.tar.gz
toolchain_files = \
	$(call shell_real_build_only, find $(SCRIPTS_DIR)/toolchain -name *.sh) \
	$(SCRIPTS_DIR)/toolchain/container/Dockerfile

TOOLCHAIN_MANIFEST ?= $(TOOLCHAIN_MANIFESTS_DIR)/toolchain_$(build_arch).txt
# Find the *.rpm corresponding to each of the entries in the manifest
# regex operation: (.*\.([^\.]+)\.rpm) extracts *.(<arch>).rpm" to determine
# the exact path of the required rpm
# Outputs: $(TOOLCHAIN_RPMS_DIR)/<arch>/<name>.<arch>.rpm
sed_regex_full_path = 's`(.*\.([^\.]+)\.rpm)`$(TOOLCHAIN_RPMS_DIR)/\2/\1`p'
sed_regex_full_path_rehydrated = 's`(.*\.([^\.]+)\.rpm)`$(toolchain_from_repos)/\1`p'
sed_regex_full_path_out_rpms = 's`(.*\.([^\.]+)\.rpm)`$(RPMS_DIR)/\2/\1`p'
toolchain_rpms := $(shell sed -nr $(sed_regex_full_path) < $(TOOLCHAIN_MANIFEST))
toolchain_rpms_buildarch := $(shell grep $(build_arch) $(TOOLCHAIN_MANIFEST))
toolchain_rpms_noarch := $(shell grep noarch $(TOOLCHAIN_MANIFEST))
toolchain_rpms_rehydrated := $(shell sed -nr $(sed_regex_full_path_rehydrated) < $(TOOLCHAIN_MANIFEST))
toolchain_out_rpms := $(shell sed -nr $(sed_regex_full_path_out_rpms) < $(TOOLCHAIN_MANIFEST))

$(call create_folder,$(toolchain_build_dir))
$(call create_folder,$(toolchain_downloads_logs_dir))
$(call create_folder,$(toolchain_from_repos))
$(call create_folder,$(populated_toolchain_chroot))

.PHONY: raw-toolchain toolchain clean-toolchain clean-toolchain-containers check-manifests check-aarch64-manifests check-x86_64-manifests
##help:target:raw-toolchain=Build the initial toolchain bootstrap stage.
raw-toolchain: $(raw_toolchain)
##help:target:toolchain=Ensure all toolchain RPMs are present.
toolchain: $(toolchain_rpms)
ifeq ($(REBUILD_TOOLCHAIN),y)
# If we are rebuilding the toolchain, we also expect the built RPMs to end up in out/RPMS
toolchain: $(toolchain_out_rpms)
endif

clean: clean-toolchain

clean-toolchain:
	$(SCRIPTS_DIR)/safeunmount.sh "$(toolchain_build_dir)"
	rm -rf $(toolchain_build_dir)
	rm -rf $(toolchain_local_temp)
	rm -rf $(toolchain_logs_dir)
	rm -rf $(toolchain_from_repos)
	rm -rf $(STATUS_FLAGS_DIR)/toolchain_local_temp.flag
	rm -f $(SCRIPTS_DIR)/toolchain/container/toolchain-local-wget-list
	rm -f $(SCRIPTS_DIR)/toolchain/container/texinfo-perl-fix.patch
	rm -f $(SCRIPTS_DIR)/toolchain/container/Awt_build_headless_only.patch
	rm -f $(SCRIPTS_DIR)/toolchain/container/check-system-ca-certs.patch
	rm -f $(SCRIPTS_DIR)/toolchain/container/rpm-define-RPM-LD-FLAGS.patch
	rm -f $(SCRIPTS_DIR)/toolchain/container/.bashrc

# Clean the containers we use during toolchain build
ifeq ($(CLEAN_TOOLCHAIN_CONTAINERS),y)
clean:  clean-toolchain-containers
endif

# Optionally remove all toolchain docker containers
clean-toolchain-containers:
	$(SCRIPTS_DIR)/toolchain/toolchain_clean.sh $(BUILD_DIR)

clean-toolchain-rpms:
	for f in $(toolchain_rpms_buildarch); do rm -vf $(RPMS_DIR)/$(build_arch)/$$f; done
	for f in $(toolchain_rpms_noarch); do rm -vf $(RPMS_DIR)/noarch/$$f; done

copy-toolchain-rpms:
	for f in $(toolchain_rpms_buildarch); do cp -vf $(TOOLCHAIN_RPMS_DIR)/$(build_arch)/$$f $(RPMS_DIR)/$(build_arch); done
	for f in $(toolchain_rpms_noarch); do cp -vf $(TOOLCHAIN_RPMS_DIR)/noarch/$$f $(RPMS_DIR)/noarch; done
	@#Print a red warning message so that it is more visible to the user
	@echo "\e[31m"
	@echo "WARNING: copy-toolchain-rpms should no longer be required for most use-cases. Please remove it from your build script unless you need to build older versions of the repo."
	@echo "\e[0m"

# check that the manifest files only contain RPMs that could have been generated from toolchain specs.
check-manifests: check-x86_64-manifests check-aarch64-manifests
check-aarch64-manifests: $(toolchain_spec_list)
	cd $(SCRIPTS_DIR)/toolchain && \
		./check_manifests.sh \
			$(toolchain_spec_list) \
			$(SPECS_DIR) \
			$(TOOLCHAIN_MANIFESTS_DIR) \
			$(DIST_TAG) \
			aarch64
check-x86_64-manifests: $(toolchain_spec_list)
	cd $(SCRIPTS_DIR)/toolchain && \
		./check_manifests.sh \
			$(toolchain_spec_list) \
			$(SPECS_DIR) \
			$(TOOLCHAIN_MANIFESTS_DIR) \
			$(DIST_TAG) \
			x86_64

# Generate a list of a specs built as part of the toolchain.
$(toolchain_spec_list): $(toolchain_files)
	cd $(SCRIPTS_DIR)/toolchain && \
		./list_toolchain_specs.sh \
			$(SCRIPTS_DIR)/toolchain/build_official_toolchain_rpms.sh \
			$(toolchain_spec_list)

# To save toolchain artifacts use compress-toolchain and cache the tarballs
# To restore toolchain artifacts use hydrate-toolchain and give the location of the tarballs on the command-line
# sudo make compress-toolchain TOOLCHAIN_SOURCE_ARCHIVE=~/cache/toolchain_sources.tar.gz CACHE_DIR=~/cache
# sudo make hydrate-toolchain TOOLCHAIN_CONTAINER_ARCHIVE=~/cache/toolchain_from_container.tar.gz TOOLCHAIN_ARCHIVE=~/cache/toolchain_built_rpms_all.tar.gz TOOLCHAIN_SOURCE_ARCHIVE=~/cache/toolchain_source.tar.gz
compress-toolchain:
	tar -I $(ARCHIVE_TOOL) -cvp --exclude='SOURCES' -f $(raw_toolchain) -C $(toolchain_build_dir) populated_toolchain
	tar -cvp -f $(final_toolchain) -C $(toolchain_build_dir) built_rpms_all
	$(if $(CACHE_DIR), cp $(raw_toolchain) $(final_toolchain) $(CACHE_DIR))

# After hydrating the toolchain run
# "sudo touch build/toolchain/toolchain_from_container.tar.gz" (should really check for existence of files in toolchain_*.txt)
# "sudo make toolchain REBUILD_TOOLCHAIN=y INCREMENTAL_TOOLCHAIN=y"
hydrate-toolchain:
	$(if $(TOOLCHAIN_CONTAINER_ARCHIVE),,$(error Must set TOOLCHAIN_CONTAINER_ARCHIVE=))
	$(if $(TOOLCHAIN_ARCHIVE),,$(error Must set TOOLCHAIN_ARCHIVE=))
	sudo mkdir -vp $(toolchain_build_dir)
	sudo cp $(TOOLCHAIN_CONTAINER_ARCHIVE) $(raw_toolchain)
	tar -I $(ARCHIVE_TOOL) -xf $(TOOLCHAIN_CONTAINER_ARCHIVE) -C $(toolchain_build_dir) --skip-old-files --touch --checkpoint=100000 --checkpoint-action=echo="%T"
	sudo cp $(TOOLCHAIN_ARCHIVE) $(final_toolchain)
	tar -xf $(TOOLCHAIN_ARCHIVE) -C $(toolchain_build_dir) --skip-old-files --touch --checkpoint=100000 --checkpoint-action=echo="%T"
	sudo touch $(final_toolchain)
	sudo mkdir -vp $(RPMS_DIR)/noarch
	sudo mkdir -vp $(RPMS_DIR)/$(build_arch)
	sudo cp $(toolchain_build_dir)/built_rpms_all/*.noarch.rpm $(RPMS_DIR)/noarch
	sudo cp $(toolchain_build_dir)/built_rpms_all/*.$(build_arch).rpm $(RPMS_DIR)/$(build_arch)
	sudo find $(RPMS_DIR) -name '*.rpm' -exec sudo touch {} ';'
	sudo mkdir -vp $(populated_toolchain_rpms)/noarch
	sudo mkdir -vp $(populated_toolchain_rpms)/$(build_arch)
	sudo cp $(toolchain_build_dir)/built_rpms_all/*.$(build_arch).rpm $(populated_toolchain_rpms)/$(build_arch)
	sudo cp  $(toolchain_build_dir)/built_rpms_all/*.noarch.rpm $(populated_toolchain_rpms)/noarch
	sudo find $(populated_toolchain_rpms) -name '*.rpm' -exec sudo touch {} ';'
	sudo rm $(final_toolchain)
	sudo touch $(raw_toolchain)

# Output:
# out/toolchain/toolchain_from_container.tar.gz
$(raw_toolchain): $(toolchain_files)
	@echo "Building raw toolchain"
	cd $(SCRIPTS_DIR)/toolchain && \
		./create_toolchain_in_container.sh \
			$(BUILD_DIR) \
			$(SPECS_DIR) \
			$(SOURCE_URL) \
			$(INCREMENTAL_TOOLCHAIN) \
			$(ARCHIVE_TOOL)

# This target establishes a cache of toolchain RPMs for partially rehydrating the toolchain from package repos.
# $(toolchain_from_repos) is a staging folder for these RPMs. We use the toolchain manifest to get a list of
# filenames for each possibly-rehydrated RPM. We attempt to download each RPM from $(PACKAGE_URL_LIST). In cases
# where an RPM is unavailable/download fails, we create an empty file. The build_official_toolchain_rpms.sh script
# knows the distinction between empty/non-empty files.
#
# The main usage scenario is avoiding full toolchain rebuilds after changing a toolchain package. The time needed to
# fully rebuild the final toolchain phase is vastly longer than the time needed to rehydrate most of the RPMs and
# build one or two changed SRPMs. Additionally, it allows us to build against the packages that are already published.
#
# When is it meaningful to attempt to partially rehydrate? It makes no sense to partially rehydrate if:
# - REBUILD_TOOLCHAIN = n: We aren't building the toolchain, so we defer to the full rehydration step
# - INCREMENTAL_TOOLCHAIN = n: We explicitly want to build a full toolchain
# - ALLOW_TOOLCHAIN_DOWNLOAD_FAIL = n: This flag explicitly disables partial toolchain rehydration from repos
# In these cases, we just create empty files for each possible rehydrated RPM.
ifeq ($(strip $(INCREMENTAL_TOOLCHAIN))$(strip $(REBUILD_TOOLCHAIN))$(strip $(ALLOW_TOOLCHAIN_DOWNLOAD_FAIL)),yyy)
$(toolchain_rpms_rehydrated): $(TOOLCHAIN_MANIFEST) $(go-downloader)
	@rpm_filename="$(notdir $@)" && \
	rpm_dir="$(dir $@)" && \
	log_file="$(toolchain_downloads_logs_dir)/$$rpm_filename.log" && \
	echo "Attempting to download toolchain RPM: $$rpm_filename" | tee -a "$$log_file" && \
	mkdir -p $$rpm_dir && \
	cd $$rpm_dir && \
	for url in $(PACKAGE_URL_LIST); do \
		$(go-downloader) --no-verbose --no-clobber $$url/$$rpm_filename \
			$(if $(TLS_CERT),--certificate=$(TLS_CERT)) \
			$(if $(TLS_KEY),--private-key=$(TLS_KEY)) \
			--log-file $$log_file && \
		echo "Downloaded toolchain RPM: $$rpm_filename" >> $$log_file && \
		echo "$$rpm_filename" >> $(toolchain_downloads_manifest) | tee -a "$$log_file" && \
		touch $@ && \
		break; \
	done || { \
		echo "Could not find toolchain package in package repo: $$rpm_filename." | tee -a "$$log_file" && \
		touch $@; \
	}
else
$(toolchain_rpms_rehydrated): $(TOOLCHAIN_MANIFEST)
	@touch $@
endif

# Output:
# out/toolchain/built_rpms
# out/toolchain/toolchain_built_rpms.tar.gz
$(final_toolchain): $(no_repo_acl) $(raw_toolchain) $(toolchain_rpms_rehydrated) $(STATUS_FLAGS_DIR)/build_toolchain_srpms.flag | $(go-bldtracker)
	@echo "Building base packages"
	# Clean the existing chroot if not doing an incremental build
	$(if $(filter y,$(INCREMENTAL_TOOLCHAIN)),,$(SCRIPTS_DIR)/safeunmount.sh "$(populated_toolchain_chroot)" || $(call print_error,failed to clean mounts for toolchain build))
	$(if $(filter y,$(INCREMENTAL_TOOLCHAIN)),,rm -rf $(populated_toolchain_chroot))
	cd $(SCRIPTS_DIR)/toolchain && \
		./build_mariner_toolchain.sh \
			$(DIST_TAG) \
			$(BUILD_NUMBER) \
			$(RELEASE_VERSION) \
			$(BUILD_DIR) \
			$(RPMS_DIR) \
			$(SPECS_DIR) \
			$(RUN_CHECK) \
			$(TOOLCHAIN_MANIFESTS_DIR) \
			$(INCREMENTAL_TOOLCHAIN) \
			$(BUILD_SRPMS_DIR) \
			$(SRPMS_DIR) \
			$(toolchain_from_repos) \
			$(TOOLCHAIN_MANIFEST) \
			$(go-bldtracker) \
			$(TIMESTAMP_DIR)/build_mariner_toolchain.jsonl && \
	$(if $(filter y,$(UPDATE_TOOLCHAIN_LIST)), ls -1 $(toolchain_build_dir)/built_rpms_all > $(MANIFESTS_DIR)/package/toolchain_$(build_arch).txt && ) \
	touch $@

.SILENT: $(toolchain_rpms)

ifeq ($(REBUILD_TOOLCHAIN),y)
# We know how to build this archive from scratch (possibly with some rehydrated RPMs from the package repo)
selected_toolchain_archive = $(final_toolchain)
else
# This may be an empty string, that is fine. If it's empty we will try to fully rehydrate using online packages
selected_toolchain_archive = $(TOOLCHAIN_ARCHIVE)
endif

# We will have three options at this point:
# 1) REBUILD_TOOLCHAIN: yes                                     -> Rebuild a toolchain from scratch and place it into $(final_toolchain)
# 2) REBUILD_TOOLCHAIN: no && TOOLCHAIN_ARCHIVE: 'foo.tar.gz'   -> Extract the RPMs from foo.tar.gz
# 3) REBUILD_TOOLCHAIN: no && TOOLCHAIN_ARCHIVE: ''             -> Download required RPMs using wget

# If there is an archive selected (build from scratch or provided via TOOLCHAIN_ARCHIVE), extract the RPMs from it.
ifneq (,$(selected_toolchain_archive))
# Our manifest files should always track the contents of the freshly built archives exactly
$(STATUS_FLAGS_DIR)/toolchain_verify.flag: $(TOOLCHAIN_MANIFEST) $(selected_toolchain_archive)
	@echo Validating contents of toolchain against manifest...
	tar -tf $(selected_toolchain_archive) | grep -oP "[^/]+rpm$$" | sort > $(toolchain_actual_contents) && \
	sort $(TOOLCHAIN_MANIFEST) > $(toolchain_expected_contents) && \
	diff="$$( comm -3 $(toolchain_actual_contents) $(toolchain_expected_contents) --check-order )" && \
	if [ -n "$${diff}" ]; then \
		printf "ERROR: Mismatched packages between:\n\n'%s'\n\t'%s'\n\n" '$(selected_toolchain_archive)' '$(TOOLCHAIN_MANIFEST)' && \
		echo "$${diff}"; \
		$(call print_error, $@ failed) ; \
	fi && \
	touch $@
	@echo Done validating toolchain

# Targets tracking toolchain staging area for bulk extraction of RPMs from toolchain package tarball
# The files are generated by $(STATUS_FLAGS_DIR)/toolchain_local_temp.flag
$(toolchain_local_temp): ;
$(toolchain_local_temp)%: ;

# If $(depend_TOOLCHAIN_ARCHIVE) and $(depend_REBUILD_TOOLCHAIN) argument trackers change it is important to check
#	that all of the toolchain .rpms are correct. The different toolchain sources may have identical files but with
#	different contents, so always redo the bulk rpm extraction. The $(toolchain_rpms): target will take
#	responsibility for updating the .rpms in the final destination if needed.
$(STATUS_FLAGS_DIR)/toolchain_local_temp.flag: $(selected_toolchain_archive) $(toolchain_local_temp) $(call shell_real_build_only, find $(toolchain_local_temp)/* 2>/dev/null) $(STATUS_FLAGS_DIR)/toolchain_verify.flag  $(depend_TOOLCHAIN_ARCHIVE) $(depend_REBUILD_TOOLCHAIN)
	mkdir -p $(toolchain_local_temp) && \
	rm -f $(toolchain_local_temp)/* && \
	tar -xf $(selected_toolchain_archive) -C $(toolchain_local_temp) --strip-components 1 && \
	touch $(toolchain_local_temp)/* && \
	touch $@

# Replace the toolchain RPM if one of the following is true:
#	The .rpm doesn't exist
#	The .rpm is older than the archive we are extracting it from
#	The toolchain configuration has been changed (depend_TOOLCHAIN_ARCHIVE and depend_REBUILD_TOOLCHAIN)
$(toolchain_rpms): $(TOOLCHAIN_MANIFEST) $(STATUS_FLAGS_DIR)/toolchain_local_temp.flag $(depend_TOOLCHAIN_ARCHIVE) $(depend_REBUILD_TOOLCHAIN)
	tempFile=$(toolchain_local_temp)/$(notdir $@) && \
	if [ ! -f $@ \
			-o $(selected_toolchain_archive) -nt $@ \
			-o $(depend_TOOLCHAIN_ARCHIVE) -nt $@ \
			-o $(depend_REBUILD_TOOLCHAIN) -nt $@ ]; then \
		echo Extracting RPM $@ from toolchain && \
		mkdir -p $(dir $@) && \
		cp $$tempFile $(dir $@) && \
		touch $@ ; \
	fi || $(call print_error, $@ failed) ; \
	touch $@

# No archive was selected, so download from online package server instead. All packages must be available for this step to succeed.
else
$(toolchain_rpms): $(TOOLCHAIN_MANIFEST) $(depend_REBUILD_TOOLCHAIN) $(go-downloader)
	@rpm_filename="$(notdir $@)" && \
	rpm_dir="$(dir $@)" && \
	log_file="$(toolchain_downloads_logs_dir)/$$rpm_filename.log" && \
	echo "Downloading toolchain RPM: $$rpm_filename" | tee -a "$$log_file" && \
	mkdir -p $$rpm_dir && \
	cd $$rpm_dir && \
	for url in $(PACKAGE_URL_LIST); do \
		$(go-downloader) --no-verbose --no-clobber $$url/$$rpm_filename \
			$(if $(TLS_CERT),--certificate=$(TLS_CERT)) \
			$(if $(TLS_KEY),--private-key=$(TLS_KEY)) \
			--log-file $$log_file && \
		echo "Downloaded toolchain RPM: $$rpm_filename" >> $$log_file && \
		touch $@ && \
		break; \
	done || { \
		echo "\nERROR: Failed to download toolchain package: $$rpm_filename." && \
		echo "ERROR: Last $(toolchain_log_tail_length) lines from log '$$log_file':\n" && \
		tail -n$(toolchain_log_tail_length) $$log_file | sed 's/^/\t/' && \
		$(call print_error,\nToolchain download failed. See above errors for more details.) \
	}
endif

# ./out/RPMS is reserved for RPMs generated by the tooling, all other RPMs are cached in the ./build folder. If REBUILD_TOOLCHAIN=y is set
# the toolchain RPMs should also be placed into out/RPMs.
# ./out/SRPMS are still handled by build_official_toolchain_rpms.sh as a side effect of building the toolchain tar.gz.
ifeq ($(REBUILD_TOOLCHAIN),y)
$(RPMS_DIR): $(toolchain_out_rpms)

# For each toolchain RPM in ./out/RPMS, add a dependency on the counterparts in the normal toolchain directory:
# Each path in $(toolchain_out_rpms) corresponds to a .rpm file we expect to have been built by the toolchain target and made available in ./out/RPMS.
# Those RPMs however are placed by default in ./build/toolchain/* (listed in $(toolchain_rpms)). So if we want a copy placed in ./out/RPMS
# we will need to copy it over. We can filter the list of toolchain rpms $(toolchain_rpms) to find the source that matches the target ($@),
# then copy it over.
$(toolchain_out_rpms): $(toolchain_rpms)
	@src_rpm='$(filter %/$(notdir $@),$(toolchain_rpms))'  && \
	if [ ! -f "$@" \
			-o "$$src_rpm" -nt "$@" ] ; then \
		echo "Placing built toolchain RPM $(notdir $@) into $(RPMS_DIR)" && \
		cp $$src_rpm $@; \
	fi || $(call print_error, Failed to duplicate '$$src_rpm' to '$@' )
endif
