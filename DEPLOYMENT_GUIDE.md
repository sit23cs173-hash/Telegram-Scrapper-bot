# 🚀 Deploy DealFinder to Render.com (FREE)

## Overview
This guide will help you deploy your DealFinder project online for FREE using Render.com. The deployment includes:
- **Web Service**: Frontend website + API (always accessible)
- **Background Worker**: Telegram bot that scrapes deals 24/7

---

## 📋 Prerequisites

1. **GitHub Account** - To host your code
2. **Render.com Account** - Sign up at https://render.com (free)
3. **Supabase Account** - Your database (already set up)
4. **Telegram API Credentials** - Your existing credentials

---

## 🔧 Step 1: Prepare Your Repository

### 1.0 **IMPORTANT: Create Telegram Session File**

⚠️ **You MUST do this before deploying to Render!**

Render doesn't have an interactive terminal, so you need to create the session file locally first:

```bash
python create_session_for_render.py
```

**What happens during this step:**
1. ✅ Script connects to Telegram
2. 📱 Telegram sends an **OTP code to your phone**
3. ⌨️ **You enter the OTP code** in the terminal
4. 🔐 Script creates and saves the authenticated session
5. 📋 Script shows you a **long base64 string**

**IMPORTANT Notes:**
- ⚠️ Have your phone ready to receive the OTP
- ⭐ OTP is **ONLY needed during this one-time setup**
- ✅ Once the session is uploaded to Render, **no OTP will ever be needed again**
- 🔒 The session remains valid indefinitely
- 💾 Save the base64 string safely - you'll paste it into Render

**Copy the entire base64 string** - you'll add it to Render as an environment variable.

### 1.1 Create a GitHub Repository

1. Go to https://github.com/new
2. Create a new repository named `dealfinder-app`
3. Don't initialize with README (we'll push existing code)

### 1.2 Push Your Code to GitHub

Open terminal in your project folder and run:

```bash
git init
git add .
git commit -m "Initial commit - DealFinder app"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/dealfinder-app.git
git push -u origin main
```

**Note**: Create a `.gitignore` file first to exclude sensitive data:
```
.env
*.session
*.session-journal
__pycache__/
*.pyc
.vscode/
```

---

## 🌐 Step 2: Deploy to Render.com

### 2.1 Sign Up & Connect GitHub

1. Go to https://render.com and sign up (use GitHub login)
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub account
4. Select your `dealfinder-app` repository

### 2.2 Configure Environment Variables

Render will automatically detect `render.yaml` and create 2 services:

#### For Web Service (dealfinder-website):
- `SUPABASE_URL` → Your Supabase project URL
- `SUPABASE_KEY` → Your Supabase anon key
- `PORT` → 10000 (auto-set)

#### For Worker Service (telegram-scraper-bot):
- `TELEGRAM_API_ID` → Your Telegram API ID
- `TELEGRAM_API_HASH` → Your Telegram API hash
- `TELEGRAM_PHONE` → Your phone number (with country code)
- `TELEGRAM_SESSION` → **The base64 string from create_session_for_render.py** ⚠️ REQUIRED!
- `SUPABASE_URL` → Your Supabase project URL
- `SUPABASE_KEY` → Your Supabase anon key
- `OPENAI_API_KEY` → (Optional) Your OpenAI API key

### 2.3 Deploy

1. Click **"Apply"** to deploy both services
2. Wait 5-10 minutes for build and deployment
3. You'll get a URL like: `https://dealfinder-website.onrender.com`

---

## 🎯 Step 3: Access Your Website

Once deployed:

✅ **Website URL**: `https://dealfinder-website.onrender.com`
- Accessible to anyone, anywhere
- Shows all deals from your database
- Real-time filtering and search

✅ **Backend Bot**: Runs 24/7 in the background
- Automatically scrapes deals from Telegram
- Saves to your Supabase database
- No manual intervention needed

---

## ⚙️ Important Notes

### Free Tier Limitations:
- **Web Service**: May sleep after 15 minutes of inactivity (wakes up automatically)
- **Worker Service**: Runs continuously (24/7)
- 750 hours/month free (enough for 24/7 operation)

### Keep Web Service Active:
Add this to your Telegram bot session file upload, or use a free uptime monitor:
- https://uptimerobot.com (free)
- Ping your website every 5 minutes: `https://dealfinder-website.onrender.com/health`
Solution ✅:
We've solved the session persistence issue! Steps:
1. Run `python create_session_for_render.py` locally (BEFORE deploying)
2. Copy the base64 session string it generates
3. Add it to Render as `TELEGRAM_SESSION` environment variable
4. The bot will automatically load it on startup - no re-authentication needed!s code modification)
3. **Use persistent disk** (paid feature)

---

## 🔒 Security Tips

1. **Never commit** `.env` or `.session` files to GitHub
2. **Use environment variables** for all sensitive data
3. **Rotate credentials** regularly
4. **Enable 2FA** on all accounts

---

## 🐛 Troubleshooting

### Build Fails:
- Check `requirements.txt` is up to date
- Verify Python version (3.11.0)

### Bot Not Working:
- Check environment variables are set correctly
- View logs in Render dashboard
- Ensure Telegram session is authenticated

### Website Shows No Deals:
- Verify Supabase credentials
- Check database has data
- View browser console for API errors

---

## 📊 Monitoring

### View Logs:
1. Go to Render Dashboard
2. Click on service name
3. Go to "Logs" tab
4. Real-time logs will appear

### Check Health:
- Visit: `https://dealfinder-website.onrender.com/health`
- Should return: `{"status": "healthy"}`

---

## 🎉 Success!

Your DealFinder is now live and accessible worldwide! 

**Share your website**: `https://dealfinder-website.onrender.com`

The bot will continuously scrape deals, and users can browse them on your website in real-time! 🚀
