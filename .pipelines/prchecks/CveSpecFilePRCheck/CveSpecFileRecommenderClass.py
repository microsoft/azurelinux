import os, subprocess, sys
from azure.identity import DefaultAzureCredential
from azure.ai.openai import OpenAIClient

def gather_diff():
    src = os.environ["SYSTEM_PULLREQUEST_SOURCECOMMITID"]
    tgt = os.environ["SYSTEM_PULLREQUEST_TARGETCOMMITID"]
    diff = subprocess.check_output(
        ["git", "diff", "--unified=0", tgt, src],
        cwd=os.environ["BUILD_SOURCESDIRECTORY"]
    )
    return diff.decode()

def call_openai(diff_text):
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    deployment = os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"]
    credential = DefaultAzureCredential()
    client = OpenAIClient(endpoint=endpoint, credential=credential)
    resp = client.get_chat_completions(
        deployment_name=deployment,
        messages=[
            {"role":"system","content":"You are a code reviewer."},
            {"role":"user","content":f"Review this diff:\n```diff\n{diff_text}\n```"}
        ]
    )
    return resp.choices[0].message.content

if __name__ == "__main__":
    diff = gather_diff()
    if not diff.strip():
        print("⚠️ No changes detected.")
        sys.exit(0)
    review = call_openai(diff)
    print("\n=== LLM REVIEW ===\n", review)
