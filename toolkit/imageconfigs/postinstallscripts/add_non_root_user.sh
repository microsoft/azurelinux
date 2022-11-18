#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Add nonroot user to the container image
USERNAME=nonroot
USER_UID=65532
USER_GID=$USER_UID

groupadd --gid $USER_GID $USERNAME
useradd --uid $USER_UID --gid $USER_GID -m $USERNAME
