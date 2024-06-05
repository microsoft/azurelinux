
#### VARIABLES
COAL_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
ROOT_DIR := $(realpath $(COAL_DIR)/..)

TOOLKIT_DIR := $(realpath $(ROOT_DIR)/toolkit)
AZURE_INIT_DIR := $(realpath $(ROOT_DIR)/SPECS/azure-init)

COAL_IMAGE_DIR := $(abspath $(COAL_DIR)/images)
COAL_RPMS_DIR := $(abspath $(COAL_DIR)/rpms)
OUT_DIR := $(abspath $(ROOT_DIR)/out)
TOOLKIT_TRIDENT_RPM_DIR := $(abspath $(OUT_DIR)/RPMS/trident)

MIC_BUILD_DIR := $(abspath $(COAL_DIR)/mic-build)

COAL_CONFIG_FILE := $(realpath $(TOOLKIT_DIR)/imageconfigs/coal-marketplace-gen2.json)
TOOLKIT_OUT_IMAGE_DIR := $(abspath $(OUT_DIR)/images/$(basename $(notdir $(COAL_CONFIG_FILE))))

# Toolkit Image Build Args
BASE_BUILD_ARGS += QUICK_REBUILD_PACKAGES="y"
BASE_BUILD_ARGS += SRPM_PACK_LIST="azure-init coal-trident-module"
BASE_BUILD_ARGS += CONFIG_FILE="$(COAL_CONFIG_FILE)"

ifneq ($(DAILY_BUILD_ID),)
$(warning Using Daily Build $(DAILY_BUILD_ID))
BASE_BUILD_ARGS += DAILY_BUILD_ID="$(DAILY_BUILD_ID)"
endif

#### VARIABLES - END

.PHONY: coal build-images imagecustomizer-bin clean clean-image-dir trident-rpm

coal: build-images

build-images: $(COAL_IMAGE_DIR)/base-image.vhdx $(COAL_IMAGE_DIR)/mic-image.vhdx $(COAL_RPMS_DIR)/trident.rpm

clean: clean-image-dir

clean-image-dir:
	rm -rf $(COAL_IMAGE_DIR)
	rm -rf $(COAL_RPMS_DIR)
	rm -rf $(MIC_BUILD_DIR)

$(COAL_IMAGE_DIR):
	mkdir -p $@

$(COAL_RPMS_DIR):
	mkdir -p $@

$(TOOLKIT_TRIDENT_RPM_DIR):
	mkdir -p $@

trident-rpm: | $(COAL_RPMS_DIR) $(TOOLKIT_TRIDENT_RPM_DIR)
	az artifacts universal download \
	--organization "https://dev.azure.com/mariner-org/" \
	--project "2311650c-e79e-4301-b4d2-96543fdd84ff" \
	--scope project \
	--feed "Trident" \
	--name "rpms-prerelease" \
	--version "0.1.2024052933-v90df99a" \
	--path $(COAL_RPMS_DIR)/
	cp $(COAL_RPMS_DIR)/* $(TOOLKIT_TRIDENT_RPM_DIR)

$(COAL_IMAGE_DIR)/base-image.vhdx: trident-rpm $(COAL_CONFIG_FILE) $(AZURE_INIT_DIR) | $(COAL_IMAGE_DIR)
	echo "Running Make target: $@"
	sudo $(MAKE) -C $(TOOLKIT_DIR) clean-imagegen
	sudo $(MAKE) -C $(TOOLKIT_DIR) -j100 image $(BASE_BUILD_ARGS)
	sudo cp $(TOOLKIT_OUT_IMAGE_DIR)/*.vhdx $@

$(COAL_IMAGE_DIR)/mic-image.vhdx: $(COAL_IMAGE_DIR)/base-image.vhdx $(COAL_DIR)/mic-coal-config.yaml | $(MIC_BUILD_DIR)
	echo "Running Make target: $@"
	sudo $(MAKE) -C $(TOOLKIT_DIR) go-tools
	cd $(TOOLKIT_DIR)/tools/imagecustomizer && \
	sudo ./imagecustomizer \
	--config-file="$(COAL_DIR)/mic-coal-config.yaml" \
	--image-file="$(COAL_IMAGE_DIR)/base-image.vhdx" \
	--build-dir="$(MIC_BUILD_DIR)" \
	--output-image-file="$@" \
	--output-image-format="vhdx" 

$(MIC_BUILD_DIR):
	mkdir $@

