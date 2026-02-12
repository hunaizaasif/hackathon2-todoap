# Hugging Face Spaces Deployment Guide

## Prerequisites

1. Hugging Face account (https://huggingface.co/join)
2. Neon PostgreSQL database (https://neon.tech) - Free tier available
3. Git installed locally

## Step 1: Create Neon Database

1. Go to https://neon.tech and sign up
2. Create a new project
3. Copy the connection string (format: `postgresql://user:password@host/database`)
4. Keep this connection string safe - you'll need it for environment variables

## Step 2: Create Hugging Face Space

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Fill in details:
   - **Space name**: `phase-2-todo-api` (or your choice)
   - **License**: MIT
   - **SDK**: Docker
   - **Space hardware**: CPU basic (free tier)
4. Click "Create Space"

## Step 3: Configure Environment Variables

In your Hugging Face Space settings, add these secrets:

```bash
DATABASE_URL=postgresql://user:password@host:port/database?sslmode=require
AUTH_SECRET_KEY=76lYYDv3HxxlE19Gf3u5SMN8Las00JcM
DEBUG=false
CORS_ORIGINS=["*"]
```

**Important**: Replace `DATABASE_URL` with your actual Neon connection string!

## Step 4: Push Code to Hugging Face

### Option A: Using Git (Recommended)

```bash
# Navigate to phase-2 directory
cd /mnt/e/Hackathon-2/phase-2

# Add Hugging Face remote
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME

# Create deployment branch
git checkout -b hf-deploy

# Copy HF README
cp README_HF.md README.md

# Commit and push
git add .
git commit -m "Deploy to Hugging Face Spaces"
git push hf hf-deploy:main
```

### Option B: Using Hugging Face Web Interface

1. Go to your Space's "Files" tab
2. Upload these files:
   - `Dockerfile`
   - `README_HF.md` (rename to `README.md`)
   - `main.py`
   - `pyproject.toml`
   - `uv.lock`
   - `alembic.ini`
   - `src/` folder (all files)
   - `alembic/` folder (all files)

## Step 5: Run Database Migrations

After deployment, you need to run migrations. You have two options:

### Option A: Local Migration (Before Deployment)

```bash
# Set your Neon DATABASE_URL
export DATABASE_URL="postgresql://user:password@host:port/database?sslmode=require"

# Run migrations
uv run alembic upgrade head
```

### Option B: Add Migration to Dockerfile

Update the CMD in Dockerfile to run migrations on startup:

```dockerfile
CMD ["sh", "-c", "uv run alembic upgrade head && uv run uvicorn main:app --host 0.0.0.0 --port 7860"]
```

## Step 6: Verify Deployment

1. Wait for Space to build (2-5 minutes)
2. Visit your Space URL: `https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME`
3. Check endpoints:
   - `/health` - Should return healthy status
   - `/docs` - Interactive API documentation
   - `/` - API information

## Testing the API

```bash
# Health check
curl https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space/health

# Register user
curl -X POST https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123","full_name":"Test User"}'

# Login
curl -X POST https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123"}'
```

## Troubleshooting

### Build Fails
- Check Dockerfile syntax
- Verify all files are uploaded
- Check Space logs in "Logs" tab

### Database Connection Error
- Verify DATABASE_URL is correct
- Ensure Neon database is active
- Check if `?sslmode=require` is added to connection string

### Port Issues
- Hugging Face Spaces requires port 7860
- Verify Dockerfile EXPOSE and CMD use port 7860

### Migration Errors
- Run migrations manually using Option A above
- Check Alembic configuration in `alembic.ini`

## Important Notes

1. **Free Tier Limitations**:
   - CPU basic (free) may be slow for heavy traffic
   - Space sleeps after 48h of inactivity
   - Consider upgrading for production use

2. **Security**:
   - Never commit `.env` file
   - Use Hugging Face Secrets for sensitive data
   - Change AUTH_SECRET_KEY to a secure random string

3. **Database**:
   - Neon free tier has limits (3GB storage, 1 project)
   - Database persists even if Space restarts
   - Backup your database regularly

## Next Steps

- Set up custom domain (HF Pro feature)
- Add monitoring and logging
- Configure auto-scaling (HF Pro feature)
- Add rate limiting for production use
