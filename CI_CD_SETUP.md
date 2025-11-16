# CI/CD Pipeline Setup Guide

This guide will walk you through setting up the complete CI/CD pipeline for your ML Model API.

## 📋 Prerequisites Checklist

- [x] Local project is working (✅ You've confirmed this)
- [ ] GitHub account
- [ ] Railway account (for deployment)
- [ ] Git installed locally

---

## 🚀 Step-by-Step Setup

### Step 1: Initialize Git Repository

```bash
# Make sure you're in the project directory
cd /home/cartrabbit/Documents/project/ML-CI-CD-Pipeline

# Initialize git (if not already done)
git init

# Add all files
git add .

# Make initial commit
git commit -m "Initial commit: ML Model API with CI/CD pipeline"
```

### Step 2: Create GitHub Repository

1. **Go to GitHub**: https://github.com/new
2. **Create a new repository**:
   - Repository name: `ML-CI-CD-Pipeline` (or your preferred name)
   - Description: "ML Model API with Full CI/CD Pipeline"
   - Visibility: Public or Private (your choice)
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
3. **Click "Create repository"**

### Step 3: Connect Local Repository to GitHub

```bash
# Add GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/ML-CI-CD-Pipeline.git

# Or if using SSH:
# git remote add origin git@github.com:YOUR_USERNAME/ML-CI-CD-Pipeline.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 4: Verify CI Pipeline (Automatic)

Once you push to GitHub, the CI pipeline will run automatically!

1. **Go to your GitHub repository**
2. **Click on "Actions" tab**
3. **You should see the CI workflow running**

The CI pipeline will:
- ✅ Install Python 3.10
- ✅ Install dependencies
- ✅ Run linting (flake8)
- ✅ Run format check (black)
- ✅ Train the model
- ✅ Run all tests (pytest)
- ✅ Upload model artifact

**Note:** The first run might take a few minutes. You can watch it in real-time!

### Step 5: Set Up Railway Deployment

You have **3 options** for Railway deployment. Choose the one that works best for you:

---

## 🚂 Railway Deployment Options

### Option A: Auto-Deploy from GitHub (Easiest - Recommended)

This is the simplest method - Railway automatically deploys when you push to GitHub.

#### Steps:

1. **Create Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub (recommended) or email

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Authorize Railway to access your GitHub account
   - Select your `ML-CI-CD-Pipeline` repository

3. **Configure Deployment**
   - Railway will automatically detect your `Dockerfile`
   - It will build and deploy automatically
   - Wait for the build to complete (usually 2-5 minutes)

4. **Get Your Public URL**
   - Once deployed, Railway will provide a public URL
   - Click on your service → Settings → Generate Domain
   - Your API will be available at: `https://your-app-name.railway.app`

5. **Test Your Deployed API**
   ```bash
   curl -X POST "https://your-app-name.railway.app/predict" \
        -H "Content-Type: application/json" \
        -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
   ```

**✅ That's it!** Every push to `main` branch will automatically trigger a new deployment.

---

### Option B: GitHub Actions Deployment (More Control)

This uses the provided GitHub Actions workflow for deployment.

#### Steps:

1. **Get Railway Token**
   - Go to Railway Dashboard → Account Settings → Tokens
   - Click "New Token"
   - Give it a name (e.g., "GitHub Actions")
   - Copy the token (you'll only see it once!)

2. **Get Railway Service ID**
   - First, deploy your app using Option A (one-time setup)
   - In Railway dashboard, click on your service
   - The Service ID is in the URL: `https://railway.app/project/PROJECT_ID/service/SERVICE_ID`
   - Or go to Settings → General → Service ID

3. **Add GitHub Secrets**
   - Go to your GitHub repository
   - Click "Settings" → "Secrets and variables" → "Actions"
   - Click "New repository secret"
   - Add two secrets:
     - **Name:** `RAILWAY_TOKEN` → **Value:** (paste your Railway token)
     - **Name:** `RAILWAY_SERVICE_ID` → **Value:** (paste your Service ID)

4. **Push to Main Branch**
   ```bash
   # Make any small change to trigger deployment
   echo "# Deployment test" >> README.md
   git add README.md
   git commit -m "Trigger deployment"
   git push origin main
   ```

5. **Monitor Deployment**
   - Go to GitHub → Actions tab
   - You'll see "CD Pipeline - Deploy to Railway" workflow running
   - Once complete, your app will be deployed

---

### Option C: Railway CLI (Manual Deployment)

For manual deployments using command line.

#### Steps:

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**
   ```bash
   railway login
   ```

3. **Initialize Project**
   ```bash
   cd /home/cartrabbit/Documents/project/ML-CI-CD-Pipeline
   railway init
   ```

4. **Deploy**
   ```bash
   railway up
   ```

---

## 🔄 CI/CD Workflow Overview

### What Happens on Each Push:

1. **CI Pipeline Runs** (on every push/PR):
   ```
   Push to GitHub
   ↓
   GitHub Actions triggers CI workflow
   ↓
   Install dependencies
   ↓
   Run linting & formatting checks
   ↓
   Train model
   ↓
   Run tests
   ↓
   Upload model artifact
   ↓
   ✅ CI passes
   ```

2. **CD Pipeline Runs** (on push to `main` branch):
   ```
   Push to main branch
   ↓
   GitHub Actions triggers CD workflow
   ↓
   Train model
   ↓
   Build Docker image
   ↓
   Deploy to Railway
   ↓
   ✅ App is live!
   ```

---

## 🧪 Testing Your CI/CD Pipeline

### Test CI Pipeline:

1. **Make a small change**:
   ```bash
   echo "# Test CI" >> README.md
   git add README.md
   git commit -m "Test CI pipeline"
   git push origin main
   ```

2. **Check GitHub Actions**:
   - Go to your repo → Actions tab
   - Watch the CI workflow run
   - Verify all steps pass ✅

### Test CD Pipeline:

1. **Make a code change**:
   ```bash
   # Edit app/main.py or any file
   git add .
   git commit -m "Update API"
   git push origin main
   ```

2. **Monitor Deployment**:
   - Check GitHub Actions for CD workflow
   - Check Railway dashboard for new deployment
   - Test your live API endpoint

---

## 📊 Monitoring & Logs

### GitHub Actions Logs:
- Go to: `https://github.com/YOUR_USERNAME/ML-CI-CD-Pipeline/actions`
- Click on any workflow run to see detailed logs

### Railway Logs:
- Go to Railway Dashboard
- Click on your service
- Click "Logs" tab to see real-time logs

### Test Your Deployed API:
```bash
# Health check
curl https://your-app.railway.app/health

# Make prediction
curl -X POST "https://your-app.railway.app/predict" \
     -H "Content-Type: application/json" \
     -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

---

## 🔧 Troubleshooting

### CI Pipeline Fails:

1. **Check GitHub Actions logs** for specific errors
2. **Common issues**:
   - Linting errors → Fix code style
   - Test failures → Fix tests
   - Model training fails → Check train.py

### CD Pipeline Fails:

1. **Check Railway token** is correct in GitHub Secrets
2. **Check Service ID** is correct
3. **Verify Dockerfile** is in root directory
4. **Check Railway logs** for build errors

### Deployment Issues:

1. **Model not found error**:
   - The Dockerfile trains the model during build
   - Check Railway build logs to see if training succeeded

2. **Port issues**:
   - Railway automatically handles ports
   - Make sure Dockerfile exposes port 8000

---

## ✅ Success Checklist

- [ ] Code pushed to GitHub
- [ ] CI pipeline runs successfully
- [ ] All tests pass
- [ ] Railway account created
- [ ] App deployed to Railway
- [ ] Public URL working
- [ ] API responds to requests
- [ ] CD pipeline triggers on push to main

---

## 🎉 You're Done!

Your ML Model API now has a complete CI/CD pipeline:
- ✅ Automated testing on every push
- ✅ Automated deployment to production
- ✅ Model training in CI
- ✅ Full observability with logs

**Next Steps:**
- Make changes to your code
- Push to GitHub
- Watch it automatically deploy! 🚀

