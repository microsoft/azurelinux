# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import json
from enum import Enum
from pathlib import Path
from typing import List, Union

from pydantic import BaseModel, Field


class KernelConfigValue(str, Enum):
    """Enum for common kernel configuration values."""

    ENABLED = "y"
    DISABLED = "n"
    MODULE = "m"


class Architecture(str, Enum):
    """Enum for supported architectures."""

    ARM64 = "arm64"
    X86_64 = "x86_64"


class ArchConfigPair(BaseModel):
    """Schema for architecture and kernel config value pair."""

    model_config = {"extra": "forbid"}

    architecture: Architecture = Field(description="Target architecture")
    value: Union[KernelConfigValue, str] = Field(
        union_mode="left_to_right",
        description="Kernel configuration value for this architecture (y/n/m or custom)",
    )


class KernelConfig(BaseModel):
    """Schema for kernel configuration settings."""

    model_config = {"extra": "forbid"}

    name: str = Field(description="Name of the kernel configuration")
    values: List[ArchConfigPair] = Field(
        description="List of architecture-value pairs for this configuration"
    )
    justification: str = Field(
        description="Justification for this configuration setting"
    )


class KernelObject(BaseModel):
    """Schema for a kernel object containing configurations."""

    model_config = {"extra": "forbid"}

    name: str = Field(description="Name of the kernel")
    kernel_configs: List[KernelConfig] = Field(
        default_factory=list, description="List of kernel configuration settings"
    )


class IntentionalKernelConfigSchema(BaseModel):
    """Root schema for intentional kernel configuration settings."""

    model_config = {"extra": "forbid"}

    default: KernelObject = Field(description="Default kernel configuration object")
    overrides: List[KernelObject] = Field(
        default_factory=list,
        description="List of kernel override objects (kernel-1 to kernel-n)",
    )


def load_schema(filepath: Path) -> IntentionalKernelConfigSchema:
    """Load the schema from a JSON file."""
    with open(filepath, "r") as file:
        data = json.load(file)
    return IntentionalKernelConfigSchema.model_validate(data)


def save_schema(schema: IntentionalKernelConfigSchema, filepath: Path) -> None:
    """Save the schema to a JSON file."""
    with open(filepath, "w") as file:
        json.dump(schema.model_dump(mode="json"), file, indent=2)
