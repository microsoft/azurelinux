#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""
GptModelConfig provides configuration for Azure OpenAI models,
including specific handling for reasoning models.
"""

class GptModelConfig:
    """Simple configuration class for GPT models"""
    
    def __init__(self, model_name: str, api_version: str, api_base: str, deployment_name: str) -> None:
        self.model = model_name
        self.api_version = api_version
        self.openai_api_base = api_base
        self.deployment_name = deployment_name
        
        # Set default values
        self.temperature = 0.7
        self.chain_of_thought_temperature = 0.9
        self.completion_style = "chat"
        self.reasoning_effort = 0.5
        
        # Determine if this is a reasoning model based on the name
        self._is_reasoning_model = model_name.startswith("o1") or model_name.startswith("o3")
    
    @property
    def isReasoningModel(self) -> bool:
        """Return whether this is a reasoning model"""
        return self._is_reasoning_model