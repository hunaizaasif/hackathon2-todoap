# Phase 3 Quick Deployment Checklist

## 🎯 Overview

Phase 3 has **2 components** to deploy:
1. **MCP Server** → Hugging Face Spaces (Docker)
2. **Frontend** → Vercel (Next.js)

---

## ✅ Pre-Deployment Checklist

### Prerequisites (5 minutes)

- [ ] Phase 2 API already deployed on Hugging Face
- [ ] Hugging Face account with Write token
- [ ] Vercel account (free)
- [ ] OpenAI API key (or OpenRouter key)
- [ ] GitHub repository access

---

## 🔧 Part 1: MCP Server (Hugging Face)

### Step 1: Create HF Space (2 min)
```
1. https://huggingface.co/spaces → "Create new Space"
2. Name: phase-3-mcp-server
3. SDK: Docker ⚠️ IMPORTANT!
4. Hardware: CPU basic (free)
```

### Step 2: Add GitHub Secret (1 min)
```
GitHub Repo → Settings → Secrets → Actions
Add: HF_MCP_SPACE_NAME = phase-3-mcp-server
```

### Step 3: Configure HF Space Secrets (1 min)
```
HF Space → Settings → Repository secrets:

PHASE2_API_URL = https://YOUR_USERNAME-phase-2-todo-api.hf.space
PORT = 7860
```

### Step 4: Deploy (1 command)
```bash
cd /mnt/e/Hackathon-2
git add phase-3/mcp-server
git commit -m "Deploy MCP Server"
git push origin main
```

### Step 5: Verify (30 sec)
```bash
curl https://YOUR_USERNAME-phase-3-mcp-server.hf.space/health
```

Expected: `{"status":"healthy","tools":5}`

---

## 🎨 Part 2: Frontend (Vercel)

### Step 1: Connect GitHub to Vercel (2 min)
```
1. https://vercel.com → Sign in with GitHub
2. "Add New Project"
3. Import: hunaizaasif/hackathon2-todoap
4. Root Directory: phase-3/frontend
5. Framework: Next.js (auto-detected)
```

### Step 2: Configure Environment Variables (2 min)
```
Vercel Project → Settings → Environment Variables:

NEXT_PUBLIC_PHASE2_API_URL = https://YOUR_USERNAME-phase-2-todo-api.hf.space
MCP_SERVER_URL = https://YOUR_USERNAME-phase-3-mcp-server.hf.space
OPENAI_API_KEY = sk-proj-xxxxx (or OpenRouter key)
OPENAI_BASE_URL = https://openrouter.ai/api/v1
```

### Step 3: Deploy (1 click)
```
Click "Deploy" button in Vercel
Wait 2-3 minutes for build
```

### Step 4: Verify (30 sec)
```
Open: https://your-app.vercel.app
Should see: Login/Register page
```

---

## 🧪 Testing Complete System

### Test 1: Backend Health
```bash
curl https://YOUR_USERNAME-phase-2-todo-api.hf.space/health
# Expected: {"status":"healthy",...}
```

### Test 2: MCP Server Health
```bash
curl https://YOUR_USERNAME-phase-3-mcp-server.hf.space/health
# Expected: {"status":"healthy","tools":5}
```

### Test 3: Frontend
```
1. Open: https://your-app.vercel.app
2. Register new account
3. Login
4. Try AI chat: "Add a task: Test deployment"
5. Check if task appears in dashboard
```

---

## 📋 Deployment Status Tracker

### Phase 2 (Backend)
- [ ] Hugging Face Space created
- [ ] Environment variables configured
- [ ] Deployed via GitHub Actions
- [ ] Health check passing
- [ ] Database connected

### Phase 3 - MCP Server
- [ ] Hugging Face Space created
- [ ] GitHub secret added (HF_MCP_SPACE_NAME)
- [ ] Environment variables configured
- [ ] Deployed via GitHub Actions
- [ ] Health check passing
- [ ] Can connect to Phase 2 API

### Phase 3 - Frontend
- [ ] Vercel project created
- [ ] Environment variables configured
- [ ] Deployed successfully
- [ ] Can access login page
- [ ] Can register/login
- [ ] AI chat working
- [ ] Tasks CRUD working

---

## 🚨 Common Issues & Quick Fixes

### Issue: MCP Server build fails
**Fix**: Check Dockerfile, verify src/ directory exists

### Issue: Frontend can't connect to MCP Server
**Fix**: Verify MCP_SERVER_URL in Vercel env vars

### Issue: AI chat not working
**Fix**: Check OPENAI_API_KEY is valid and has credits

### Issue: CORS errors
**Fix**: Check Phase 2 API CORS settings allow your Vercel domain

### Issue: Database connection error
**Fix**: Verify DATABASE_URL in Phase 2 HF Space secrets

---

## 📊 Deployment URLs Reference

After deployment, save these URLs:

```
Phase 2 API:
https://YOUR_USERNAME-phase-2-todo-api.hf.space

MCP Server:
https://YOUR_USERNAME-phase-3-mcp-server.hf.space

Frontend:
https://your-app.vercel.app
```

---

## 💰 Cost Summary

| Service | Cost | Notes |
|---------|------|-------|
| Hugging Face (Phase 2) | Free | May sleep after 48h |
| Hugging Face (MCP) | Free | May sleep after 48h |
| Vercel | Free | 100GB bandwidth/month |
| Neon PostgreSQL | Free | 3GB storage |
| OpenAI API | ~$5-10/mo | Pay per use |

**Total**: ~$5-10/month (only OpenAI)

---

## ⏱️ Total Deployment Time

- Phase 2: ~10 minutes
- MCP Server: ~5 minutes
- Frontend: ~5 minutes
- Testing: ~5 minutes

**Total**: ~25 minutes (excluding build times)

---

## 🎉 Success Criteria

Your deployment is successful when:

✅ All 3 services are running
✅ Health checks pass
✅ Can register/login on frontend
✅ Can create tasks via UI
✅ Can create tasks via AI chat
✅ Tasks persist in database

---

## 📚 Additional Resources

- [Full Deployment Guide](./DEPLOYMENT_GUIDE.md)
- [Phase 2 Deployment](../../phase-2/DEPLOY_NOW.md)
- [Vercel Docs](https://vercel.com/docs)
- [Hugging Face Docs](https://huggingface.co/docs/hub/spaces)
