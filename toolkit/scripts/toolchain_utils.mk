# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Contains:
#	- Toolchain Bootstrapping

######## COMMON TOOLCHAIN UTILITIES ########

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
$(toolchain_spec_list): $(toolchain_files) $(SCRIPTS_DIR)/toolchain/list_toolchain_specs.sh
	cd $(SCRIPTS_DIR)/toolchain && \
		./list_toolchain_specs.sh \
			$(SCRIPTS_DIR)/toolchain/build_official_toolchain_rpms.sh \
			$(SPECS_DIR) \
			$(toolchain_spec_list)

$(toolchain_spec_buildable_list): $(toolchain_files) $(SCRIPTS_DIR)/toolchain/list_toolchain_specs.sh
	cd $(SCRIPTS_DIR)/toolchain && \
		./list_toolchain_specs.sh \
			$(SCRIPTS_DIR)/toolchain/build_official_toolchain_rpms.sh \
			$(SPECS_DIR) \
			$(toolchain_spec_buildable_list) \
			--filter-buildable

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
