# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Azure Linux Image Customizer version.
# This is using semantic versioning.
#
# IMAGE_CUSTOMIZER_VERSION should have the format:
#
#   <major>.<minor>.<patch>
#
# and should hold the value of the next (or current) official release, not the previous official
# release.
IMAGE_CUSTOMIZER_VERSION ?= 0.3.0
IMAGE_CUSTOMIZER_VERSION_PREVIEW ?= -dev.$(DATETIME_AS_VERSION)+$(GIT_COMMIT_ID)
IMAGE_CUSTOMIZER_FULL_VERSION := $(IMAGE_CUSTOMIZER_VERSION)$(IMAGE_CUSTOMIZER_VERSION_PREVIEW)
