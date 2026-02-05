#!/bin/bash
# Quick Deploy Script for DealFinder

echo "🚀 DealFinder Deployment Setup"
echo "=============================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    git branch -M main
else
    echo "✅ Git already initialized"
fi

# Check if .gitignore exists
if [ ! -f ".gitignore" ]; then
    echo "⚠️  Warning: .gitignore not found!"
    echo "   Create .gitignore before committing!"
else
    echo "✅ .gitignore exists"
fi

# Check if remote is set
if ! git remote get-url origin > /dev/null 2>&1; then
    echo ""
    echo "📝 Set up your GitHub repository:"
    echo "   1. Go to: https://github.com/new"
    echo "   2. Create repository: dealfinder-app"
    echo "   3. Run: git remote add origin https://github.com/YOUR_USERNAME/dealfinder-app.git"
else
    echo "✅ Git remote configured"
fi

echo ""
echo "📋 Next Steps:"
echo "   1. Review .gitignore file"
echo "   2. git add ."
echo "   3. git commit -m 'Initial commit'"
echo "   4. git push -u origin main"
echo "   5. Go to render.com and deploy"
echo ""
echo "📖 Full guide: See DEPLOYMENT_GUIDE.md"
