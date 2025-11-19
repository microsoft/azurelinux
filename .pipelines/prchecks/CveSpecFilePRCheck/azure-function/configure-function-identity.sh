#!/bin/bash
# Configure Azure Function with UMI client ID for blob storage access
# This fixes the "Submitting..." stuck issue when users submit challenges

FUNCTION_APP_NAME="radarfunc"
RESOURCE_GROUP="Radar-Storage-RG"
UMI_CLIENT_ID="7bf2e2c3-009a-460e-90d4-eff987a8d71d"  # cblmargh-identity

echo "🔧 Configuring Azure Function with UMI client ID..."
echo "   Function App: $FUNCTION_APP_NAME"
echo "   Resource Group: $RESOURCE_GROUP"
echo "   UMI Client ID: $UMI_CLIENT_ID"

# Add AZURE_CLIENT_ID to function app settings
az functionapp config appsettings set \
  --name "$FUNCTION_APP_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --settings "AZURE_CLIENT_ID=$UMI_CLIENT_ID" \
  --output table

if [ $? -eq 0 ]; then
  echo "✅ Successfully configured AZURE_CLIENT_ID"
  echo ""
  echo "📋 Current app settings:"
  az functionapp config appsettings list \
    --name "$FUNCTION_APP_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --query "[?name=='AZURE_CLIENT_ID']" \
    --output table
else
  echo "❌ Failed to configure AZURE_CLIENT_ID"
  exit 1
fi

echo ""
echo "🔄 Restarting function app to apply changes..."
az functionapp restart \
  --name "$FUNCTION_APP_NAME" \
  --resource-group "$RESOURCE_GROUP"

if [ $? -eq 0 ]; then
  echo "✅ Function app restarted successfully"
  echo ""
  echo "🎉 Configuration complete! Challenge submissions should now work."
else
  echo "⚠️  Failed to restart function app - you may need to restart manually"
  exit 1
fi
