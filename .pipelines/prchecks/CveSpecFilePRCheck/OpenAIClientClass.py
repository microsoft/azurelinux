#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""
OpenAIClient adapts Azure OpenAI client requests based on the model configuration.

Important:
    - For reasoning models (o1, mini-o3), special handling is applied:
      - Initial message role is set to "assistant" (vs "system" for standard models)
      - Temperature parameter is omitted (API default of 1.0 is used)
      - Optional reasoning_effort parameter is included when applicable
"""

import logging
from typing import Dict, Any

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI

from GptModelConfigClass import GptModelConfig

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("azure-openai-client")

class OpenAIClient:
    def __init__(self, gpt_model: GptModelConfig):
        """
        Initialize the OpenAIClient with model configuration.

        Args:
            gpt_model: Configuration for the GPT model
        """
        logger.info("Setting up Azure OpenAI client")
        self.__model = gpt_model
        
        # Get token provider for Azure services
        self.__token_provider = get_bearer_token_provider(
            DefaultAzureCredential(), 
            "https://cognitiveservices.azure.com/.default"
        )
        
        # Initialize the client
        self.__client = AzureOpenAI(
            azure_endpoint=gpt_model.openai_api_base,
            api_version=gpt_model.api_version,
            azure_ad_token_provider=self.__token_provider,
        )
        
        # Log configuration details
        logger.info(f"OpenAI client initialized with model: {gpt_model.model}")
        logger.info(f"Deployment: {gpt_model.deployment_name}")
        logger.info(f"API endpoint: {gpt_model.openai_api_base}")
        logger.info(f"Reasoning model: {gpt_model.isReasoningModel}")

    @property
    def is_reasoning_model(self) -> bool:
        """Public property for the reasoning model flag"""
        return self.__model.isReasoningModel
    
    def get_chat_completion(self, system_msg: str, user_msg: str) -> Dict[str, Any]:
        """
        Send a chat completion request to OpenAI and process the response.
        
        Args:
            system_msg: System message (instructions for the assistant)
            user_msg: User message (query)
            
        Returns:
            Dictionary with response content and metadata
        """
        logger.info("Sending chat completion request")
        
        # Set initial role based on model type (assistant for reasoning models, system for others)
        initial_role = "assistant" if self.__model.isReasoningModel else "system"
        
        # Build request parameters
        request_params = {
            "model": self.__model.deployment_name,
            "messages": [
                {"role": initial_role, "content": system_msg},
                {"role": "user", "content": user_msg}
            ]
        }
        
        # Special handling for different model types
        if not self.__model.isReasoningModel:
            # For standard models, include temperature
            request_params["temperature"] = self.__model.temperature
        else:
            # For reasoning models that support reasoning_effort, include it
            logger.info("Using reasoning model defaults (temperature=1.0)")
            if self.__model.model in ("o1", "mini-o3"):
                request_params["reasoning_effort"] = self.__model.reasoning_effort
                logger.info(f"Including reasoning_effort={self.__model.reasoning_effort}")
        
        # Send request to the API
        response = self.__client.chat.completions.create(**request_params)
        
        # Extract content from response
        content = response.choices[0].message.content.strip()
        
        # Return structured result
        return {
            "content": content,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            },
            "model": response.model,
            "api_version": self.__model.api_version,
            "deployment_name": self.__model.deployment_name,
        }