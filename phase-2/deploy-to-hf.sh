#!/bin/bash

# Hugging Face Spaces Deployment Script
# Usage: ./deploy-to-hf.sh YOUR_HF_USERNAME YOUR_SPACE_NAME

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check arguments
if [ "$#" -ne 2 ]; then
    echo -e "${RED}Error: Missing arguments${NC}"
    echo "Usage: ./deploy-to-hf.sh YOUR_HF_USERNAME YOUR_SPACE_NAME"
    echo "Example: ./deploy-to-hf.sh johndoe phase-2-todo-api"
    exit 1
fi

HF_USERNAME=$1
SPACE_NAME=$2
HF_REPO="https://huggingface.co/spaces/${HF_USERNAME}/${SPACE_NAME}"

echo -e "${GREEN}=== Hugging Face Spaces Deployment ===${NC}"
echo "Username: ${HF_USERNAME}"
echo "Space Name: ${SPACE_NAME}"
echo "Repository: ${HF_REPO}"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}Error: git is not installed${NC}"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "main.py" ] || [ ! -f "Dockerfile" ]; then
    echo -e "${RED}Error: Please run this script from the phase-2 directory${NC}"
    exit 1
fi

# Backup current README if exists
if [ -f "README.md" ]; then
    echo -e "${YELLOW}Backing up current README.md to README.backup.md${NC}"
    cp README.md README.backup.md
fi

# Copy HF README
echo -e "${GREEN}Copying Hugging Face README...${NC}"
cp README_HF.md README.md

# Check if hf remote exists
if git remote | grep -q "^hf$"; then
    echo -e "${YELLOW}Removing existing 'hf' remote...${NC}"
    git remote remove hf
fi

# Add Hugging Face remote
echo -e "${GREEN}Adding Hugging Face remote...${NC}"
git remote add hf ${HF_REPO}

# Create deployment branch
CURRENT_BRANCH=$(git branch --show-current)
echo -e "${GREEN}Current branch: ${CURRENT_BRANCH}${NC}"

if git show-ref --verify --quiet refs/heads/hf-deploy; then
    echo -e "${YELLOW}Switching to existing hf-deploy branch...${NC}"
    git checkout hf-deploy
    git merge ${CURRENT_BRANCH} -m "Merge latest changes for HF deployment"
else
    echo -e "${GREEN}Creating new hf-deploy branch...${NC}"
    git checkout -b hf-deploy
fi

# Stage changes
echo -e "${GREEN}Staging files for deployment...${NC}"
git add README.md Dockerfile main.py pyproject.toml uv.lock alembic.ini
git add src/ alembic/ 2>/dev/null || true

# Check if there are changes to commit
if git diff --staged --quiet; then
    echo -e "${YELLOW}No changes to commit${NC}"
else
    echo -e "${GREEN}Committing changes...${NC}"
    git commit -m "Deploy to Hugging Face Spaces

- Updated README for HF Spaces
- Configured Dockerfile with auto-migrations
- Ready for deployment"
fi

# Push to Hugging Face
echo -e "${GREEN}Pushing to Hugging Face Spaces...${NC}"
echo -e "${YELLOW}You may be prompted for your Hugging Face credentials${NC}"
git push hf hf-deploy:main

# Switch back to original branch
echo -e "${GREEN}Switching back to ${CURRENT_BRANCH}...${NC}"
git checkout ${CURRENT_BRANCH}

# Restore original README
if [ -f "README.backup.md" ]; then
    echo -e "${GREEN}Restoring original README...${NC}"
    mv README.backup.md README.md
fi

echo ""
echo -e "${GREEN}=== Deployment Complete! ===${NC}"
echo ""
echo "Next steps:"
echo "1. Go to: https://huggingface.co/spaces/${HF_USERNAME}/${SPACE_NAME}"
echo "2. Configure environment variables in Space settings:"
echo "   - DATABASE_URL (your Neon PostgreSQL connection string)"
echo "   - AUTH_SECRET_KEY (generate a secure random key)"
echo "   - DEBUG=false"
echo "3. Wait for the Space to build (2-5 minutes)"
echo "4. Test your API at: https://${HF_USERNAME}-${SPACE_NAME}.hf.space"
echo ""
echo -e "${YELLOW}Important: Don't forget to set up your environment variables!${NC}"
