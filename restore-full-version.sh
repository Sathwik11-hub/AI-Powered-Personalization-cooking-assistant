#!/bin/bash

# Restore Full Version Script
# This script restores your original app files after Vercel deployment

echo "🔄 Restoring full version..."

if [ -f "requirements-full.txt.backup" ]; then
    mv requirements-full.txt.backup requirements.txt
    echo "✅ Restored requirements.txt"
else
    echo "❌ Backup not found: requirements-full.txt.backup"
fi

if [ -f "app-full.py.backup" ]; then
    mv app-full.py.backup app.py
    echo "✅ Restored app.py"
else
    echo "❌ Backup not found: app-full.py.backup"
fi

echo ""
echo "✅ Full version restored!"
echo "Your app is back to the original with all ML features."
