#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""
Main entry point for the OpenAI client test script.
"""

import os
import sys

from GptModelConfigClass import GptModelConfig
from OpenAIClientClass import OpenAIClient


def main():
    """Main entry point for the script"""
    # Read environment variables exported from the pipeline
    api_version = os.getenv("openAiApiVersion")
    api_base = os.getenv("openAiApiBase")
    deployment_name = os.getenv("openAiDeploymentName")
    model_name = os.getenv("openAiModelName")

    # Validate environment variables
    if not all([api_version, api_base, deployment_name, model_name]):
        print("❌ Missing required environment variables")
        print("Required: openAiApiVersion, openAiApiBase, openAiDeploymentName, openAiModelName")
        sys.exit(1)

    print(f"🔗 API Endpoint: {api_base}")
    print(f"🚀 Deployment: {deployment_name}")
    print(f"🤖 Model: {model_name}")
    print(f"📄 API Version: {api_version}")

    try:
        # Create model configuration
        model_config = GptModelConfig(
            model_name=model_name,
            api_version=api_version,
            api_base=api_base,
            deployment_name=deployment_name
        )
        
        # Initialize client
        client = OpenAIClient(model_config)
        
        # Send a test chat request
        response = client.get_chat_completion(
            system_msg="You are a helpful assistant.",
            user_msg="Say hello world, and tell me the name and version of the model you're running on."
        )
        
        # Display results
        print("\n💬 OpenAI Response:")
        print("=" * 40)
        print(response["content"])
        print("=" * 40)
        print(f"Tokens used: {response['usage']['total_tokens']}")
        
        return 0
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())