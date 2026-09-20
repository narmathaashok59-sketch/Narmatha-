"""
Script to push files to GitHub repository without needing Git installed.
Uses GitHub REST API.
"""

import base64
import os
import sys
import requests

OWNER = "narmathaashok59-sketch"
REPO = "Narmatha-"
BRANCH = "main"

FILES_TO_PUSH = [
    "Srilanka.py",
    "requirements.txt",
    ".gitignore",
    ".github/workflows/main.yml"
]

def push_files(token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    # 1. Check if repo exists; if not, attempt to create it
    repo_url = f"https://api.github.com/repos/{OWNER}/{REPO}"
    res = requests.get(repo_url, headers=headers)
    if res.status_code == 404:
        print(f"📦 Repository '{OWNER}/{REPO}' not found. Creating it now...")
        create_res = requests.post("https://api.github.com/user/repos", headers=headers, json={
            "name": REPO,
            "private": False,
            "auto_init": True
        })
        if create_res.status_code not in (200, 201):
            print(f"❌ Failed to create repository: {create_res.status_code} - {create_res.text}")
            return
        print(f"✅ Repository '{OWNER}/{REPO}' created successfully!")
    elif res.status_code != 200:
        print(f"❌ GitHub API Error: {res.status_code} - {res.text}")
        return

    # 2. Push each file
    for filepath in FILES_TO_PUSH:
        if not os.path.exists(filepath):
            print(f"⚠️ Skipping {filepath} (file not found locally)")
            continue

        with open(filepath, "rb") as f:
            content_b64 = base64.b64encode(f.read()).decode("utf-8")

        clean_path = filepath.replace("\\", "/")
        file_api_url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{clean_path}"
        
        # Check if file already exists in repo to get SHA
        get_res = requests.get(f"{file_api_url}?ref={BRANCH}", headers=headers)
        payload = {
            "message": f"Upload {filepath} via automated script",
            "content": content_b64,
            "branch": BRANCH
        }
        if get_res.status_code == 200:
            payload["sha"] = get_res.json().get("sha")

        put_res = requests.put(file_api_url, headers=headers, json=payload)
        if put_res.status_code in (200, 201):
            print(f"✅ Successfully pushed: {filepath}")
        else:
            print(f"❌ Failed to push {filepath}: {put_res.status_code} - {put_res.text}")

    print(f"\n🎉 Finished! View your repository at: https://github.com/{OWNER}/{REPO}")

if __name__ == "__main__":
    token = sys.argv[1] if len(sys.argv) > 1 else input("Enter your GitHub Personal Access Token: ").strip()
    if not token:
        print("❌ Error: GitHub token is required.")
        sys.exit(1)
    push_files(token)
