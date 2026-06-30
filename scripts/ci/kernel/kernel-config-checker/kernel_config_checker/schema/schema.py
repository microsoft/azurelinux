# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""Schema definitions for kernel configuration validation."""

from __future__ import annotations

import json
from enum import StrEnum
from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from pathlib import Path


class KernelConfigValue(StrEnum):
    """Enum for common kernel configuration values."""

    ENABLED = "y"
    DISABLED = "n"
    MODULE = "m"


class Architecture(StrEnum):
    """Enum for supported architectures."""

    ARM64 = "arm64"
    X86_64 = "x86_64"


class ArchConfigPair(BaseModel):
    """Schema for architecture and kernel config value pair."""

    model_config = {"extra": "forbid"}

    architecture: Architecture = Field(description="Target architecture")
    value: KernelConfigValue | str = Field(
        union_mode="left_to_right",
        description="Kernel configuration value for this architecture (y/n/m or custom)",
    )


class KernelConfig(BaseModel):
    """Schema for kernel configuration settings."""

    model_config = {"extra": "forbid"}

    name: str = Field(description="Name of the kernel configuration")
    values: list[ArchConfigPair] = Field(description="List of architecture-value pairs for this configuration")
    justification: str = Field(description="Justification for this configuration setting")


class KernelObject(BaseModel):
    """Schema for a kernel object containing configurations."""

    model_config = {"extra": "forbid"}

    name: str = Field(description="Name of the kernel")
    kernel_configs: list[KernelConfig] = Field(
        default_factory=list, description="List of kernel configuration settings"
    )


class IntentionalKernelConfigSchema(BaseModel):
    """Root schema for intentional kernel configuration settings."""

    model_config = {"extra": "forbid"}

    default: KernelObject = Field(description="Default kernel configuration object")
    overrides: list[KernelObject] = Field(
        default_factory=list,
        description="List of kernel override objects (kernel-1 to kernel-n)",
    )


def load_schema(filepath: Path) -> IntentionalKernelConfigSchema:
    """Load the schema from a JSON file."""
    with filepath.open(encoding="utf-8") as file:
        data = json.load(file)
    return IntentionalKernelConfigSchema.model_validate(data)


def save_schema(schema: IntentionalKernelConfigSchema, filepath: Path) -> None:
    """Save the schema to a JSON file."""
    with filepath.open("w", encoding="utf-8") as file:
        json.dump(schema.model_dump(mode="json"), file, indent=2)
