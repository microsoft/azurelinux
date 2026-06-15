# CVE Spec File PR Check

## Overview

The CVE Spec File PR Check is an AI-assisted pipeline that automatically analyzes pull requests containing changes to Azure Linux spec files. It combines programmatic anti-pattern detection with Azure OpenAI analysis to provide comprehensive feedback on spec file modifications, focusing on CVE-related changes, patch management, and spec file best practices.

## 🚀 Key Features

- **Dual Analysis Approach**: Combines rule-based anti-pattern detection with AI-powered analysis
- **Structured Output**: Generates brief PR comments and detailed pipeline logs separately
- **Integrated GitHub Integration**: Posts concise comments directly to PRs with critical issues
- **Severity-Based Pipeline Control**: Fails pipeline on critical/error issues, warns on minor issues
- **Comprehensive Reporting**: Creates detailed reports for Azure DevOps pipeline logs

## 🔄 Architecture Overview

```
┌─────────────────────────────────────────────┐
│  GitHub PR → Azure DevOps Pipeline         │
│  (via webhook trigger)                     │
└─────────────────────────────────────────────┘
                ↓
┌─────────────────────────────────────────────┐
│  azure-pipelines.yml                       │
│  PR trigger on fasttrack/*/3.0 branches    │
└─────────────────────────────────────────────┘
                ↓
    1) Checkout repository
    2) Apply OpenAI configuration
    3) Install Python dependencies  
    4) Run CveSpecFilePRCheck.py
                ↓
┌─────────────────────────────────────────────┐
│  🔍 Analysis Pipeline                       │
│  • Git diff extraction                     │
│  • Anti-pattern detection                  │
│  • AI-powered analysis                     │
│  • Structured result processing            │
│  • GitHub integration                      │
└─────────────────────────────────────────────┘
```

## 📁 Project Structure

```
CveSpecFilePRCheck/
├── README.md                    # This documentation
├── requirements.txt             # Python dependencies
├── run-pr-check.sh             # Bash entry point
├── CveSpecFilePRCheck.py       # Main Python script
├── AntiPatternDetector.py      # Rule-based detection
├── ResultAnalyzer.py           # Result processing & formatting
├── PromptTemplatesClass.py     # AI prompt templates
├── OpenAIClientClass.py        # Azure OpenAI integration
├── GptModelConfigClass.py      # AI model configuration
├── GitHubClient.py            # GitHub API integration
├── apply-security-config.sh    # Azure authentication
└── docs/                       # Documentation and UML diagrams
    ├── class-diagram.puml
    ├── sequence-diagram.puml
    └── data-flow-diagram.puml
```

## 🏗️ Class Architecture

### Core Classes

1. **CveSpecFilePRCheck** (Main Entry Point)
   - Orchestrates the entire analysis pipeline
   - Handles git diff extraction and file processing
   - Coordinates between anti-pattern detection and AI analysis
   - Manages GitHub integration and pipeline exit codes

2. **AntiPatternDetector**
   - Implements rule-based detection for common spec file issues
   - Detects missing patches, unreferenced files, CVE changelog issues
   - Returns structured AntiPattern objects with severity levels

3. **ResultAnalyzer**
   - Processes results from both detection methods
   - Parses structured AI output (brief vs detailed sections)
   - Generates formatted reports for different audiences
   - Handles severity-based pipeline decisions

4. **PromptTemplatesClass**
   - Provides structured prompt templates for AI analysis
   - Requests AI output in two sections: brief PR comments and detailed logs
   - Supports different analysis types (general, patch verification, CVE validation)

5. **OpenAIClient**
   - Handles Azure OpenAI API communication
   - Manages authentication and model configuration
   - Provides chat completion functionality

6. **GitHubClient**
   - Manages GitHub API integration
   - Posts/updates PR comments with brief analysis
   - Supports GitHub Checks API for status updates

### 📊 Visual Architecture

