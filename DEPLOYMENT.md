# Complete Deployment Guide - Hackathon Todo App

This repository contains a 3-phase Todo application with AI capabilities. This guide covers deployment of all phases.

## 📋 Project Overview

### Phase 1: CLI Todo App
- **Status**: Local only (no deployment needed)
- **Tech**: Python 3.13, UV package manager
- **Storage**: In-memory

### Phase 2: Web API + Persistence
- **Deployment**: Hugging Face Spaces (Docker)
- **Tech**: FastAPI, SQLModel, PostgreSQL
- **Database**: Neon Serverless PostgreSQL

### Phase 3: AI Agent + Frontend
- **MCP Server**: Hugging Face Spaces (Docker)
- **Frontend**: Vercel (Next.js)
- **Tech**: Next.js 15, OpenAI, MCP SDK

---

## 🚀 Quick Start (30 minutes total)

### Prerequisites
- [ ] GitHub account
- [ ] Hugging Face account + Write token
- [ ] Vercel account (free)
- [ ] Neon PostgreSQL database (free)
- [ ] OpenAI API key (or OpenRouter)

---

## 📦 Phase 2: Backend API Deployment

### Time: ~10 minutes

#### Step 1: Create Neon Database (2 min)
```
1. Go to https://neon.tech
2. Create new project
3. Copy connection string
```

#### Step 2: Create Hugging Face Space (2 min)
```
1. https://huggingface.co/spaces
2. Create Space: phase-2-todo-api
3. SDK: Docker
4. Hardware: CPU basic (free)
```

#### Step 3: Configure HF Space Secrets (1 min)
```
Space Settings → Repository secrets:

DATABASE_URL = postgresql://user:pass@host/db?sslmode=require
AUTH_SECRET_KEY = 76lYYDv3HxxlE19Gf3u5SMN8Las00JcM
DEBUG = false
```

#### Step 4: Setup GitHub Secrets (2 min)
```
GitHub Repo → Settings → Secrets → Actions

HF_USERNAME = your_hf_username
HF_SPACE_NAME = phase-2-todo-api
HF_TOKEN = hf_xxxxx (Write token)
```

#### Step 5: Deploy (1 command)
```bash
git add .
git commit -m "Deploy Phase 2 to Hugging Face"
git push origin main
```

GitHub Actions will automatically deploy!

#### Step 6: Verify
```bash
curl https://YOUR_USERNAME-phase-2-todo-api.hf.space/health
```

**Detailed Guide**: [phase-2/DEPLOY_NOW.md](phase-2/DEPLOY_NOW.md)

---

## 🔧 Phase 3: MCP Server Deployment

### Time: ~5 minutes

#### Step 1: Create HF Space (2 min)
```
1. https://huggingface.co/spaces
2. Create Space: phase-3-mcp-server
3. SDK: Docker
4. Hardware: CPU basic (free)
```

#### Step 2: Configure HF Space Secrets (1 min)
```
Space Settings → Repository secrets:

PHASE2_API_URL = https://YOUR_USERNAME-phase-2-todo-api.hf.space
PORT = 7860
```

#### Step 3: Add GitHub Secret (1 min)
```
GitHub Repo → Settings → Secrets → Actions

HF_MCP_SPACE_NAME = phase-3-mcp-server
```

#### Step 4: Deploy (1 command)
```bash
git add .
git commit -m "Deploy MCP Server"
git push origin main
```

#### Step 5: Verify
```bash
curl https://YOUR_USERNAME-phase-3-mcp-server.hf.space/health
```

**Detailed Guide**: [phase-3/QUICK_DEPLOY.md](phase-3/QUICK_DEPLOY.md)

---

## 🎨 Phase 3: Frontend Deployment (Vercel)

### Time: ~5 minutes

#### Step 1: Connect to Vercel (2 min)
```
1. https://vercel.com
2. Sign in with GitHub
3. Import repository
4. Root Directory: phase-3/frontend
5. Framework: Next.js (auto-detected)
```

#### Step 2: Configure Environment Variables (2 min)
```
Vercel Project → Settings → Environment Variables:

NEXT_PUBLIC_PHASE2_API_URL =  https://vercel.com/dashboard
MCP_SERVER_URL = https://YOUR_USERNAME-phase-3-mcp-server.hf.space
OPENAI_API_KEY = sk-proj-xxxxx
OPENAI_BASE_URL = https://openrouter.ai/api/v1
```

#### Step 3: Deploy (1 click)
Click "Deploy" in Vercel dashboard

#### Step 4: Verify
Open your Vercel URL and test login/registration

**Detailed Guide**: [phase-3/DEPLOYMENT_GUIDE.md](phase-3/DEPLOYMENT_GUIDE.md)

---

## 🧪 Testing Complete System

### 1. Test Backend
```bash
curl https://YOUR_USERNAME-phase-2-todo-api.hf.space/health
# Expected: {"status":"healthy",...}
```

### 2. Test MCP Server
```bash
curl https://YOUR_USERNAME-phase-3-mcp-server.hf.space/health
# Expected: {"status":"healthy","tools":5}
```

### 3. Test Frontend
```
1. Open: https://your-app.vercel.app
2. Register account
3. Login
4. Create task via UI
5. Try AI chat: "Add a task: Test deployment"
```

---

## 📊 Architecture Diagram

