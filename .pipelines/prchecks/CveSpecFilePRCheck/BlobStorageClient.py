#!/usr/bin/env python3
"""
BlobStorageClient.py
Azure Blob Storage client for uploading analysis reports and HTML files.
Uses User Managed Identity (UMI) authentication via DefaultAzureCredential.
"""

import logging
from datetime import datetime
from typing import Optional, List
from azure.storage.blob import BlobServiceClient, ContentSettings, PublicAccess
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import AzureError, ResourceNotFoundError

logger = logging.getLogger(__name__)


class BlobStorageClient:
    """
    Client for uploading analysis data and HTML reports to Azure Blob Storage.
    
    Uses DefaultAzureCredential which automatically detects:
    - Managed Identity (UMI/SMI) in Azure environments (e.g., Azure DevOps agents)
    - Azure CLI credentials for local development
    - Environment variables (AZURE_CLIENT_ID, AZURE_TENANT_ID, etc.)
    """
    
    def __init__(self, storage_account_name: str, container_name: str):
        """
        Initialize the Blob Storage client.
        
        Args:
            storage_account_name: Name of the Azure Storage account (e.g., 'radarblobstore')
            container_name: Name of the container (e.g., 'radarcontainer')
        """
        self.storage_account_name = storage_account_name
        self.container_name = container_name
        self.account_url = f"https://{storage_account_name}.blob.core.windows.net"
        
        logger.info(f"🚀 Initializing BlobStorageClient...")
        logger.info(f"   Storage Account: {storage_account_name}")
        logger.info(f"   Container: {container_name}")
        logger.info(f"   Account URL: {self.account_url}")
        
        # Initialize credential (will use UMI in pipeline, Azure CLI locally)
        logger.info(f"🔐 Creating DefaultAzureCredential (will auto-detect UMI in pipeline)...")
        self.credential = DefaultAzureCredential()
        logger.info(f"✅ Credential created successfully")
        
        # Initialize blob service client
        logger.info(f"🔗 Creating BlobServiceClient...")
        self.blob_service_client = BlobServiceClient(
            account_url=self.account_url,
            credential=self.credential
        )
        logger.info(f"✅ BlobServiceClient created successfully")
        
        # Test connection on initialization
        logger.info(f"🧪 Testing connection to blob storage...")
        if self.test_connection():
            logger.info(f"✅✅✅ BlobStorageClient initialized successfully!")
        else:
            logger.warning(f"⚠️  BlobStorageClient initialized but connection test failed - blob operations may fail")
        
        # Run diagnostics
        self._run_diagnostics()
        
        # Ensure container exists with public access
        logger.info(f"📦 Ensuring container exists with public blob access...")
        if self._ensure_container_exists_with_public_access():
            logger.info(f"✅ Container is ready for blob uploads")
        else:
            logger.error(f"❌ Container setup failed - blobs may not be publicly accessible")
    
    def _run_diagnostics(self):
        """Run diagnostic checks on storage account and container."""
        try:
            logger.info(f"🔍 Running diagnostics on storage account and containers...")
            
            # List all containers
            self._list_all_containers()
            
            # Check if our target container exists and its public access level
            self._check_container_status()
            
        except Exception as e:
            logger.error(f"❌ Error during diagnostics: {e}")
            logger.exception(e)
    
    def _list_all_containers(self):
        """List all containers in the storage account (diagnostic)."""
        try:
            logger.info(f"📦 Listing all containers in storage account '{self.storage_account_name}':")
            
            containers = list(self.blob_service_client.list_containers())
            
            if not containers:
                logger.warning(f"⚠️  No containers found in storage account!")
                return
            
            for container in containers:
                public_access = container.public_access or "Private (None)"
                logger.info(f"   📦 Container: '{container.name}' | Public Access: {public_access}")
            
            logger.info(f"✅ Found {len(containers)} container(s) total")
            
        except Exception as e:
            logger.error(f"❌ Failed to list containers: {e}")
            logger.exception(e)
    
    def _check_container_status(self):
        """Check if target container exists and log its configuration."""
        try:
            logger.info(f"🔍 Checking target container '{self.container_name}':")
            
            container_client = self.blob_service_client.get_container_client(self.container_name)
            
            # Check if container exists
            exists = container_client.exists()
            
            if not exists:
                logger.error(f"❌ Container '{self.container_name}' DOES NOT EXIST!")
                logger.error(f"   This is why blobs cannot be accessed publicly!")
                logger.error(f"   Solution: Create container with public blob access")
                return False
            
            # Get container properties
            properties = container_client.get_container_properties()
            public_access = properties.public_access or "Private (None)"
            
            logger.info(f"✅ Container '{self.container_name}' exists")
            logger.info(f"   Public Access Level: {public_access}")
            logger.info(f"   Last Modified: {properties.last_modified}")
            
            if public_access == "Private (None)" or not properties.public_access:
                logger.error(f"❌ Container has NO public access!")
                logger.error(f"   Blobs in this container will NOT be publicly accessible!")
                logger.error(f"   Current setting: {public_access}")
                logger.error(f"   Required setting: 'blob' (for blob-level public access)")
                return False
            else:
                logger.info(f"✅ Public access is configured: {public_access}")
                return True
                
        except ResourceNotFoundError:
            logger.error(f"❌ Container '{self.container_name}' NOT FOUND!")
            return False
        except Exception as e:
            logger.error(f"❌ Error checking container status: {e}")
            logger.exception(e)
            return False
    
    def _ensure_container_exists_with_public_access(self):
        """
        Ensure container exists with public blob access.
        Creates container if it doesn't exist.
        
        Returns:
            True if container exists/was created with public access, False otherwise
        """
        try:
            container_client = self.blob_service_client.get_container_client(self.container_name)
            
            # Check if container exists
            if container_client.exists():
                logger.info(f"✅ Container '{self.container_name}' already exists")
                
                # Check public access level
                properties = container_client.get_container_properties()
                public_access = properties.public_access
                
                if not public_access or public_access == "None":
                    logger.warning(f"⚠️  Container exists but has NO public access!")
                    logger.warning(f"   Attempting to set public access to 'blob' level...")
                    try:
                        container_client.set_container_access_policy(public_access=PublicAccess.Blob)
                        logger.info(f"✅ Public access set to 'blob' level successfully!")
                        return True
                    except Exception as set_error:
                        logger.error(f"❌ Failed to set public access: {set_error}")
                        logger.error(f"   Manual action required: Set container public access via Azure Portal")
                        return False
                else:
                    logger.info(f"✅ Container has public access: {public_access}")
                    return True
            else:
                # Container doesn't exist - create it with public access
                logger.warning(f"⚠️  Container '{self.container_name}' does not exist!")
                logger.info(f"📦 Creating container with blob-level public access...")
                
                container_client.create_container(public_access=PublicAccess.Blob)
                
                logger.info(f"✅✅✅ Container created successfully with blob-level public access!")
                return True
                
        except Exception as e:
            logger.error(f"❌ Error ensuring container exists: {e}")
            logger.exception(e)
            return False
    
    def upload_html(
        self,
        pr_number: int,
        html_content: str,
        timestamp: Optional[datetime] = None
    ) -> Optional[str]:
        """
        Upload HTML report to blob storage.
        
        Args:
            pr_number: GitHub PR number
            html_content: HTML content as string
            timestamp: Timestamp for the report (defaults to now)
            
        Returns:
            Public URL of the uploaded blob, or None if upload failed
        """
        if timestamp is None:
            timestamp = datetime.utcnow()
        
        # Format: PR-12345/report-2025-10-15T203450Z.html
        timestamp_str = timestamp.strftime("%Y-%m-%dT%H%M%SZ")
        blob_name = f"PR-{pr_number}/report-{timestamp_str}.html"
        
        try:
            # Log upload attempt with details
            logger.info(f"📤 Starting blob upload for PR #{pr_number}")
            logger.info(f"   Storage Account: {self.storage_account_name}")
            logger.info(f"   Container: {self.container_name}")
            logger.info(f"   Blob Path: {blob_name}")
            logger.info(f"   Content Size: {len(html_content)} bytes")
            
            # Get blob client
            logger.info(f"🔗 Getting blob client for: {self.container_name}/{blob_name}")
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=blob_name
            )
            logger.info(f"✅ Blob client created successfully")
            
            # Set content type for HTML
            content_settings = ContentSettings(content_type='text/html; charset=utf-8')
            logger.info(f"📝 Content-Type set to: text/html; charset=utf-8")
            
            # Upload
            logger.info(f"⬆️  Uploading blob content ({len(html_content)} bytes)...")
            upload_result = blob_client.upload_blob(
                data=html_content,
                content_settings=content_settings,
                overwrite=True
            )
            logger.info(f"✅ Blob upload completed successfully")
            logger.info(f"   ETag: {upload_result.get('etag', 'N/A')}")
            logger.info(f"   Last Modified: {upload_result.get('last_modified', 'N/A')}")
            
            # Generate public URL
            blob_url = f"{self.account_url}/{self.container_name}/{blob_name}"
            logger.info(f"🌐 Generated public URL: {blob_url}")
            
            # Verify blob exists (optional check)
            try:
                blob_properties = blob_client.get_blob_properties()
                logger.info(f"✅ Blob verified - Size: {blob_properties.size} bytes, Content-Type: {blob_properties.content_settings.content_type}")
            except Exception as verify_error:
                logger.warning(f"⚠️  Could not verify blob properties: {verify_error}")
            
            # List blobs for this PR to verify it appears in container
            logger.info(f"🔍 Verifying blob appears in container listing...")
            try:
                blobs = self.list_blobs_in_container(prefix=f"PR-{pr_number}/", max_results=10)
                if blob_name in blobs:
                    logger.info(f"✅ Blob confirmed in container listing!")
                else:
                    logger.warning(f"⚠️  Blob NOT found in container listing (found {len(blobs)} blob(s))")
                    if blobs:
                        logger.warning(f"   Blobs found: {', '.join(blobs)}")
            except Exception as list_error:
                logger.warning(f"⚠️  Could not list blobs for verification: {list_error}")
            
            logger.info(f"✅✅✅ HTML report uploaded successfully to blob storage!")
            return blob_url
            
        except AzureError as e:
            logger.error(f"❌ Azure error during blob upload:")
            logger.error(f"   Error Code: {getattr(e, 'error_code', 'N/A')}")
            logger.error(f"   Error Message: {str(e)}")
            logger.error(f"   Storage Account: {self.storage_account_name}")
            logger.error(f"   Container: {self.container_name}")
            logger.error(f"   Blob Path: {blob_name}")
            logger.exception(e)
            return None
        except Exception as e:
            logger.error(f"❌ Unexpected error during blob upload:")
            logger.error(f"   Error Type: {type(e).__name__}")
            logger.error(f"   Error Message: {str(e)}")
            logger.error(f"   Storage Account: {self.storage_account_name}")
            logger.error(f"   Container: {self.container_name}")
            logger.error(f"   Blob Path: {blob_name}")
            logger.exception(e)
            return None
    
    def upload_json(
        self,
        pr_number: int,
        json_data: str,
        timestamp: Optional[datetime] = None,
        filename_prefix: str = "analysis"
    ) -> Optional[str]:
        """
        Upload JSON analytics data to blob storage.
        
        Args:
            pr_number: GitHub PR number
            json_data: JSON content as string
            timestamp: Timestamp for the data (defaults to now)
            filename_prefix: Prefix for the JSON filename (e.g., 'analysis', 'feedback')
            
        Returns:
            Public URL of the uploaded blob, or None if upload failed
        """
        if timestamp is None:
            timestamp = datetime.utcnow()
        
        # Format: PR-12345/analysis-2025-10-15T203450Z.json
        timestamp_str = timestamp.strftime("%Y-%m-%dT%H%M%SZ")
        blob_name = f"PR-{pr_number}/{filename_prefix}-{timestamp_str}.json"
        
        try:
            logger.info(f"Uploading JSON data to blob: {blob_name}")
            
            # Get blob client
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=blob_name
            )
            
            # Set content type for JSON
            content_settings = ContentSettings(content_type='application/json; charset=utf-8')
            
            # Upload
            blob_client.upload_blob(
                data=json_data,
                content_settings=content_settings,
                overwrite=True
            )
            
            # Generate public URL
            blob_url = f"{self.account_url}/{self.container_name}/{blob_name}"
            logger.info(f"✅ JSON data uploaded successfully: {blob_url}")
            
            return blob_url
            
        except AzureError as e:
            logger.error(f"❌ Failed to upload JSON data: {str(e)}")
            logger.exception(e)
            return None
        except Exception as e:
            logger.error(f"❌ Unexpected error uploading JSON data: {str(e)}")
            logger.exception(e)
            return None
    
    def generate_blob_url(self, pr_number: int, filename: str) -> str:
        """
        Generate a public blob URL for a given PR and filename.
        
        Args:
            pr_number: GitHub PR number
            filename: Filename within the PR folder
            
        Returns:
            Public URL to the blob
        """
        blob_name = f"PR-{pr_number}/{filename}"
        return f"{self.account_url}/{self.container_name}/{blob_name}"
    
    def list_blobs_in_container(self, prefix: str = None, max_results: int = 100) -> list:
        """
        List blobs in the container (for debugging).
        
        Args:
            prefix: Optional prefix to filter blobs (e.g., "PR-14877/")
            max_results: Maximum number of blobs to return
            
        Returns:
            List of blob names
        """
        try:
            logger.info(f"🔍 Listing blobs in container: {self.container_name}")
            if prefix:
                logger.info(f"   Prefix filter: {prefix}")
            
            container_client = self.blob_service_client.get_container_client(self.container_name)
            blob_list = []
            
            for blob in container_client.list_blobs(name_starts_with=prefix):
                blob_list.append(blob.name)
                logger.info(f"   📄 Found blob: {blob.name} (Size: {blob.size} bytes)")
                if len(blob_list) >= max_results:
                    break
            
            if not blob_list:
                logger.warning(f"⚠️  No blobs found in container{' with prefix: ' + prefix if prefix else ''}")
            else:
                logger.info(f"✅ Found {len(blob_list)} blob(s) in container")
            
            return blob_list
            
        except Exception as e:
            logger.error(f"❌ Failed to list blobs: {str(e)}")
            logger.exception(e)
            return []
    
    def verify_blob_exists(self, pr_number: int, filename: str) -> bool:
        """
        Verify if a specific blob exists (for debugging).
        
        Args:
            pr_number: GitHub PR number
            filename: Filename to check
            
        Returns:
            True if blob exists, False otherwise
        """
        try:
            blob_name = f"PR-{pr_number}/{filename}"
            logger.info(f"🔍 Checking if blob exists: {blob_name}")
            
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=blob_name
            )
            
            properties = blob_client.get_blob_properties()
            logger.info(f"✅ Blob exists!")
            logger.info(f"   Size: {properties.size} bytes")
            logger.info(f"   Content-Type: {properties.content_settings.content_type}")
            logger.info(f"   Last Modified: {properties.last_modified}")
            logger.info(f"   Public URL: {self.account_url}/{self.container_name}/{blob_name}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Blob does not exist or cannot be accessed: {blob_name}")
            logger.error(f"   Error: {str(e)}")
            return False
    
    def test_connection(self) -> bool:
        """
        Test the connection to blob storage and verify permissions.
        
        Returns:
            True if connection and permissions are OK, False otherwise
        """
        try:
            logger.info("🔌 Testing blob storage connection and permissions...")
            logger.info(f"   Storage Account: {self.storage_account_name}")
            logger.info(f"   Container: {self.container_name}")
            logger.info(f"   Account URL: {self.account_url}")
            
            # Try to get container properties (requires read permission)
            container_client = self.blob_service_client.get_container_client(self.container_name)
            properties = container_client.get_container_properties()
            
            logger.info(f"✅ Successfully connected to container!")
            logger.info(f"   Container last modified: {properties.last_modified}")
            logger.info(f"   Public access level: {properties.public_access or 'Private (no public access)'}")
            
            # Check if public access is enabled
            if properties.public_access:
                logger.info(f"✅ Public access is ENABLED: {properties.public_access}")
            else:
                logger.warning(f"⚠️  Public access is DISABLED - blobs will not be publicly accessible")
                logger.warning(f"   To fix: Enable 'Blob' level public access on container '{self.container_name}'")
            
            return True
            
        except AzureError as e:
            logger.error(f"❌ Failed to connect to blob storage:")
            logger.error(f"   Error Code: {getattr(e, 'error_code', 'N/A')}")
            logger.error(f"   Error Message: {str(e)}")
            logger.error("   Possible causes:")
            logger.error("   1. UMI doesn't have 'Storage Blob Data Contributor' role")
            logger.error("   2. Container doesn't exist")
            logger.error("   3. Network/firewall issues")
            logger.exception(e)
            return False
        except Exception as e:
            logger.error(f"❌ Unexpected error testing connection: {str(e)}")
            logger.exception(e)
            return False


# Example usage
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Initialize client
    client = BlobStorageClient(
        storage_account_name="radarblobstore",
        container_name="radarcontainer"
    )
    
    # Test connection
    if client.test_connection():
        print("✅ Blob storage connection test passed!")
        
        # Test upload
        test_html = "<html><body><h1>Test Report</h1></body></html>"
        html_url = client.upload_html(pr_number=99999, html_content=test_html)
        
        if html_url:
            print(f"✅ Test HTML uploaded: {html_url}")
        
        test_json = '{"test": true, "pr_number": 99999}'
        json_url = client.upload_json(pr_number=99999, json_data=test_json)
        
        if json_url:
            print(f"✅ Test JSON uploaded: {json_url}")
    else:
        print("❌ Blob storage connection test failed!")
        print("   See MANUAL_ADMIN_STEPS.md for required Azure configuration")
