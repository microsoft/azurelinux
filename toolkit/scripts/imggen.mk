# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

$(call create_folder,$(IMAGEGEN_DIR))

# Resources
config_name              = $(notdir $(CONFIG_FILE:%.json=%))
config_other_files       = $(if $(CONFIG_FILE),$(shell find $(CONFIG_BASE_DIR)))
assets_dir               = $(RESOURCES_DIR)/assets/
assets_files             = $(shell find $(assets_dir))
imggen_local_repo        = $(MANIFESTS_DIR)/image/local.repo
imagefetcher_local_repo  = $(MANIFESTS_DIR)/package/local.repo
imagefetcher_cloned_repo = $(MANIFESTS_DIR)/package/fetcher.repo
ifeq ($(build_arch),aarch64)
initrd_config_json       = $(RESOURCES_DIR)/imageconfigs/iso_initrd_arm64.json
else
initrd_config_json       = $(RESOURCES_DIR)/imageconfigs/iso_initrd.json
endif
meta_user_data_files     = $(META_USER_DATA_DIR)/user-data $(META_USER_DATA_DIR)/meta-data
ova_ovfinfo              = $(assets_dir)/ova/ovfinfo.txt
ova_vmxtemplate          = $(assets_dir)/ova/vmx-template

# Built RPMs
imggen_rpms = $(shell find $(RPMS_DIR) -type f -name '*.rpm')

# Imagegen workspace and cache
imggen_config_dir                    = $(IMAGEGEN_DIR)/$(config_name)
workspace_dir                        = $(imggen_config_dir)/workspace
local_and_external_rpm_cache         = $(imggen_config_dir)/package_repo
external_rpm_cache                   = $(imggen_config_dir)/external_package_repo
image_fetcher_tmp_dir                = $(imggen_config_dir)/fetcher_tmp
image_roaster_tmp_dir                = $(imggen_config_dir)/roaster_tmp
validate-config                      = $(STATUS_FLAGS_DIR)/validate-image-config-$(config_name).flag
meta_user_data_tmp_dir               = $(IMAGEGEN_DIR)/meta-user-data_tmp
image_package_cache_summary          = $(imggen_config_dir)/image_deps.json
image_external_package_cache_summary = $(imggen_config_dir)/image_external_deps.json

# Outputs
artifact_dir             = $(IMAGES_DIR)/$(config_name)
imager_disk_output_dir   = $(imggen_config_dir)/imager_output
imager_disk_output_files = $(shell find $(imager_disk_output_dir) -not -name '*:*')
ifeq ($(build_arch),aarch64)
initrd_img               = $(IMAGES_DIR)/iso_initrd_arm64/iso-initrd.img
else
initrd_img               = $(IMAGES_DIR)/iso_initrd/iso-initrd.img
endif
meta_user_data_iso       = ${IMAGES_DIR)/meta-user-data.iso

$(call create_folder,$(workspace_dir))
$(call create_folder,$(imager_disk_output_dir))
$(call create_folder,$(artifact_dir))
$(call create_folder,$(meta_user_data_tmp_dir))

.PHONY: fetch-image-packages fetch-external-image-packages make-raw-image image iso initrd validate-image-config clean-imagegen

clean: clean-imagegen
clean-imagegen:
	rm -rf $(STATUS_FLAGS_DIR)/build_srpms.flag
	rm -rf $(STATUS_FLAGS_DIR)/imager_disk_output.flag
	rm -rf $(STATUS_FLAGS_DIR)/validate-image-config-*
	rm -rf $(artifact_dir)
	rm -rf $(IMAGES_DIR)
	@echo Verifying no mountpoints present in $(IMAGEGEN_DIR)
	$(SCRIPTS_DIR)/safeunmount.sh "$(IMAGEGEN_DIR)" && \
	rm -rf $(IMAGEGEN_DIR)

fetch-image-packages: $(image_package_cache_summary)
fetch-external-image-packages: $(image_external_package_cache_summary)

