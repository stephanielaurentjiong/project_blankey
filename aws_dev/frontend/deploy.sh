#!/bin/bash

# =============================================================================
# AWS S3 Frontend Deployment Script
# =============================================================================
# 
# This script builds and deploys the Next.js frontend to AWS S3
# 
# Prerequisites:
# 1. AWS CLI installed and configured
# 2. Node.js and npm installed
# 3. Proper AWS permissions for S3 bucket access
#
# Usage:
#   ./deploy.sh
#
# What it does:
# 1. Builds the Next.js app for static export
# 2. Syncs the built files to S3 bucket
# 3. Sets proper cache headers
# 4. Provides the website URL
#
# =============================================================================

set -e  # Exit on any error

# Configuration
BUCKET_NAME="project-blankey-frontend"
S3_PREFIX=""
REGION="us-east-2"
WEBSITE_URL="https://${BUCKET_NAME}.s3-website-${REGION}.amazonaws.com/${S3_PREFIX}"

echo "🚀 Starting frontend deployment..."
echo "📦 Bucket: ${BUCKET_NAME}"
echo "📁 Prefix: ${S3_PREFIX}"
echo "🌍 Region: ${REGION}"
echo ""

# Step 1: Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI is not installed. Please install it first:"
    echo "   brew install awscli"
    echo "   aws configure"
    exit 1
fi

# Step 2: Check if bucket exists
echo "🔍 Checking if S3 bucket exists..."
if ! aws s3 ls "s3://${BUCKET_NAME}" 2>/dev/null; then
    echo "❌ Bucket '${BUCKET_NAME}' does not exist or you don't have access."
    echo "   Please create the bucket first:"
    echo "   aws s3 mb s3://${BUCKET_NAME} --region ${REGION}"
    exit 1
fi

# Step 3: Load nvm and check Node.js
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"

# Use node version
nvm use node &> /dev/null

if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install it first."
    echo "   Run: nvm install node && nvm use node"
    exit 1
fi

# Step 4: Navigate to caption-generator directory
cd caption-generator

# Step 5: Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Step 6: Build the frontend
echo "🔨 Building Next.js app for static export..."
npm run build

# Check if build was successful
if [ ! -d "out" ]; then
    echo "❌ Build failed - 'out' directory not found"
    echo "   Make sure your next.config.js is configured for static export"
    exit 1
fi

# Step 7: Deploy to S3
echo "📤 Deploying to S3..."
aws s3 sync out/ "s3://${BUCKET_NAME}/${S3_PREFIX}" --delete

# Step 8: Set cache headers for better performance
echo "⚡ Setting cache headers..."
aws s3 cp "s3://${BUCKET_NAME}/${S3_PREFIX}" "s3://${BUCKET_NAME}/${S3_PREFIX}" \
    --recursive \
    --metadata-directive REPLACE \
    --cache-control "max-age=31536000" \
    --exclude "*.html" \
    --exclude "*.json"

# Set shorter cache for HTML files
aws s3 cp "s3://${BUCKET_NAME}/${S3_PREFIX}" "s3://${BUCKET_NAME}/${S3_PREFIX}" \
    --recursive \
    --metadata-directive REPLACE \
    --cache-control "max-age=0" \
    --include "*.html" \
    --include "*.json"

# Step 9: Enable static website hosting (if not already enabled)
echo "🌐 Configuring static website hosting..."
aws s3 website "s3://${BUCKET_NAME}" \
    --index-document "index.html" \
    --error-document "404.html" 2>/dev/null || true

# Step 10: Set bucket policy for public read access
echo "🔓 Setting bucket policy for public access..."
cat > bucket-policy.json << EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::${BUCKET_NAME}/*"
        }
    ]
}
EOF

aws s3api put-bucket-policy --bucket "${BUCKET_NAME}" --policy file://bucket-policy.json
rm bucket-policy.json

echo ""
echo "✅ Deployment completed successfully!"
echo ""
echo "🌐 Your frontend is now available at:"
echo "   ${WEBSITE_URL}"
echo ""
echo "📊 Deployment Summary:"
echo "   • Bucket: ${BUCKET_NAME}"
echo "   • Prefix: ${S3_PREFIX}"
echo "   • Region: ${REGION}"
echo "   • Files: $(find out -type f | wc -l) files deployed"
echo ""
echo "💡 To update your frontend, just run this script again!"
echo "   ./deploy.sh"
