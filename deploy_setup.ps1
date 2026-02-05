# Quick Deploy Script for DealFinder (Windows)

Write-Host "🚀 DealFinder Deployment Setup" -ForegroundColor Cyan
Write-Host "==============================" -ForegroundColor Cyan
Write-Host ""

# Check if git is initialized
if (-not (Test-Path ".git")) {
    Write-Host "📦 Initializing git repository..." -ForegroundColor Yellow
    git init
    git branch -M main
} else {
    Write-Host "✅ Git already initialized" -ForegroundColor Green
}

# Check if .gitignore exists
if (-not (Test-Path ".gitignore")) {
    Write-Host "⚠️  Warning: .gitignore not found!" -ForegroundColor Red
    Write-Host "   Create .gitignore before committing!" -ForegroundColor Red
} else {
    Write-Host "✅ .gitignore exists" -ForegroundColor Green
}

# Check if remote is set
$remoteUrl = git remote get-url origin 2>$null
if (-not $remoteUrl) {
    Write-Host ""
    Write-Host "📝 Set up your GitHub repository:" -ForegroundColor Yellow
    Write-Host "   1. Go to: https://github.com/new" -ForegroundColor White
    Write-Host "   2. Create repository: dealfinder-app" -ForegroundColor White
    Write-Host "   3. Run: git remote add origin https://github.com/YOUR_USERNAME/dealfinder-app.git" -ForegroundColor White
} else {
    Write-Host "✅ Git remote configured: $remoteUrl" -ForegroundColor Green
}

Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor Cyan
Write-Host "   1. Review .gitignore file" -ForegroundColor White
Write-Host "   2. git add ." -ForegroundColor White
Write-Host "   3. git commit -m 'Initial commit'" -ForegroundColor White
Write-Host "   4. git push -u origin main" -ForegroundColor White
Write-Host "   5. Go to render.com and deploy" -ForegroundColor White
Write-Host ""
Write-Host "📖 Full guide: See DEPLOYMENT_GUIDE.md" -ForegroundColor Cyan
