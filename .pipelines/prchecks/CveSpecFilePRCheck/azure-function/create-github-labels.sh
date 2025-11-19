#!/bin/bash
# Create GitHub labels for RADAR challenge tracking
# These labels are used in the hybrid approach: comments + labels

REPO="microsoft/azurelinux"

echo "🏷️  Creating RADAR challenge labels in $REPO"
echo ""

# Note: You need to have gh CLI installed and authenticated
# Or use GitHub API directly with a PAT

# Check if gh CLI is available
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) not found. Please install it:"
    echo "   https://cli.github.com/"
    echo ""
    echo "Or create labels manually in GitHub:"
    echo "   https://github.com/$REPO/labels"
    exit 1
fi

# Create labels
echo "Creating label: radar:challenged (general - PR has been reviewed)"
gh label create "radar:challenged" \
  --repo "$REPO" \
  --description "RADAR: PR has challenges/feedback from reviewers" \
  --color "0E8A16" \
  --force 2>&1 || echo "  (label might already exist)"

echo "Creating label: radar:false-positive (False Alarm)"
gh label create "radar:false-positive" \
  --repo "$REPO" \
  --description "RADAR: Finding marked as false positive" \
  --color "00FF00" \
  --force 2>&1 || echo "  (label might already exist)"

echo "Creating label: radar:needs-context (Needs Context)"
gh label create "radar:needs-context" \
  --repo "$REPO" \
  --description "RADAR: Finding needs additional explanation" \
  --color "FFA500" \
  --force 2>&1 || echo "  (label might already exist)"

echo "Creating label: radar:acknowledged (Acknowledged)"
gh label create "radar:acknowledged" \
  --repo "$REPO" \
  --description "RADAR: Finding acknowledged by PR author" \
  --color "FF0000" \
  --force 2>&1 || echo "  (label might already exist)"

echo ""
echo "✅ Label creation complete!"
echo ""
echo "Labels can be viewed at:"
echo "   https://github.com/$REPO/labels"
