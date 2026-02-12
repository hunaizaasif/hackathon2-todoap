# Phase 3 Deployment Guide

Phase 3 has two components that need to be deployed separately:

1. **MCP Server** → Hugging Face Spaces (Docker)
2. **Frontend (Next.js)** → Vercel (Recommended)

---

## Part 1: MCP Server Deployment (Hugging Face)

### Step 1: Create Hugging Face Space for MCP Server

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Fill details:
   - **Space name**: `phase-3-mcp-server` (or your choice)
   - **License**: MIT
   - **SDK**: **Docker** (IMPORTANT!)
   - **Space hardware**: CPU basic (free)
4. Click "Create Space"

### Step 2: Configure MCP Server Environment Variables

In your HF Space settings → "Repository secrets":

```
PHASE2_API_URL = https://YOUR_USERNAME-phase-2-todo-api.hf.space
PORT = 7860
```

**Important**: Replace `YOUR_USERNAME` with your actual Hugging Face username!

### Step 3: Setup GitHub Secrets for MCP Server

Go to: `https://github.com/hunaizaasif/hackathon2-todoap/settings/secrets/actions`

Add this new secret:

```
HF_MCP_SPACE_NAME = phase-3-mcp-server
```

(HF_USERNAME and HF_TOKEN should already exist from Phase 2)

### Step 4: Deploy MCP Server

```bash
cd /mnt/e/Hackathon-2/phase-3/mcp-server
git add .
git commit -m "Deploy MCP Server to Hugging Face"
git push origin main
```

GitHub Actions will automatically deploy to Hugging Face!

### Step 5: Verify MCP Server

```bash
# Replace with your actual Space URL
MCP_URL="https://YOUR_USERNAME-phase-3-mcp-server.hf.space"

# Health check
curl $MCP_URL/health

# List tools
curl $MCP_URL/tools
```

---

## Part 2: Frontend Deployment (Vercel)

### Why Vercel?
- Next.js is built by Vercel
- Zero-config deployment
- Automatic HTTPS
- Edge functions support
- Better performance for Next.js apps

### Step 1: Install Vercel CLI (Optional)

```bash
npm install -g vercel
```

### Step 2: Deploy via Vercel Dashboard (Recommended)

1. Go to https://vercel.com
2. Sign in with GitHub
3. Click "Add New Project"
4. Import your repository: `hunaizaasif/hackathon2-todoap`
5. Configure project:
   - **Framework Preset**: Next.js
   - **Root Directory**: `phase-3/frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

### Step 3: Configure Frontend Environment Variables

In Vercel project settings → "Environment Variables":

```
NEXT_PUBLIC_PHASE2_API_URL = https://YOUR_USERNAME-phase-2-todo-api.hf.space
MCP_SERVER_URL = https://YOUR_USERNAME-phase-3-mcp-server.hf.space
OPENAI_API_KEY = sk-proj-xxxxx
OPENAI_BASE_URL = https://openrouter.ai/api/v1
```

**Important**:
- Get OpenAI API key from https://platform.openai.com/api-keys
- Or use OpenRouter: https://openrouter.ai/keys

### Step 4: Deploy

Click "Deploy" in Vercel dashboard. It will:
- Build your Next.js app
- Deploy to Vercel's edge network
- Provide a production URL

### Step 5: Verify Frontend

Visit your Vercel URL (e.g., `https://your-app.vercel.app`)

---

## Alternative: Deploy Frontend via CLI

```bash
cd /mnt/e/Hackathon-2/phase-3/frontend

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

---

## Complete Architecture After Deployment

```
┌────────────────────────────────────────────────┐
│                                                 │
│  Frontend (Vercel)                              │
│  https://your-app.vercel.app                    │
│                                                 │
└────────────┬────────────────────────────────────┘
             │
             ├──────────────────┐
             │                  │
             ▼                  ▼
┌────────────────────┐  ┌──────────────────────┐
│                    │  │                      │
│  MCP Server (HF)   │  │  Phase 2 API (HF)    │
│  Port 7860         │  │  Port 7860           │
│                    │  │                      │
└────────────────────┘  └──────────┬───────────┘
                                   │
                                   ▼
                        ┌──────────────────────┐
                        │                      │
                        │  Neon PostgreSQL     │
                        │  (Database)          │
                        │                      │
                        └──────────────────────┘
```

---

## Testing the Complete System

### 1. Test Phase 2 API
```bash
curl https://YOUR_USERNAME-phase-2-todo-api.hf.space/health
```

### 2. Test MCP Server
```bash
curl https://YOUR_USERNAME-phase-3-mcp-server.hf.space/health
```

### 3. Test Frontend
Open browser: `https://your-app.vercel.app`

### 4. Test AI Chat
1. Register/Login on frontend
2. Go to chat interface
3. Try: "Add a task: Buy groceries"
4. Try: "Show me all my tasks"

---

## Troubleshooting

### MCP Server Issues

**Build fails:**
- Check Dockerfile syntax
- Verify all files uploaded
- Check Space logs

**Cannot connect to Phase 2 API:**
- Verify PHASE2_API_URL is correct
- Check Phase 2 API is running
- Test Phase 2 API health endpoint

### Frontend Issues

**Build fails on Vercel:**
- Check build logs in Vercel dashboard
- Verify all dependencies in package.json
- Check TypeScript errors

**Cannot connect to MCP Server:**
- Verify MCP_SERVER_URL is correct
- Check MCP Server is running
- Test MCP Server health endpoint

**OpenAI API errors:**
- Verify OPENAI_API_KEY is set
- Check API key has credits
- Check rate limits

### CORS Issues

If you get CORS errors:
1. Check Phase 2 API CORS settings
2. Verify MCP Server CORS headers
3. Add your Vercel domain to allowed origins

---

## Cost Breakdown (Free Tier)

| Service | Free Tier | Limits |
|---------|-----------|--------|
| Hugging Face (Phase 2) | ✅ Free | CPU basic, sleeps after 48h |
| Hugging Face (MCP) | ✅ Free | CPU basic, sleeps after 48h |
| Vercel (Frontend) | ✅ Free | 100GB bandwidth/month |
| Neon PostgreSQL | ✅ Free | 3GB storage, 1 project |
| OpenAI API | 💰 Paid | $5 minimum |

**Total Monthly Cost**: ~$5-10 (only OpenAI API)

---

## Production Recommendations

1. **Upgrade Hugging Face Spaces** to prevent sleep
2. **Use custom domain** on Vercel
3. **Add monitoring** (Sentry, LogRocket)
4. **Set up CI/CD** for automated testing
5. **Add rate limiting** to prevent abuse
6. **Use environment-specific configs** (dev/staging/prod)

---

## Next Steps

1. ✅ Deploy Phase 2 API to Hugging Face
2. ✅ Deploy MCP Server to Hugging Face
3. ✅ Deploy Frontend to Vercel
4. 🔄 Test complete system
5. 🔄 Share with users
6. 🔄 Monitor and iterate
