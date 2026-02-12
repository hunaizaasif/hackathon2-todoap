# Quick Deployment Checklist

## ✅ Pre-Deployment (Complete these first)

### 1. Create Neon Database
- [ ] Go to https://neon.tech
- [ ] Sign up / Login
- [ ] Create new project
- [ ] Copy connection string (looks like: `postgresql://user:pass@host/db`)
- [ ] Save it securely

### 2. Create Hugging Face Space
- [ ] Go to https://huggingface.co/spaces
- [ ] Click "Create new Space"
- [ ] Name: `phase-2-todo-api` (or your choice)
- [ ] SDK: **Docker**
- [ ] License: MIT
- [ ] Click "Create Space"

### 3. Configure Environment Variables
In your HF Space settings → "Settings" → "Repository secrets":

```
DATABASE_URL = postgresql://user:pass@host:port/db?sslmode=require
AUTH_SECRET_KEY = 76lYYDv3HxxlE19Gf3u5SMN8Las00JcM
DEBUG = false
```

## 🚀 Deployment Options

### Option 1: Automated Script (Recommended)

```bash
cd /mnt/e/Hackathon-2/phase-2
./deploy-to-hf.sh YOUR_HF_USERNAME YOUR_SPACE_NAME
```

Example:
```bash
./deploy-to-hf.sh hunaizaasif phase-2-todo-api
```

### Option 2: Manual Git Push

```bash
cd /mnt/e/Hackathon-2/phase-2

# Add HF remote
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME

# Create branch
git checkout -b hf-deploy

# Copy README
cp README_HF.md README.md

# Commit
git add .
git commit -m "Deploy to Hugging Face Spaces"

# Push
git push hf hf-deploy:main
```

### Option 3: Web Upload (If Git Issues)

1. Go to your Space → "Files" tab
2. Click "Add file" → "Upload files"
3. Upload these files:
   - `Dockerfile`
   - `README_HF.md` (rename to `README.md`)
   - `main.py`
   - `pyproject.toml`
   - `uv.lock`
   - `alembic.ini`
4. Upload folders:
   - `src/` (all files inside)
   - `alembic/` (all files inside)

## 🧪 Testing After Deployment

```bash
# Replace with your actual Space URL
SPACE_URL="https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space"

# Health check
curl $SPACE_URL/health

# API docs
# Visit: $SPACE_URL/docs

# Register user
curl -X POST $SPACE_URL/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123","full_name":"Test User"}'

# Login
curl -X POST $SPACE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'
```

## 📝 Important Notes

1. **Wait Time**: Space build takes 2-5 minutes
2. **First Request**: May be slow (cold start)
3. **Logs**: Check "Logs" tab in HF Space for errors
4. **Database**: Migrations run automatically on startup

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| Build fails | Check Dockerfile syntax, verify all files uploaded |
| Database error | Verify DATABASE_URL, add `?sslmode=require` |
| 502 Bad Gateway | Wait for build to complete, check logs |
| Port error | Ensure port 7860 in Dockerfile |

## 📞 Support

- Hugging Face Docs: https://huggingface.co/docs/hub/spaces
- Neon Docs: https://neon.tech/docs
- FastAPI Docs: https://fastapi.tiangolo.com