```
┌─────────────────────────────────────────────┐
│  Frontend (Vercel)                          │
│  https://your-app.vercel.app                │
│  - Next.js 15                               │
│  - AI Chat Interface                        │
│  - Task Dashboard                           │
└──────────────┬──────────────────────────────┘
               │
               ├─────────────────┐
               │                 │
               ▼                 ▼
┌──────────────────────┐  ┌─────────────────────┐
│  MCP Server (HF)     │  │  Phase 2 API (HF)   │
│  Port 7860           │  │  Port 7860          │
│  - MCP Tools         │  │  - FastAPI          │
│  - Task Operations   │  │  - Authentication   │
└──────────────────────┘  └──────────┬──────────┘
                                     │
                                     ▼
                          ┌─────────────────────┐
                          │  Neon PostgreSQL    │
                          │  - User data        │
                          │  - Tasks            │
                          └─────────────────────┘
```

---

## 💰 Cost Breakdown

| Service | Free Tier | Paid Option |
|---------|-----------|-------------|
| Hugging Face (Phase 2) | ✅ CPU basic | $0.60/hour (GPU) |
| Hugging Face (MCP) | ✅ CPU basic | $0.60/hour (GPU) |
| Vercel | ✅ 100GB/mo | $20/mo (Pro) |
| Neon PostgreSQL | ✅ 3GB storage | $19/mo (Scale) |
| OpenAI API | ❌ Pay-per-use | ~$5-10/mo |

**Total Free Tier**: ~$5-10/month (only OpenAI API)

---

## 🔧 GitHub Actions Workflows

This repository includes automated deployment workflows:

### 1. Phase 2 Backend Deployment
- **File**: `.github/workflows/deploy-phase2-backend.yml`
- **Triggers**: Push to `main` (when `phase-2/` changes)
- **Deploys to**: Hugging Face Spaces

### 2. MCP Server Deployment
- **File**: `.github/workflows/deploy-mcp-server.yml`
- **Triggers**: Push to `main` (when `phase-3/mcp-server/` changes)
- **Deploys to**: Hugging Face Spaces

### Manual Trigger
You can also manually trigger workflows:
```
GitHub → Actions → Select workflow → Run workflow
```

---

## 🚨 Troubleshooting

### Phase 2 Issues

**Build fails:**
- Check Dockerfile syntax
- Verify all files present (src/, alembic/)
- Check GitHub Actions logs

**Database connection error:**
- Verify DATABASE_URL format
- Ensure `?sslmode=require` is added
- Check Neon database is active

### Phase 3 MCP Server Issues

**Cannot connect to Phase 2:**
- Verify PHASE2_API_URL is correct
- Check Phase 2 is running
- Test Phase 2 health endpoint

### Phase 3 Frontend Issues

**Build fails on Vercel:**
- Check build logs
- Verify all dependencies
- Check TypeScript errors

**AI chat not working:**
- Verify OPENAI_API_KEY
- Check API credits
- Test MCP Server connection

---

## 📚 Detailed Documentation

### Phase 2
- [Quick Start](phase-2/DEPLOY_NOW.md)
- [GitHub Actions Setup](phase-2/GITHUB_ACTIONS_SETUP.md)
- [Full Deployment Guide](phase-2/DEPLOYMENT.md)

### Phase 3
- [Quick Deploy Checklist](phase-3/QUICK_DEPLOY.md)
- [Complete Deployment Guide](phase-3/DEPLOYMENT_GUIDE.md)
- [Main README](phase-3/README.md)

---

## ✅ Deployment Checklist

### Phase 2 Backend
- [ ] Neon database created
- [ ] HF Space created (phase-2-todo-api)
- [ ] HF Space secrets configured
- [ ] GitHub secrets configured
- [ ] Deployed via GitHub Actions
- [ ] Health check passing

### Phase 3 MCP Server
- [ ] HF Space created (phase-3-mcp-server)
- [ ] HF Space secrets configured
- [ ] GitHub secret added (HF_MCP_SPACE_NAME)
- [ ] Deployed via GitHub Actions
- [ ] Health check passing

### Phase 3 Frontend
- [ ] Vercel project created
- [ ] Environment variables configured
- [ ] Deployed successfully
- [ ] Login/registration working
- [ ] AI chat working
- [ ] Tasks CRUD working

---

## 🎉 Success Criteria

Your deployment is complete when:

✅ Phase 2 API health check passes
✅ MCP Server health check passes
✅ Frontend loads successfully
✅ Can register/login
✅ Can create tasks via UI
✅ Can create tasks via AI chat
✅ Tasks persist in database

---

## 🔗 Important Links

- **GitHub Repository**: https://github.com/hunaizaasif/hackathon2-todoap
- **Hugging Face Spaces**: https://huggingface.co/spaces
- **Vercel Dashboard**: https://vercel.com/dashboard
- **Neon Console**: https://console.neon.tech

---

## 📞 Support

For issues or questions:
1. Check troubleshooting sections in detailed guides
2. Review GitHub Actions logs
3. Check Hugging Face Space logs
4. Review Vercel deployment logs

---

## 🚀 Next Steps After Deployment

1. Test all functionality
2. Share app with users
3. Monitor usage and errors
4. Consider upgrading to paid tiers for production
5. Add custom domains
6. Set up monitoring (Sentry, LogRocket)
7. Implement rate limiting
8. Add analytics

---

**Last Updated**: 2026-02-12
**Repository**: https://github.com/hunaizaasif/hackathon2-todoap
