# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ---------------------------------------------------------

import json

from .schema import IntentionalKernelConfigSchema


def get_schema() -> str:
    """Return the JSON schema for kernel configuration settings."""
    schema = IntentionalKernelConfigSchema.model_json_schema()
    return json.dumps(schema, indent=2)


if __name__ == "__main__":
    print(get_schema())
