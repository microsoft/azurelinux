#!/usr/bin/env bash
#
# Mint a GitHub App installation token.
# Usage: get-github-app-token.sh <App_ID> <Installation_ID> <Key_PEM_Path>

set -euo pipefail

if [ $# -ne 3 ]; then
  echo "Usage: $0 <App_ID> <Installation_ID> <Key_PEM_Path>"
  exit 1
fi

APP_ID="$1"
INSTALL_ID="$2"
KEY_PATH="$3"

# 1) Create a JWT signed with the App's private key
iat=$(date +%s)
exp=$((iat + 600))  # valid for 10 minutes
jwt=$(python3 - <<EOF
import jwt
payload = {"iat": $iat, "exp": $exp, "iss": $APP_ID}
key = open("$KEY_PATH", "r").read()
print(jwt.encode(payload, key, algorithm="RS256"))
EOF
)

# 2) Exchange the JWT for an installation token
token=$(curl -s \
  -X POST \
  -H "Authorization: Bearer $jwt" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/app/installations/$INSTALL_ID/access_tokens \
| python3 -c 'import sys, json; print(json.load(sys.stdin)["token"])'
)

# 3) Output the token
echo "$token"