# Validate the selected config file if any changes occur in the image config base directory.
# Changes to files located outside the base directory will not be detected.
validate-image-config: $(validate-config)
$(STATUS_FLAGS_DIR)/validate-image-config%.flag: $(go-imageconfigvalidator) $(depend_CONFIG_FILE) $(CONFIG_FILE) $(config_other_files)
	$(go-imageconfigvalidator) \
		--input=$(CONFIG_FILE) \
		--dir=$(CONFIG_BASE_DIR) && \
	touch $@


imagepkgfetcher_extra_flags :=
ifeq ($(DISABLE_UPSTREAM_REPOS),y)
imagepkgfetcher_extra_flags += --disable-upstream-repos
endif

ifeq ($(USE_PREVIEW_REPO),y)
imagepkgfetcher_extra_flags += --use-preview-repo
endif

$(image_package_cache_summary): $(go-imagepkgfetcher) $(chroot_worker) $(imggen_local_repo) $(depend_REPO_LIST) $(REPO_LIST) $(depend_CONFIG_FILE) $(CONFIG_FILE) $(validate-config) $(packagelist_files) $(RPMS_DIR) $(imggen_rpms)
	$(if $(CONFIG_FILE),,$(error Must set CONFIG_FILE=))
	$(go-imagepkgfetcher) \
		--input=$(CONFIG_FILE) \
		--base-dir=$(CONFIG_BASE_DIR) \
		--log-level=$(LOG_LEVEL) \
		--log-file=$(LOGS_DIR)/imggen/imagepkgfetcher.log \
		--rpm-dir=$(RPMS_DIR) \
		--tmp-dir=$(image_fetcher_tmp_dir) \
		--tdnf-worker=$(chroot_worker) \
		--tls-cert=$(TLS_CERT) \
		--tls-key=$(TLS_KEY) \
		$(foreach repo, $(imagefetcher_local_repo) $(imagefetcher_cloned_repo) $(REPO_LIST),--repo-file="$(repo)" ) \
		$(imagepkgfetcher_extra_flags) \
		--input-summary-file=$(IMAGE_CACHE_SUMMARY) \
		--output-summary-file=$@ \
		--output-dir=$(local_and_external_rpm_cache)

make-raw-image: $(imager_disk_output_dir)
$(imager_disk_output_dir): $(STATUS_FLAGS_DIR)/imager_disk_output.flag
	@touch $@
	@echo Finished updating $@

