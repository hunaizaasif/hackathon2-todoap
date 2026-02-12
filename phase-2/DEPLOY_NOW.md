# 🚀 Quick Deployment Steps

## Abhi karna hai (5 minutes):

### 1. Hugging Face Space banao
```
https://huggingface.co/spaces
→ "Create new Space"
→ SDK: Docker (IMPORTANT!)
→ Name: phase-2-todo-api
```

### 2. HF Token banao
```
https://huggingface.co/settings/tokens
→ "New token"
→ Type: Write
→ Copy token
```

### 3. GitHub Secrets add karo
```
https://github.com/hunaizaasif/hackathon2-todoap/settings/secrets/actions
→ Add 3 secrets:

HF_USERNAME = hunaizaasif
HF_SPACE_NAME = phase-2-todo-api
HF_TOKEN = hf_xxxxx (token from step 2)
```

### 4. HF Space mein environment variables
```
Your Space → Settings → Repository secrets:

DATABASE_URL = postgresql://...?sslmode=require
AUTH_SECRET_KEY = 76lYYDv3HxxlE19Gf3u5SMN8Las00JcM
DEBUG = false
```

### 5. Deploy karo (jab network theek ho)
```bash
cd /mnt/e/Hackathon-2/phase-2
git add .
git commit -m "Setup HF deployment"
git push origin main
```

## Result:
- GitHub Actions automatically deploy karega
- Hugging Face par build hoga (2-5 min)
- API live ho jayegi: https://hunaizaasif-phase-2-todo-api.hf.space

## Local Docker ki zaroorat nahi!
GitHub Actions sab handle karega ✓
