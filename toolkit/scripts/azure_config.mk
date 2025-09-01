# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# By default pass original user's Azure configuration if running as root.
# Running as root is required by how the toolkit operates while
# in most cases the user expects to still use their Azure configuration, thus the default.
ifneq ($(SUDO_USER),)
	export AZURE_CONFIG_DIR ?= $(shell sudo -u "$(SUDO_USER)" bash -c 'echo $${AZURE_CONFIG_DIR:-$${HOME}/.azure}')
endif
