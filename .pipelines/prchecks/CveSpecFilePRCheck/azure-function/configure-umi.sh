#!/bin/bash
# Configure Azure Function with UMI Client ID for blob storage access

set -e

FUNCTION_NAME="radarfunc-eka5fmceg4b5fub0"
RESOURCE_GROUP="Radar-Storage-RG"
UMI_CLIENT_ID="7bf2e2c3-009a-460e-90d4-eff987a8d71d"  # cblmargh-identity

echo "🔧 Configuring Azure Function with UMI Client ID"
echo "   Function: $FUNCTION_NAME"
echo "   Resource Group: $RESOURCE_GROUP"
echo "   UMI Client ID: $UMI_CLIENT_ID"
echo ""

# Set AZURE_CLIENT_ID environment variable
echo "📝 Setting AZURE_CLIENT_ID environment variable..."
az functionapp config appsettings set \
  --name "$FUNCTION_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --settings "AZURE_CLIENT_ID=$UMI_CLIENT_ID" \
  --output table

echo ""
echo "✅ UMI Client ID configured successfully!"
echo ""
echo "🔍 Verifying configuration..."
az functionapp config appsettings list \
  --name "$FUNCTION_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --query "[?name=='AZURE_CLIENT_ID']" \
  --output table

echo ""
echo "✅ Configuration complete!"
echo ""
echo "ℹ️  The Azure Function will now use the cblmargh-identity UMI"
echo "   to authenticate with blob storage (instead of failing with DefaultAzureCredential)"
