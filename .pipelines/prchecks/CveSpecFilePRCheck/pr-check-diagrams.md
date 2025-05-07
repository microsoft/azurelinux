# Azure Linux PR Check Flow Diagrams

This file contains two different diagram styles to explain the PR check flow for Azure Linux SPEC/patch file reviews.

## 1. Sequence Diagram

This sequence diagram shows the temporal flow of actions and communications between components.

```mermaid
sequenceDiagram
    participant Developer
    participant TopicBranch as Topic Branch
    participant TargetBranch as Target Branch (fasttrack/abadawi/test/3.0)
    participant ADO as Azure DevOps Pipeline
    participant Git as Git Repository
    participant OpenAI as Azure OpenAI

    Developer->>TopicBranch: Create topic branch
    Developer->>TopicBranch: Modify .spec/.patch files
    Developer->>Git: Push changes
    Developer->>TargetBranch: Create PR to target branch

    Note over TargetBranch: PR triggered with<br/>SYSTEM_PULLREQUEST_SOURCECOMMITID<br/>SYSTEM_PULLREQUEST_TARGETCOMMITID

    TargetBranch->>ADO: Trigger PR check pipeline
    
    ADO->>Git: Checkout repository
    ADO->>ADO: Set up environment<br/>(apply-security-config.sh)
    
    Note over ADO: 1. Export OpenAI credentials<br/>2. Map to AZURE_OPENAI_* variables

    ADO->>Git: git diff between source & target commits
    
    Note over Git: Compare SYSTEM_PULLREQUEST_SOURCECOMMITID<br/>with SYSTEM_PULLREQUEST_TARGETCOMMITID

    Git->>ADO: Return diff content (.spec/.patch files)
    
    Note over ADO: CveSpecFileRecommenderClass.py processes diffs

    ADO->>OpenAI: Send diffs for analysis
    OpenAI->>ADO: Return AI analysis/recommendations
    ADO->>Developer: Show analysis in pipeline logs

    Note over Developer,OpenAI: The AI reviews code changes<br/>and provides feedback on security/quality
```

## 2. UML Class Diagram

This UML class diagram shows the structural relationships between components.

```mermaid
classDiagram
    class Developer {
        Creates topic branch
        Modifies .spec/.patch files
        Creates PR
    }

    class GitRepository {
        topic_branch
        target_branch: fasttrack/abadawi/test/3.0
        SYSTEM_PULLREQUEST_SOURCECOMMITID
        SYSTEM_PULLREQUEST_TARGETCOMMITID
        getDiff()
    }

    class PullRequest {
        sourceBranch
        targetBranch
        specFileChanges
        triggerPipeline()
    }

    class ADOPipeline {
        run_in_agent()
        checkout_repo()
        setup_environment()
        run_scripts()
        show_results()
    }
    
    class ApplySecurityConfig {
        exportOpenAICredentials()
        loginWithUMI()
    }
    
    class RunPRCheck {
        mapEnvironmentVariables()
        getBuildSourcesDirectory()
        getPRCommitIDs()
        installDependencies()
        runCveAnalysis()
    }
    
    class CveSpecFileRecommender {
        getGitDiff()
        analyzeWithOpenAI()
        generateReport()
    }
    
    class AzureOpenAI {
        endpoint
        deploymentName
        analyzeDiffs()
        provideRecommendations()
    }
    
    Developer --> GitRepository : pushes to
    Developer --> PullRequest : creates
    PullRequest --> GitRepository : references
    PullRequest --> ADOPipeline : triggers
    ADOPipeline --> ApplySecurityConfig : executes
    ADOPipeline --> RunPRCheck : executes
    RunPRCheck --> CveSpecFileRecommender : invokes
    CveSpecFileRecommender --> GitRepository : gets diff from
    CveSpecFileRecommender --> AzureOpenAI : sends diffs to
    AzureOpenAI --> CveSpecFileRecommender : returns analysis
    CveSpecFileRecommender --> ADOPipeline : provides results
    ADOPipeline --> Developer : shows results to

    note for Developer "Makes changes to .spec/.patch files in SPECS directory"
    note for GitRepository "Source of diffs between source and target commits"
    note for PullRequest "Must target fasttrack/abadawi/test/3.0 branch"
    note for ADOPipeline "Azure DevOps Pipeline with mariner-dev-build-1es-mariner2-amd64 agent"
    note for AzureOpenAI "AI model that analyzes security implications of spec/patch changes"
```

## Process Explanation

### 1. PR Creation Process
- Developer creates a branch from the target branch (`fasttrack/abadawi/test/3.0`)
- Developer modifies `.spec` or `.patch` files in the `SPECS` directory
- Developer creates a PR targeting `fasttrack/abadawi/test/3.0`
- ADO pipeline is triggered automatically when it detects these changes

### 2. Pipeline Execution Process
- The pipeline runs on the mariner-dev-build-1es-mariner2-amd64 agent
- `apply-security-config.sh` authenticates with UMI and exports OpenAI credentials
- `run-pr-check.sh` maps environment variables and prepares the environment
- Git diff is extracted between source and target commits
- `CveSpecFileRecommenderClass.py` sends the diffs to Azure OpenAI for analysis
- Results are displayed in the pipeline logs

### 3. Key Environment Variables
- `AZURE_OPENAI_ENDPOINT`: The Azure OpenAI API endpoint (mapped from OPENAI_API_BASE)
- `AZURE_OPENAI_DEPLOYMENT_NAME`: The deployment name (mapped from OPENAI_DEPLOYMENT_NAME)
- `SYSTEM_PULLREQUEST_SOURCECOMMITID`: The source commit ID of the PR
- `SYSTEM_PULLREQUEST_TARGETCOMMITID`: The target commit ID of the PR
- `BUILD_SOURCESDIRECTORY`: The directory containing the source code