# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Contains:
#	- build optimization flag auto configuration

######## QUICKBUILD AUTO CONFIGURE ########

# The QUICKBUILD* flags are special flags that will try to build the toolchain and packages as quickly as possible. They will
# automatically set REBUILD_TOOLS, USE_CCACHE, REBUILD_TOOLCHAIN, DELTA_BUILD, INCREMENTAL_TOOLCHAIN, and ALLOW_TOOLCHAIN_DOWNLOAD_FAIL to 'y'.
QUICKBUILD           ?= n
QUICKBUILD_TOOLCHAIN ?= n
QUICKBUILD_PACKAGES  ?= n

ifeq ($(QUICKBUILD),y)
QUICKBUILD_TOOLCHAIN = y
QUICKBUILD_PACKAGES  = y
REBUILD_TOOLS=y
endif

######## QUICKBUILD TOOLCHAIN ########

ifeq ($(QUICKBUILD_TOOLCHAIN),y)
# If any of these are already set to 'n', report an error
ifneq ($(filter n,$(REBUILD_TOOLCHAIN)),)
$(error QUICKBUILD cannot be used with REBUILD_TOOLCHAIN explicitly set to 'n')
endif
ifneq ($(filter n,$(INCREMENTAL_TOOLCHAIN)),)
$(error QUICKBUILD cannot be used with INCREMENTAL_TOOLCHAIN explicitly set to 'n')
endif
ifneq ($(filter n,$(ALLOW_TOOLCHAIN_DOWNLOAD_FAIL)),)
$(error QUICKBUILD cannot be used with ALLOW_TOOLCHAIN_DOWNLOAD_FAIL explicitly set to 'n')
endif
REBUILD_TOOLCHAIN             = y
INCREMENTAL_TOOLCHAIN         = y
ALLOW_TOOLCHAIN_DOWNLOAD_FAIL = y
endif

######## QUICKBUILD PACKAGES ########

ifeq ($(QUICKBUILD_PACKAGES),y)
# If any of these are already set to 'n', report an error
ifneq ($(filter n,$(DELTA_BUILD)),)
$(error DELTA_BUILD cannot be used with REBUILD_TOOLCHAIN explicitly  set to 'n')
endif
DELTA_BUILD = y
USE_CCACHE ?= y
endif