#!/bin/bash
# Configure Azure Function after deployment

echo "🔧 Configuring Azure Function App: radar-func"

# 1. Enable CORS for blob storage origin
echo "📝 Enabling CORS for blob storage origin..."
az functionapp cors add \
  --name radar-func \
  --resource-group Radar-Storage-RG \
  --allowed-origins "https://radarblobstore.blob.core.windows.net"

echo "✅ CORS configured"

# 2. Test health endpoint
echo ""
echo "🧪 Testing health endpoint..."
curl -s https://radar-func-b5axhffvhgajbmhd.canadacentral-01.azurewebsites.net/api/health | jq

# 3. Test challenge endpoint
echo ""
echo "🧪 Testing challenge endpoint..."
curl -s -X POST \
  https://radar-func-b5axhffvhgajbmhd.canadacentral-01.azurewebsites.net/api/challenge \
  -H "Content-Type: application/json" \
  -d '{
    "pr_number": 14877,
    "antipattern_id": "test-001",
    "challenge_type": "false-positive",
    "feedback_text": "Test challenge submission from deployment script",
    "user_email": "ahmedbadawi@microsoft.com"
  }' | jq

echo ""
echo "✅ Configuration and testing complete!"
echo ""
echo "🌐 Function URLs:"
echo "  Health: https://radar-func-b5axhffvhgajbmhd.canadacentral-01.azurewebsites.net/api/health"
echo "  Challenge: https://radar-func-b5axhffvhgajbmhd.canadacentral-01.azurewebsites.net/api/challenge"
