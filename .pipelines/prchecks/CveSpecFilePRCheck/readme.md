┌─────────────────────────────────────────────┐
│  GitHub PR → ADO pipeline via webhook      │
└─────────────────────────────────────────────┘
                ↓ triggers
┌─────────────────────────────────────────────┐
│  azure-pipelines.yml                       │
│  (in GitHub repo, PR trigger on            │
│   fasttrack/abadawi/test/3.0)              │
└─────────────────────────────────────────────┘
                ↓
    1) checkout self
                ↓
    2) Bash@3 “Apply OpenAI Config”  
       • runs `apply-security-config.sh --openaiModel=o3-mini`  
       • that script:  
         - parses `security-config-dev.json`  
         - jq’s out the UMI client ID and does  
           `az login --identity --client-id $UMI_ID`  
         - jq’s out the right OpenAI endpoint, deployment name, etc.  
         - emits those as pipeline variables via  
           `echo "##vso[task.setvariable variable=…]…"`.  
                ↓
    3) UsePythonVersion@0  
    4) Bash@3 “Install Python Dependencies”  
    5) Bash@3 “Full PR Check (bash wrapper)”  
       • runs your `run-pr-check.sh`, which in turn  
         calls the Python code that:  
         - picks up those pipeline variables  
           (`$(openAiApiBase)`, `$(openAiDeploymentName)`, etc.)  
         - instantiates the Azure OpenAI client  
         - analyzes the `.spec` file and writes recommendations  