For detailed visual representations of the system architecture, see the UML diagrams in the `docs/` directory:

- **[Class Diagram](docs/class-diagram.puml)**: Shows relationships between all classes
- **[Sequence Diagram](docs/sequence-diagram.puml)**: Illustrates the complete execution flow
- **[Data Flow Diagram](docs/data-flow-diagram.puml)**: Demonstrates data transformation through the system
- **[System Architecture](docs/system-architecture.puml)**: High-level view of system components

> **Note**: UML diagrams are in PlantUML format. View them at [plantuml.com](http://www.plantuml.com/plantuml/uml/) or use the PlantUML VS Code extension.

## 🔄 Execution Flow

### Phase 1: Setup and Authentication
```bash
run-pr-check.sh
├── Apply Azure authentication (apply-security-config.sh)
├── Map environment variables for Azure OpenAI
├── Install Python dependencies
└── Execute CveSpecFilePRCheck.py
```

### Phase 2: Analysis Pipeline
```python
CveSpecFilePRCheck.main()
├── Extract git diff between source and target commits
├── Identify changed .spec files
├── Run anti-pattern detection
│   ├── Check for missing patch files
│   ├── Validate patch references
│   ├── Verify CVE changelog entries
│   └── Detect duplicate references
├── Perform AI analysis
│   ├── General spec analysis
│   ├── Patch verification (if patches exist)
│   └── CVE validation (if CVE IDs found)
└── Process and format results
```

### Phase 3: Result Processing
```python
ResultAnalyzer
├── Parse structured AI output
│   ├── Extract brief summary for PR comments
│   └── Extract detailed analysis for logs
├── Generate console summary
├── Create comprehensive reports
├── Determine pipeline status
└── Generate GitHub comment content
```

### Phase 4: GitHub Integration
```python
update_github_status()
├── Post/update PR comments with brief analysis
├── Update GitHub Checks API status
├── Handle authentication via GitHub token
└── Manage comment lifecycle (create/update)
```

## 📊 Output Structure

### Structured AI Output Format
The AI is prompted to provide output in two distinct sections:

```
SECTION 1: BRIEF PR COMMENT SUMMARY
- Concise overview of critical issues
- Key recommendations for PR authors
- Focused on actionable items

SECTION 2: DETAILED ANALYSIS FOR LOGS
- Comprehensive technical analysis
- Detailed explanations and context
- Full recommendations and best practices
```

### Generated Reports

1. **Console Summary**: Brief overview printed to pipeline console
2. **PR Comments**: Concise GitHub comments focusing on critical issues
3. **Pipeline Logs**: Detailed analysis logged to Azure DevOps
4. **JSON Report**: Machine-readable results for further processing
5. **Text Report**: Human-readable detailed analysis file

## 🔧 Configuration

### Environment Variables
```bash
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=<endpoint-url>
AZURE_OPENAI_DEPLOYMENT_NAME=<deployment-name>
AZURE_OPENAI_MODEL_NAME=<model-name>
AZURE_OPENAI_API_VERSION=<api-version>

# GitHub Integration
GITHUB_TOKEN=<github-token>
GITHUB_REPOSITORY=<owner/repo>
GITHUB_PR_NUMBER=<pr-number>

# Azure DevOps
BUILD_SOURCESDIRECTORY=<repo-root>
SYSTEM_PULLREQUEST_SOURCECOMMITID=<source-commit>
SYSTEM_PULLREQUEST_TARGETCOMMITID=<target-commit>
```

### Command Line Options
```bash
python CveSpecFilePRCheck.py [options]

Options:
  --fail-on-warnings         Fail pipeline on warning-level issues
  --exit-code-severity       Use different exit codes for different severities
  --post-github-comments     Post analysis results as GitHub PR comments
  --use-github-checks        Use GitHub Checks API for status updates
```

## 🎯 Anti-Pattern Detection

### Detected Patterns

1. **Missing Patch Files**: Referenced patches that don't exist in the directory
2. **Unreferenced Patch Files**: Patch files not referenced in the spec
3. **Missing Patch Application**: Patches referenced but not applied in %prep
4. **Duplicate Patch References**: Same patch number defined multiple times
5. **Missing CVE Changelog Entries**: CVE IDs in patches but not in changelog

### Severity Levels
- **CRITICAL**: Severe issues that break functionality
- **ERROR**: Issues that must be fixed before merging
- **WARNING**: Issues that should be addressed but don't block merging
- **INFO**: Informational notices for improvement

## 🔗 GitHub Integration

### Comment Management
- **Smart Updates**: Updates existing comments instead of creating duplicates
- **Brief Focus**: Comments contain only critical issues and key recommendations
- **Detailed Logs**: Full analysis remains in Azure DevOps pipeline logs

### Status Checks
- **GitHub Checks API**: Provides detailed status with expandable sections
- **PR Status**: Clear pass/fail indication based on severity levels
- **Navigation**: Links back to pipeline logs for full details

## 🚨 Exit Codes

| Exit Code | Meaning | Description |
|-----------|---------|-------------|
| 0 | Success | No critical issues detected |
| 1 | Critical | Critical or error-level issues found |
| 2 | Error | Error-level issues found |
| 3 | Warning | Warning-level issues found (only if --fail-on-warnings) |
| 10 | Fatal | Unexpected error during execution |

## 🔍 Usage Examples

### Basic Analysis
```bash
./run-pr-check.sh
```

### Fail on Warnings
```bash
./run-pr-check.sh --fail-on-warnings
```

### With GitHub Integration
```bash
./run-pr-check.sh --post-github-comments --use-github-checks
```

### Severity-Based Exit Codes
```bash
./run-pr-check.sh --exit-code-severity
```

## 📈 Performance Optimizations

### Removed Redundancies
- **Eliminated FixRecommender**: AI analysis now includes dynamic recommendations
- **Consolidated GitHub Integration**: Comments posted directly from main script
- **Structured Output**: Single AI call generates both brief and detailed content
- **Optimized File Processing**: Efficient git diff parsing and spec file analysis

### Enhanced Efficiency
- **Smart Parsing**: Fallback mechanisms for unstructured AI responses
- **Batched Operations**: Single AI call for multiple analysis types per file
- **Cached Results**: Reuse parsed data across multiple processing steps

## 🧪 Testing

### Local Testing
```bash
# Set required environment variables
export BUILD_SOURCESDIRECTORY=/path/to/repo
export SYSTEM_PULLREQUEST_SOURCECOMMITID=abc123
export SYSTEM_PULLREQUEST_TARGETCOMMITID=def456

# Run the check
./run-pr-check.sh
```

### Validation
- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end pipeline validation
- **Mock AI Responses**: Test structured parsing with known inputs

## 📚 Dependencies

### Python Packages
```
openai>=1.0.0
requests>=2.25.0
azure-identity>=1.12.0
azure-keyvault-secrets>=4.7.0
```

### System Requirements
- Python 3.8+
- Git
- Azure CLI (for authentication)
- jq (for JSON processing in bash scripts)

## 🤝 Contributing

1. **Code Style**: Follow PEP 8 guidelines
2. **Documentation**: Update docstrings and comments
3. **Testing**: Add tests for new functionality
4. **Logging**: Use structured logging with appropriate levels

## 📚 Documentation

Comprehensive documentation and visual diagrams are available in the `docs/` directory:

- **[Documentation Overview](docs/README.md)**: Complete guide to understanding the system
- **UML Diagrams**: Visual representations of system architecture and component interactions
- **Architecture Analysis**: Detailed explanations of optimizations and design decisions

The documentation includes PlantUML diagrams that can be viewed online or with appropriate tools.

## 📄 License

Copyright (c) Microsoft Corporation. Licensed under the MIT License.