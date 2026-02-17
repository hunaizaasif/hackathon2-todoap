#!/usr/bin/env python3
"""Upload Phase 2 files to Hugging Face Space"""

import os
import sys
import subprocess

# Hugging Face credentials
HF_TOKEN = "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"
SPACE_ID = "Amber-Asif/todo-app-phase-2"
DEPLOY_DIR = "/mnt/e/Hackathon-2/temp-hf-deploy"

def run_command(cmd):
    """Run shell command and return output"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print("🚀 Deploying Phase 2 to Hugging Face...")
    print(f"📦 Source: {DEPLOY_DIR}")
    print(f"🎯 Target: {SPACE_ID}")
    print()

    # Change to deployment directory
    os.chdir(DEPLOY_DIR)

    # Configure git with token
    print("🔧 Configuring git...")
    git_url = f"https://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@huggingface.co/spaces/{SPACE_ID}"

    # Remove existing remote
    run_command("git remote remove hf 2>/dev/null")

    # Add remote with token
    success, stdout, stderr = run_command(f"git remote add hf {git_url}")
    if not success:
        print(f"❌ Failed to add remote: {stderr}")
        return 1

    print("✅ Git configured")

    # Push to Hugging Face
    print("📤 Pushing files to Hugging Face...")
    print("   This may take 1-2 minutes...")

    # Use GIT_TERMINAL_PROMPT=0 to prevent interactive prompts
    cmd = "GIT_TERMINAL_PROMPT=0 git push hf main --force 2>&1"
    success, stdout, stderr = run_command(cmd)

    if success or "Everything up-to-date" in stdout:
        print()
        print("✅ Deployment successful!")
        print()
        print("🔐 Next step: Set environment variables")
        print("   Go to: https://huggingface.co/spaces/Amber-Asif/todo-app-phase-2/settings")
        print()
        print("   Add these secrets:")
        print("   DATABASE_URL = your_neon_connection_string?sslmode=require")
        print("   AUTH_SECRET_KEY = 18d4R14KL0ZO8uNvnw29IoJvn9iLtrkbzrCwEdGMCSg")
        print("   DEBUG = false")
        print()
        print("🌐 Your API will be live at:")
        print("   https://amber-asif-todo-app-phase-2.hf.space")
        return 0
    else:
        print(f"❌ Push failed!")
        print(f"Output: {stdout}")
        print(f"Error: {stderr}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
