# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Contains:
#	- pprof & trace setup

# At the beginning of the build, create an empty directory at build/profile
$(call create_folder,$(PROFILE_DIR))
