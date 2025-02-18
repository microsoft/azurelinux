# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Contains:
#	- build optimization flag auto configuration

######## QUICK_REBUILD AUTO CONFIGURE ########

# The QUICK_REBUILD* flags are special flags that will try to build the toolchain and packages as quickly as possible. They will
# automatically set REBUILD_TOOLS, REBUILD_TOOLCHAIN, DELTA_BUILD, INCREMENTAL_TOOLCHAIN, and ALLOW_TOOLCHAIN_DOWNLOAD_FAIL to 'y'.
# It will also set CLEAN_TOOLCHAIN_CONTAINERS to 'n'
##help:var:QUICK_REBUILD:{y,n}=Optimize the build for speed by using existing published components and optimizing unimpactful package rebuilds (Implies QUICK_REBUILD_PACKAGES=y, QUICK_REBUILD_TOOLCHAIN=y).
QUICK_REBUILD           ?= n
##help:var:QUICK_REBUILD_TOOLCHAIN:{y,n}=Rebuild the toolchain, but attempt to download components where possible.
QUICK_REBUILD_TOOLCHAIN ?= n
##help:var:QUICK_REBUILD_PACKAGES:{y,n}=Use as many packages as possible from upstream repos, limit cascading rebuilds when a dependency is rebuilt.
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

# Don't care if REBUILD_TOOLS is set or not, doesn't matter to the quickbuild. Just turn it
# on to be friendly to the user unless they have explicitly set it to off.
REBUILD_TOOLS          ?= y
DELTA_FETCH            ?= y
PRECACHE               ?= y
# We also want to try and limit pointless rebuilds, so set EXTRA_BUILD_LAYERS to 1 if it's not already set.
MAX_CASCADING_REBUILDS ?= 1
endif

######## SET REMAINING FLAG DEFAULTS ########
ifeq ($(USE_NEW_TOOLCHAIN),y)
REBUILD_TOOLCHAIN               ?= auto
else
REBUILD_TOOLCHAIN               ?= n
endif
ALLOW_TOOLCHAIN_DOWNLOAD_FAIL   ?= n
##help:var:REBUILD_TOOLS:{y,n}=Build the go tools locally instead of taking them from the SDK.
REBUILD_TOOLS                   ?= n
DELTA_BUILD                     ?= n
CLEAN_TOOLCHAIN_CONTAINERS      ?= y
MAX_CPU                         ?=
PACKAGE_BUILD_TIMEOUT           ?= 8h
DELTA_FETCH                     ?= n
PRECACHE                        ?= n
MAX_CASCADING_REBUILDS          ?=

######## HANDLE INCREMENTAL_TOOLCHAIN DEPRECATION ########

# Generally, the DELTA_BUILD flag is used to determine whether to use the incremental toolchain, but to preserve
# backwards compatibility, use the INCREMENTAL_TOOLCHAIN flag if it's set.
ifneq ($(origin INCREMENTAL_TOOLCHAIN), undefined)
# Use \e[33m and \e[0m to generate yellow text. Need to execute inside $(shell...) to get the colors.
$(warning $(shell echo "\e[33mWARNING: INCREMENTAL_TOOLCHAIN is being deprecated, please use DELTA_BUILD=y instead. \e[0m" ))
endif
INCREMENTAL_TOOLCHAIN ?= $(DELTA_BUILD)
