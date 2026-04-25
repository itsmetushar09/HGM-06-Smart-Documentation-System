# Deployment Guide for Smart Documentation System

## Overview

This guide provides step-by-step instructions for deploying the Smart Documentation System to Render (free tier).

## Prerequisites

Before deploying, ensure you have:

1. **GitHub OAuth Application**
   - Go to GitHub Settings → Developer settings → OAuth Apps
   - Create a new OAuth App
   - Note your Client ID and Client Secret

2. **MongoDB Atlas Account**
   - Create a free cluster
   - Create a database user and get connection string

3. **Qdrant Cloud Account** (or self-hosted Qdrant)
   - Get your API key and instance URL

4. **API Keys**
   - Hugging Face API token
   - Groq API key

5. **Render Account**
   - Sign up at render.com with GitHub

## Step 1: Prepare GitHub Repository

1. Push your project to GitHub
2. Ensure `.env` and `.env.example` files are in the repository root

## Step 2: Update GitHub OAuth App

1. Go to your GitHub OAuth App settings
2. Update "Authorization callback URL":
   ```
   https://your-render-backend-url.onrender.com/auth/github/callback
   ```
3. Update "Homepage URL":
   ```
   https://your-render-frontend-url.onrender.com
   ```

## Step 3: Deploy Backend on Render

### Option A: Manual Setup (Recommended)

1. **Log in to Render**
   - Go to render.com and sign in with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Select your GitHub repository
   - Choose branch (usually main)

3. **Configure Service**
   - **Name**: `smartdocs-backend`
   - **Runtime**: Python 3
   - **Build Command**: 
     ```
     cd backend && pip install -r requirements.txt
     ```
   - **Start Command**: 
     ```
     cd backend && gunicorn -w 2 -b 0.0.0.0:$PORT app:app
     ```
   - **Plan**: Free tier

