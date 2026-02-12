# GitHub Actions Deployment Setup

## Overview

Yeh workflow automatically aapke Phase 2 backend ko Hugging Face Spaces par deploy karega jab bhi aap `main` branch par push karoge.

## Prerequisites

1. ✅ GitHub repository (already have)
2. ✅ Hugging Face account
3. ✅ Neon PostgreSQL database

## Step-by-Step Setup

### Step 1: Create Hugging Face Space

1. Go to https://huggingface.co/spaces
2. Click **"Create new Space"**
3. Fill details:
   - **Owner**: Your username (e.g., `hunaizaasif`)
   - **Space name**: `phase-2-todo-api` (ya koi bhi naam)
   - **License**: MIT
   - **Select the Space SDK**: **Docker** (IMPORTANT!)
   - **Space hardware**: CPU basic (free)
4. Click **"Create Space"**
5. Space URL note karo: `https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME`

### Step 2: Get Hugging Face Access Token

1. Go to https://huggingface.co/settings/tokens
2. Click **"New token"**
3. Token details:
   - **Name**: `github-actions-deploy`
   - **Type**: **Write** (important - read-only won't work)
   - **Repositories**: Select your space or leave as "All"
4. Click **"Generate token"**
5. **COPY THE TOKEN** - you won't see it again!

### Step 3: Configure GitHub Secrets

1. Go to your GitHub repository: `https://github.com/hunaizaasif/hackathon2-todoap`
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"** and add these 3 secrets:

#### Secret 1: HF_USERNAME
```
Name: HF_USERNAME
Value: hunaizaasif  (your Hugging Face username)
```

#### Secret 2: HF_SPACE_NAME
```
Name: HF_SPACE_NAME
Value: phase-2-todo-api  (your space name)
```

#### Secret 3: HF_TOKEN
```
Name: HF_TOKEN
Value: hf_xxxxxxxxxxxxxxxxxxxxx  (token from Step 2)
```

### Step 4: Configure Hugging Face Space Environment Variables

1. Go to your Space: `https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME`
2. Click **Settings** tab
3. Scroll to **"Repository secrets"**
4. Add these secrets:

```
DATABASE_URL
Value: postgresql://user:pass@host:port/db?sslmode=require
(Your Neon connection string)

AUTH_SECRET_KEY
Value: 76lYYDv3HxxlE19Gf3u5SMN8Las00JcM
(Or generate a new secure key)

DEBUG
Value: false
```

### Step 5: Trigger Deployment

#### Option A: Automatic (on push to main)
```bash
cd /mnt/e/Hackathon-2/phase-2
git add .
git commit -m "Setup GitHub Actions deployment"
git push origin main
```

#### Option B: Manual Trigger
1. Go to GitHub repository
2. Click **Actions** tab
3. Select **"Deploy to Hugging Face Spaces"** workflow
4. Click **"Run workflow"** → **"Run workflow"**

### Step 6: Monitor Deployment

1. Go to **Actions** tab in GitHub
2. Click on the running workflow
3. Watch the deployment progress
4. Check for success message with Space URL

## Workflow Behavior

- **Triggers on**:
  - Push to `main` branch (only if `phase-2/` files change)
  - Manual trigger via Actions tab

- **What it does**:
  1. Checks out code
  2. Prepares deployment files
  3. Pushes to Hugging Face Space
  4. Shows deployment summary

- **Build time**: 2-5 minutes on Hugging Face

## Testing After Deployment

```bash
# Replace with your actual values
HF_USERNAME="hunaizaasif"
SPACE_NAME="phase-2-todo-api"
SPACE_URL="https://${HF_USERNAME}-${SPACE_NAME}.hf.space"

# Health check
curl ${SPACE_URL}/health

# API documentation
echo "Visit: ${SPACE_URL}/docs"

# Register user
curl -X POST ${SPACE_URL}/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123","full_name":"Test User"}'
```

## Troubleshooting

### Workflow Fails with "Authentication failed"
- Check if HF_TOKEN is correct and has **Write** access
- Regenerate token if needed

### Workflow Fails with "Space not found"
- Verify HF_USERNAME and HF_SPACE_NAME secrets match exactly
- Ensure Space exists on Hugging Face

### Space Build Fails
- Check Space logs: Go to Space → **Logs** tab
- Common issues:
  - Missing DATABASE_URL in Space secrets
  - Invalid Dockerfile syntax
  - Missing files (src/, alembic/)

### Database Connection Error
- Verify DATABASE_URL in Space secrets
- Ensure `?sslmode=require` is added
- Check Neon database is active

### Port Issues
- Hugging Face requires port 7860
- Dockerfile already configured correctly

## Important Notes

1. **First deployment**: Takes 3-5 minutes to build
2. **Subsequent deployments**: Faster due to caching
3. **Space sleep**: Free tier spaces sleep after 48h inactivity
4. **Logs**: Always check Space logs for runtime errors

## Security Best Practices

- ✅ Never commit `.env` file
- ✅ Use GitHub Secrets for sensitive data
- ✅ Use Hugging Face Secrets for runtime config
- ✅ Rotate tokens periodically
- ✅ Use Write-only tokens (not Admin)

## Next Steps After Successful Deployment

1. Test all API endpoints
2. Monitor Space logs for errors
3. Set up monitoring/alerting (optional)
4. Share Space URL with team
5. Consider upgrading to paid tier for production

## Support Links

- GitHub Actions Docs: https://docs.github.com/en/actions
- Hugging Face Spaces: https://huggingface.co/docs/hub/spaces
- Neon PostgreSQL: https://neon.tech/docs
