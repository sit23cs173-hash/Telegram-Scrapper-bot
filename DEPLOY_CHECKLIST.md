# 🚀 Quick Deployment Checklist

## Before You Deploy to Render:

### ✅ Step 1: Create Session File (CRITICAL!)
```bash
python create_session_for_render.py
```

**What will happen:**
1. Script starts and asks you to press Enter
2. Telegram will send an OTP code to your phone
3. **Enter the OTP code** when prompted
4. Script generates a long base64 string
5. **Copy and save this string** - you'll need it for Render

⚠️ **IMPORTANT:**
- You need your phone with you (to receive OTP)
- OTP is **ONLY needed once** during this step
- After uploading the session to Render, **no OTP will ever be needed again**
- The session is valid indefinitely

### ✅ Step 2: Commit Your Code to GitHub
```bash
# If not already initialized
git init
git branch -M main

# Add files
git add .
git commit -m "Initial commit - DealFinder"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/dealfinder-app.git

# Push
git push -u origin main
```

### ✅ Step 3: Deploy on Render
1. Go to https://render.com
2. Sign up/Login with GitHub
3. Click **New +** → **Blueprint**
4. Select your `dealfinder-app` repository
5. Render will detect `render.yaml` automatically

### ✅ Step 4: Set Environment Variables

#### For Web Service (dealfinder-website):
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
```

#### For Worker Service (telegram-scraper-bot):
```
TELEGRAM_API_ID=31528324
TELEGRAM_API_HASH=bb4e3ae5103442b0a30534d838e902da
TELEGRAM_PHONE=+919585579490
TELEGRAM_SESSION=<paste the long base64 string here>
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
```

### ✅ Step 5: Deploy!
- Click **Apply**
- Wait 5-10 minutes
- Your website will be live at: `https://dealfinder-website.onrender.com`

---

## 🎯 What Gets Deployed:

1. **Web Service** (dealfinder-website)
   - Frontend e-commerce website
   - API endpoints for deals
   - Accessible to everyone
   
2. **Worker Service** (telegram-scraper-bot)
   - Runs in background 24/7
   - Scrapes Telegram channels
   - Saves deals to database
   - No manual intervention needed

---

## 🐛 Troubleshooting:

### Bot Not Working?
1. Check logs in Render Dashboard
2. Verify `TELEGRAM_SESSION` was added correctly
3. Make sure all environment variables are set

### Website Shows No Deals?
1. Check if bot is running (view worker logs)
2. Verify Supabase credentials
3. Check if database has data

### Need Help?
- See full guide: `DEPLOYMENT_GUIDE.md`
- Check logs in Render Dashboard
- Verify all environment variables

---

## 📊 After Deployment:

✅ Website: `https://dealfinder-website.onrender.com`
✅ Bot: Running 24/7 in background
✅ Database: Supabase (already configured)
✅ Free hosting: Yes!

**Share your website with friends and start getting those deals! 🎉**
