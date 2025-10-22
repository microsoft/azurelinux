# Creating GitHub Labels for RADAR

Since `gh` CLI is not installed, create the labels manually or use curl:

## Option 1: Manual Creation (Easiest)

Go to: https://github.com/microsoft/azurelinux/labels/new

Create these 4 labels:

### 1. radar:challenged
- **Name**: `radar:challenged`
- **Description**: `RADAR: PR has challenges/feedback from reviewers`
- **Color**: `#0E8A16` (dark green)

### 2. radar:false-positive
- **Name**: `radar:false-positive`
- **Description**: `RADAR: Finding marked as false positive`
- **Color**: `#00FF00` (bright green)

### 3. radar:needs-context
- **Name**: `radar:needs-context`
- **Description**: `RADAR: Finding needs additional explanation`
- **Color**: `#FFA500` (orange)

### 4. radar:acknowledged
- **Name**: `radar:acknowledged`
- **Description**: `RADAR: Finding acknowledged by PR author`
- **Color**: `#FF0000` (red)

## Option 2: Using Curl with GitHub PAT

If you have a GitHub Personal Access Token with `repo` scope:

```bash
GITHUB_TOKEN="your_pat_here"
REPO="microsoft/azurelinux"

# Create labels
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/$REPO/labels \
  -d '{"name":"radar:challenged","description":"RADAR: PR has challenges/feedback from reviewers","color":"0E8A16"}'

curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/$REPO/labels \
  -d '{"name":"radar:false-positive","description":"RADAR: Finding marked as false positive","color":"00FF00"}'

curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/$REPO/labels \
  -d '{"name":"radar:needs-context","description":"RADAR: Finding needs additional explanation","color":"FFA500"}'

curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/$REPO/labels \
  -d '{"name":"radar:acknowledged","description":"RADAR: Finding acknowledged by PR author","color":"FF0000"}'
```

## After Creating Labels

Test by submitting a challenge on the HTML report. The Azure Function will:
1. Post a comment to the PR
2. Add the appropriate labels automatically

View all labels at: https://github.com/microsoft/azurelinux/labels