$(STATUS_FLAGS_DIR)/imager_disk_output.flag: $(go-imager) $(image_package_cache_summary) $(imggen_local_repo) $(depend_CONFIG_FILE) $(CONFIG_FILE) $(validate-config) $(packagelist_files) $(assets_files) $(imggen_packagelist_files)
	$(if $(CONFIG_FILE),,$(error Must set CONFIG_FILE=))
	mkdir -p $(imager_disk_output_dir) && \
	rm -rf $(imager_disk_output_dir)/* && \
	$(go-imager) \
		--build-dir $(workspace_dir) \
		--input $(CONFIG_FILE) \
		--base-dir=$(CONFIG_BASE_DIR) \
		--log-level=$(LOG_LEVEL) \
		--log-file=$(LOGS_DIR)/imggen/imager.log \
		--local-repo $(local_and_external_rpm_cache) \
		--tdnf-worker $(BUILD_DIR)/worker/worker_chroot.tar.gz \
		--repo-file=$(imggen_local_repo) \
		--assets $(assets_dir) \
		--output-dir $(imager_disk_output_dir) && \
	touch $@

# Sometimes files will have been deleted, that is fine so long as we were able to detect the change
$(imager_disk_output_dir)/%: ;

image: $(imager_disk_output_dir) $(imager_disk_output_files) $(go-roast) $(depend_CONFIG_FILE) $(CONFIG_FILE) $(validate-config)
	$(if $(CONFIG_FILE),,$(error Must set CONFIG_FILE=))
	VMXTEMPLATE=$(ova_vmxtemplate) OVFINFO=$(ova_ovfinfo) \
	$(go-roast) \
		--dir=$(imager_disk_output_dir) \
		--config $(CONFIG_FILE) \
		--output-dir $(artifact_dir) \
		--tmp-dir $(image_roaster_tmp_dir) \
		--release-version $(RELEASE_VERSION) \
		--log-level=$(LOG_LEVEL) \
		--log-file=$(LOGS_DIR)/imggen/roast.log \
		--image-tag=$(IMAGE_TAG)

$(image_external_package_cache_summary): $(cached_file) $(go-imagepkgfetcher) $(depend_CONFIG_FILE) $(CONFIG_FILE) $(validate-config)
	$(if $(CONFIG_FILE),,$(error Must set CONFIG_FILE=))
	$(go-imagepkgfetcher) \
		--input=$(CONFIG_FILE) \
		--base-dir=$(CONFIG_BASE_DIR) \
		--log-level=$(LOG_LEVEL) \
		--log-file=$(LOGS_DIR)/imggen/externalimagepkgfetcher.log \
		--rpm-dir=$(RPMS_DIR) \
		--tmp-dir=$(image_fetcher_tmp_dir) \
		--tdnf-worker=$(chroot_worker) \
		--external-only \
		--package-graph=$(graph_file) \
		--tls-cert=$(TLS_CERT) \
		--tls-key=$(TLS_KEY) \
		$(foreach repo, $(imagefetcher_local_repo) $(imagefetcher_cloned_repo) $(REPO_LIST),--repo-file="$(repo)" ) \
		$(imagepkgfetcher_extra_flags) \
		--input-summary-file=$(IMAGE_CACHE_SUMMARY) \
		--output-summary-file=$@ \
		--output-dir=$(external_rpm_cache)

# Stand alone target to build just the initrd, should not be used in conjunction with other targets. Use the 'iso' target instead.
initrd: $(go-liveinstaller) $(go-imager)
	# Recursive make call to build the initrd image $(artifact_dir)/iso-initrd.img
	$(MAKE) image CONFIG_FILE=$(initrd_config_json) IMAGE_CACHE_SUMMARY=$(INITRD_CACHE_SUMMARY) IMAGE_TAG=

iso: $(go-isomaker) $(go-liveinstaller) $(go-imager) $(depend_CONFIG_FILE) $(CONFIG_FILE) $(initrd_config_json) $(validate-config) $(image_package_cache_summary)
	$(if $(CONFIG_FILE),,$(error Must set CONFIG_FILE=))
	# Recursive make call to build the initrd image iso_initrd/iso-initrd.img
	# Called here instead of as a traditional dependency to make sure package builds are done sequentially for each config.
	$(MAKE) image CONFIG_FILE=$(initrd_config_json) IMAGE_CACHE_SUMMARY=$(INITRD_CACHE_SUMMARY) IMAGE_TAG= && \
	$(go-isomaker) \
		--base-dir $(CONFIG_BASE_DIR) \
		--build-dir $(workspace_dir) \
		--initrd-path $(initrd_img) \
		--input $(CONFIG_FILE) \
		--release-version $(RELEASE_VERSION) \
		--resources $(RESOURCES_DIR) \
		--iso-repo $(local_and_external_rpm_cache) \
		--log-level=$(LOG_LEVEL) \
		--log-file=$(LOGS_DIR)/imggen/isomaker.log \
		$(if $(UNATTENDED_INSTALLER),--unattended-install) \
		--output-dir $(artifact_dir) \
		--image-tag=$(IMAGE_TAG)
meta-user-data: $(meta_user_data_files)
	cp -t $(meta_user_data_tmp_dir) $(meta_user_data_files)
	if [ -n "$(SSH_KEY_FILE)" ]; then \
		sed -i "s|ssh-rsa <YOUR SSH KEY HERE>|`cat $(SSH_KEY_FILE)`|" $(meta_user_data_tmp_dir)/user-data; \
	fi
	if [ -n "$(TLS_CERT)" ] && [ -n "$(TLS_KEY)" ] && [ -n "$(CA_CERT)" ]; then \
		$(SCRIPTS_DIR)/addcerts.sh $(meta_user_data_tmp_dir)/user-data $(TLS_CERT) $(TLS_KEY) $(CA_CERT); \
	fi
	genisoimage -output $(IMAGES_DIR)/meta-user-data.iso -volid cidata -joliet -rock $(meta_user_data_tmp_dir)/*
