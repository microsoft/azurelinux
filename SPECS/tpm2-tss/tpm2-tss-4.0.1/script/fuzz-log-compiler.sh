#!/usr/bin/env bash
# SPDX-License-Identifier: BSD-2-Clause
# Copyright (c) 2019, Intel Corporation
set -exu

# Check that the fuzz target does something by passing its own data as if it was
# random fuzz data
$1 $1
