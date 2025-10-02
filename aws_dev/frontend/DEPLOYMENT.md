# 🚀 Frontend Deployment Guide

This guide explains how to deploy the Next.js frontend to AWS S3.

## 📋 Prerequisites

### 1. AWS CLI Setup
```bash
# Install AWS CLI (if not installed)
brew install awscli

# Configure AWS credentials
aws configure
# Enter your:
# - AWS Access Key ID
# - AWS Secret Access Key  
# - Default region: us-east-2
# - Default output format: json
```

### 2. Node.js Setup
```bash
# Make sure Node.js is installed
node --version
npm --version

# If using nvm (recommended)
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm use node
```

## 🎯 Quick Start

### One-Time Setup
```bash
# 1. Navigate to frontend directory
cd /Users/dennis/Desktop/Project\ Blankey/project_blankey/aws_dev/frontend

# 2. Run deployment script (it will handle everything)
./deploy.sh
```

### Update Frontend (Every Time You Make Changes)
```bash
# Navigate to frontend directory
cd /Users/dennis/Desktop/Project\ Blankey/project_blankey/aws_dev/frontend

# Run the script again
./deploy.sh
```

## 📁 S3 Structure

After deployment, your S3 bucket will look like:
```
project-blankey/
├── frontend/           ← Your frontend files
│   ├── index.html
│   ├── _next/
│   │   ├── static/
│   │   └── ...
│   └── ...
└── chat_data/          ← Your Lambda data
    └── ...
```

## 🌐 Access Your Frontend

Your deployed frontend will be available at:
```
https://project-blankey.s3-website-us-east-2.amazonaws.com/frontend/
```

## 🔧 What the Script Does

1. **Checks Prerequisites** - AWS CLI, Node.js, S3 bucket access
2. **Installs Dependencies** - Runs `npm install` if needed
3. **Builds Frontend** - Runs `npm run build` for static export
4. **Deploys to S3** - Syncs files to `s3://project-blankey/frontend/`
5. **Sets Cache Headers** - Optimizes performance
6. **Configures Website** - Enables static website hosting
7. **Sets Permissions** - Makes files publicly readable

## 🛠️ Manual Commands (If Script Fails)

```bash
# Build frontend
npm run build

# Deploy to S3
aws s3 sync out/ s3://project-blankey/frontend/ --delete

# Set cache headers
aws s3 cp s3://project-blankey/frontend/ s3://project-blankey/frontend/ \
    --recursive --metadata-directive REPLACE --cache-control "max-age=31536000"

# Enable static website hosting
aws s3 website s3://project-blankey \
    --index-document "frontend/index.html" \
    --error-document "frontend/404.html"
```

## 🔍 Troubleshooting

### Error: "Bucket does not exist"
```bash
# Create the bucket first
aws s3 mb s3://project-blankey --region us-east-2
```

### Error: "Access Denied"
```bash
# Check your AWS credentials
aws sts get-caller-identity

# Make sure you have S3 permissions
aws s3 ls s3://project-blankey
```

### Error: "Build failed"
```bash
# Check if next.config.js exists and is configured for static export
# Make sure all dependencies are installed
npm install
```

### Error: "Command not found: aws"
```bash
# Install AWS CLI
brew install awscli
aws configure
```

## 📝 Notes

- **First deployment** may take 2-3 minutes
- **Subsequent deployments** are faster (only changed files)
- **Cache headers** are set for optimal performance
- **HTTPS** requires CloudFront (not included in this script)
- **Custom domain** requires additional DNS configuration

## 🎉 Success!

Once deployed, your frontend will be live and connected to your Lambda API!
