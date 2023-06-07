# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Contains:
#	- build optimization flag auto configuration

######## QUICK_REBUILD AUTO CONFIGURE ########

# The QUICK_REBUILD* flags are special flags that will try to build the toolchain and packages as quickly as possible. They will
# automatically set REBUILD_TOOLS, USE_CCACHE, REBUILD_TOOLCHAIN, DELTA_BUILD, INCREMENTAL_TOOLCHAIN, and ALLOW_TOOLCHAIN_DOWNLOAD_FAIL to 'y'.
# It will also set CLEAN_TOOLCHAIN_CONTAINERS to 'n'
QUICK_REBUILD           ?= n
QUICK_REBUILD_TOOLCHAIN ?= n
QUICK_REBUILD_PACKAGES  ?= n

ifeq ($(QUICK_REBUILD),y)
QUICK_REBUILD_TOOLCHAIN = y
QUICK_REBUILD_PACKAGES  = y
endif

######## QUICK_REBUILD TOOLCHAIN ########

ifeq ($(QUICK_REBUILD_TOOLCHAIN),y)
# If any of these are already set to 'n', report an error. The whole point of using QUICK_REBUILD is
# to enable these. Both INCREMENTAL_TOOLCHAIN and DELTA_BUILD are checked because DELTA_BUILD implies
# the depcrecated INCREMENTAL_TOOLCHAIN.
ifneq ($(filter n,$(REBUILD_TOOLCHAIN)),)
$(error QUICK_REBUILD_TOOLCHAIN cannot be used with REBUILD_TOOLCHAIN explicitly set to 'n')
endif
ifneq ($(filter n,$(INCREMENTAL_TOOLCHAIN)),)
$(error QUICK_REBUILD_TOOLCHAIN cannot be used with INCREMENTAL_TOOLCHAIN explicitly set to 'n')
endif
ifneq ($(filter n,$(DELTA_BUILD)),)
$(error QUICK_REBUILD_TOOLCHAIN cannot be used with DELTA_BUILD explicitly  set to 'n')
endif
ifneq ($(filter n,$(ALLOW_TOOLCHAIN_DOWNLOAD_FAIL)),)
$(error QUICK_REBUILD_TOOLCHAIN cannot be used with ALLOW_TOOLCHAIN_DOWNLOAD_FAIL explicitly set to 'n')
endif

DELTA_BUILD                   = y
REBUILD_TOOLCHAIN             = y
ALLOW_TOOLCHAIN_DOWNLOAD_FAIL = y

# Don't care if REBUILD_TOOLS or CLEAN_TOOLCHAIN_CONTAINERS is set or not, doesn't matter to the quickbuild. Just turn this
# on to be friendly to the user unless they  have explicitly set it to off.
REBUILD_TOOLS                ?= y
CLEAN_TOOLCHAIN_CONTAINERS   ?= n
endif

######## QUICK_REBUILD PACKAGES ########

ifeq ($(QUICK_REBUILD_PACKAGES),y)
# If any of these are already set to 'n', report an error
ifneq ($(filter n,$(DELTA_BUILD)),)
$(error QUICK_REBUILD_PACKAGES cannot be used with DELTA_BUILD explicitly  set to 'n')
endif

DELTA_BUILD    = y

# Don't care if USE_CCACHE or REBUILD_TOOLS are set or not, doesn't matter to the quickbuild. Just turn them
# on to be friendly to the user unless they have explicitly set it to off.
USE_CCACHE    ?= y
REBUILD_TOOLS ?= y
endif

######## SET REMAINING FLAG DEFAULTS ########

REBUILD_TOOLCHAIN               ?= n
ALLOW_TOOLCHAIN_DOWNLOAD_FAIL   ?= n
REBUILD_TOOLS                   ?= n
USE_CCACHE                      ?= n
DELTA_BUILD                     ?= n
CLEAN_TOOLCHAIN_CONTAINERS      ?= y

######## HANDLE INCREMENTAL_TOOLCHAIN DEPRECATION ########

# Generally, the DELTA_BUILD flag is used to determine whether to use the incremental toolchain, but to preserve
# backwards compatibility, use the INCREMENTAL_TOOLCHAIN flag if it's set.
ifneq ($(origin INCREMENTAL_TOOLCHAIN), undefined)
# Use \e[33m and \e[0m to generate yellow text. Need to execute inside $(shell...) to get the colors.
$(warning $(shell echo "\e[33mWARNING: INCREMENTAL_TOOLCHAIN is being deprecated, please use DELTA_BUILD=y instead. \e[0m" ))
endif
INCREMENTAL_TOOLCHAIN ?= $(DELTA_BUILD)