4. **Add Environment Variables**
   Click "Advanced" and add:
   
   ```
   FLASK_ENV=production
   FLASK_SECRET_KEY=<generate-a-random-secret-key>
   GITHUB_CLIENT_ID=<your-client-id>
   GITHUB_CLIENT_SECRET=<your-client-secret>
   MONGO_URI=<your-mongodb-atlas-uri>
   QDRANT_URL=https://<your-qdrant-instance>.qdrant.io
   QDRANT_API_KEY=<your-qdrant-api-key>
   HF_TOKEN=<your-hugging-face-token>
   GROQ_API_KEY=<your-groq-api-key>
   FRONTEND_URL=https://your-render-frontend-url.onrender.com
   CORS_ORIGINS=https://your-render-frontend-url.onrender.com
   PORT=10000
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete

### Option B: Using render.yaml

1. Render will automatically detect `render.yaml` in your repository
2. Follow the same environment variables setup as Option A

## Step 4: Deploy Frontend on Render

1. **Create Static Site**
   - Click "New +" → "Static Site"
   - Select your GitHub repository
   - Choose branch (usually main)

2. **Configure**
   - **Name**: `smartdocs-frontend`
   - **Build Command**: 
     ```
     cd frontend && npm install && npm run build
     ```
   - **Publish Directory**: `frontend/dist`

3. **Add Environment Variables**
   ```
   VITE_API_BASE=https://your-render-backend-url.onrender.com
   ```

4. **Deploy**
   - Click "Create Static Site"
   - Wait for deployment to complete

## Step 5: Update OAuth Callback URL

After frontend is deployed:

1. Update your GitHub OAuth App
2. Set "Authorization callback URL":
   ```
   https://your-render-backend-url.onrender.com/auth/github/callback
   ```

## Monitoring and Troubleshooting

### Common Issues

#### OAuth Not Working
- ✓ Verify `FRONTEND_URL` matches your deployed frontend URL
- ✓ Verify `CORS_ORIGINS` matches your deployed frontend URL
- ✓ Check GitHub OAuth app callback URL configuration
- ✓ Verify `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET`

#### Repositories Not Loading
- ✓ Check MongoDB connection: `mongosh <connection-string>`
- ✓ Verify GitHub token has `repo` scope
- ✓ Check GitHub API rate limits (60 requests/hour for unauthenticated)

#### AI Responses Not Working
- ✓ Verify Qdrant instance is running and accessible
- ✓ Test Hugging Face token: fetch embeddings
- ✓ Test Groq API key: make a test request
- ✓ Ensure repository has been loaded and embeddings created

#### Build Failing
- ✓ Check Node version in frontend: `npm --version`
- ✓ Verify Python version in backend (3.9+)
- ✓ Check build logs in Render dashboard

### Checking Logs

1. **Backend Logs**
   - Go to Render dashboard → Select backend service
   - Click "Logs" tab
   - Check for errors

2. **Frontend Logs**
   - Go to Render dashboard → Select frontend site
   - Click "Logs" tab
   - Check for build/deployment errors

## Performance Optimization Tips

1. **Gunicorn Workers**: Currently set to 2
   - For free tier, 2 workers is optimal
   - More workers = higher memory usage

2. **Vector Database**: Use Qdrant Cloud for better performance
   - Self-hosted Qdrant may timeout on Render

3. **MongoDB Atlas**: Use the free tier
   - Keep data indexed properly

4. **Request Timeouts**: Set to 30 seconds for API calls
   - Increase if getting timeout errors

## Updating Code

1. **Push changes to GitHub**
   ```bash
   git add .
   git commit -m "Your message"
   git push
   ```

2. **Trigger Render deployment**
   - Render auto-deploys on push if auto-deploy is enabled
   - Or manually trigger from Render dashboard

## Environment Variables Summary

### Backend Required Variables
| Variable | Description | Example |
|----------|-------------|---------|
| `FLASK_ENV` | Environment mode | `production` |
| `FLASK_SECRET_KEY` | Flask secret key | Random string |
| `GITHUB_CLIENT_ID` | OAuth Client ID | From GitHub |
| `GITHUB_CLIENT_SECRET` | OAuth secret | From GitHub |
| `MONGO_URI` | MongoDB connection | `mongodb+srv://...` |
| `QDRANT_URL` | Qdrant instance URL | `https://...qdrant.io` |
| `QDRANT_API_KEY` | Qdrant API key | From Qdrant |
| `HF_TOKEN` | Hugging Face token | From HF |
| `GROQ_API_KEY` | Groq API key | From Groq |
| `FRONTEND_URL` | Deployed frontend URL | `https://...onrender.com` |
| `CORS_ORIGINS` | Allowed CORS origins | Frontend URL |
| `PORT` | Server port | `10000` |

### Frontend Environment Variables
| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_BASE` | Backend API base URL | `https://...onrender.com` |

## Next Steps

1. Monitor the deployed app for 24-48 hours
2. Test all features:
   - GitHub OAuth login
   - Repository selection
   - Document loading
   - AI question answering
3. Set up error monitoring (optional)
4. Configure custom domain (optional)

## Support

For issues:
1. Check Render logs
2. Review error messages
3. Verify environment variables
4. Check GitHub OAuth app configuration
5. Test API endpoints manually using curl or Postman

## Security Checklist

- ✓ `FLASK_SECRET_KEY` is randomized
- ✓ `SESSION_COOKIE_SECURE=True` in production
- ✓ `SESSION_COOKIE_HTTPONLY=True`
- ✓ CORS origins restricted to deployed frontend
- ✓ GitHub secrets not committed to repository
- ✓ `.env` file is in `.gitignore`

## Production Checklist

- ✓ Gunicorn configured for production
- ✓ Flask debug mode disabled
- ✓ All API keys set in environment variables
- ✓ Database indices created for performance
- ✓ Error logging configured
- ✓ Timeouts configured for external APIs
- ✓ Retry logic for API calls
- ✓ Rate limiting considered

## Costs

**Render Free Tier**: 
- 1 free instance (backend or frontend)
- 1 free static site (frontend or backend)
- Total: Deploy backend + frontend, both free!

**External Services** (paid, free tier available):
- MongoDB Atlas: Free tier included
- Qdrant Cloud: Free tier included
- Hugging Face: Free API tokens available
- Groq: Free tier with credits

**Estimated Monthly Cost**: $0 (if using free tiers)

---

**Last Updated**: April 2026
