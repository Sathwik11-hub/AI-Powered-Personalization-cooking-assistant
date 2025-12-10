#!/bin/bash

# Vercel Lite Deployment Script
# This script prepares your app for Vercel by using minimal dependencies

echo "🚀 Preparing for Vercel Lite Deployment..."
echo ""
echo "⚠️  WARNING: This will deploy a LIMITED version without ML features!"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "Deployment cancelled."
    exit 1
fi

echo "📦 Step 1: Backing up original files..."
cp requirements.txt requirements-full.txt.backup
cp app.py app-full.py.backup

echo "📝 Step 2: Switching to minimal requirements..."
cp requirements-minimal.txt requirements.txt

echo "🔧 Step 3: Switching to Vercel-compatible app..."
cp app_vercel_compatible.py app.py

echo "✅ Step 4: Files prepared!"
echo ""
echo "Now run: vercel --prod"
echo ""
echo "After deployment, restore original files with:"
echo "  ./restore-full-version.sh"
echo ""
