# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Contains:
#	- build optimization flag auto configuration

######## QUICKREBUILD AUTO CONFIGURE ########

# The QUICKREBUILD* flags are special flags that will try to build the toolchain and packages as quickly as possible. They will
# automatically set REBUILD_TOOLS, USE_CCACHE, REBUILD_TOOLCHAIN, DELTA_BUILD, INCREMENTAL_TOOLCHAIN, and ALLOW_TOOLCHAIN_DOWNLOAD_FAIL to 'y'.
QUICKREBUILD           ?= n
QUICKREBUILD_TOOLCHAIN ?= n
QUICKREBUILD_PACKAGES  ?= n

ifeq ($(QUICKREBUILD),y)
QUICKREBUILD_TOOLCHAIN = y
QUICKREBUILD_PACKAGES  = y
endif

######## QUICKREBUILD TOOLCHAIN ########

ifeq ($(QUICKREBUILD_TOOLCHAIN),y)
# If any of these are already set to 'n', report an error
ifneq ($(filter n,$(REBUILD_TOOLCHAIN)),)
$(error QUICKREBUILD cannot be used with REBUILD_TOOLCHAIN explicitly set to 'n')
endif
ifneq ($(filter n,$(INCREMENTAL_TOOLCHAIN)),)
$(error QUICKREBUILD cannot be used with INCREMENTAL_TOOLCHAIN explicitly set to 'n')
endif
ifneq ($(filter n,$(ALLOW_TOOLCHAIN_DOWNLOAD_FAIL)),)
$(error QUICKREBUILD cannot be used with ALLOW_TOOLCHAIN_DOWNLOAD_FAIL explicitly set to 'n')
endif

# Don't care if REBUILD_TOOLS is set or not, doesn't matter to the quickbuild.

REBUILD_TOOLCHAIN             = y
INCREMENTAL_TOOLCHAIN         = y
ALLOW_TOOLCHAIN_DOWNLOAD_FAIL = y
REBUILD_TOOLS                 ?= y
endif

######## QUICKREBUILD PACKAGES ########

ifeq ($(QUICKREBUILD_PACKAGES),y)
# If any of these are already set to 'n', report an error
ifneq ($(filter n,$(DELTA_BUILD)),)
$(error DELTA_BUILD cannot be used with REBUILD_TOOLCHAIN explicitly  set to 'n')
endif

# Don't care if USE_CCACHE, or REBUILD_TOOLS are set or not, doesn't matter to the quickbuild.

DELTA_BUILD    = y
USE_CCACHE    ?= y
REBUILD_TOOLS ?= y
endif