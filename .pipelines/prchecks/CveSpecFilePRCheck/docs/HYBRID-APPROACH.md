# RADAR Hybrid Approach: Comments + Labels

The RADAR challenge system uses a **hybrid approach** combining GitHub comments and labels for maximum visibility and tracking.

## Why Hybrid?

1. **Comments** - Provide detailed context and feedback
2. **Labels** - Enable quick filtering, dashboards, and automation

## How It Works

When a user submits a challenge via the HTML report:

### 1. Analytics Saved to Blob Storage
- Challenge data saved to `PR-{number}/analytics.json`
- Includes challenge type, feedback text, user info, timestamp
- Used for metrics and analytics

### 2. GitHub Comment Posted
A formatted comment is posted to the PR with:
- Challenge type emoji (🟢 False Alarm / 🟡 Needs Context / 🔴 Acknowledged)
- Antipattern ID and spec file
- Submitter's username
- Feedback text
- Unique challenge ID

### 3. GitHub Labels Added
Two labels are added to the PR:
- **General label**: `radar:challenged` - Indicates PR has been reviewed
- **Type-specific label**:
  - `radar:false-positive` - Finding is incorrect (🟢 Green)
  - `radar:needs-context` - Requires explanation (🟡 Orange)
  - `radar:acknowledged` - Author agrees with finding (🔴 Red)

## Label Setup

Before using the system, create the labels in the repository:

```bash
cd .pipelines/prchecks/CveSpecFilePRCheck/azure-function
chmod +x create-github-labels.sh
./create-github-labels.sh
```

Or create manually at: https://github.com/microsoft/azurelinux/labels

## Benefits

### For PR Authors
- See challenge comments directly in PR conversation
- Quick visual indication via labels
- Can filter their PRs by challenge type

### For Reviewers
- Filter PRs with challenges: `label:radar:challenged`
- Find false positives: `label:radar:false-positive`
- Dashboard queries for analytics

### For Automation
- Trigger workflows based on labels
- Auto-assign reviewers for challenged PRs
- Generate reports on challenge rates

## Example

When a user challenges a finding as a false positive:

1. **Comment posted**:
```markdown
## 🟢 Challenge Submitted

**Finding**: missing-patch-file in `SPECS/curl/curl.spec`  
**Challenge Type**: False Alarm  
**Submitted by**: @username  

**Feedback**:
> This patch file is referenced but the actual file exists with a different name

---
*Challenge ID: `ch-001` • This challenge will be reviewed by the team.*
```

2. **Labels added**:
- `radar:challenged`
- `radar:false-positive`

3. **Analytics updated**:
```json
{
  "pr_number": 14904,
  "challenges": [
    {
      "challenge_id": "ch-001",
      "challenge_type": "false-positive",
      "submitted_by": {"username": "user", "email": "..."},
      "feedback_text": "This patch file is referenced...",
      "status": "submitted"
    }
  ]
}
```

## Label Colors

- 🟢 **radar:false-positive** - Green (#00FF00) - Safe to ignore
- 🟡 **radar:needs-context** - Orange (#FFA500) - Needs review
- 🔴 **radar:acknowledged** - Red (#FF0000) - Confirmed issue
- ✅ **radar:challenged** - Dark Green (#0E8A16) - General indicator
