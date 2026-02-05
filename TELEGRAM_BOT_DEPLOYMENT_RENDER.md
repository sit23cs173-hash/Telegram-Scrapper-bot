# Deploy Telegram Listener Bot to Render (No OTP Required)

## ✅ Step-by-Step Deployment Guide

### 1. Go to Render Dashboard
Visit: https://dashboard.render.com/

### 2. Select Your Worker Service
- Find and click on **`telegram-scraper-bot`** (Worker service)
- If it doesn't exist, create one:
  - Click **"New +"** → **"Background Worker"**
  - Connect to repository: `sit23cs173-hash/Telegram-Scrapper-bot`
  - Name: `telegram-scraper-bot`
  - Build Command: `pip install -r requirements.txt`
  - Start Command: `python telegram_listener.py`

### 3. Add Environment Variables

Go to **Environment** tab and add these variables:

#### Required Variables:

| Variable Name | Variable Value |
|---------------|----------------|
| `TELEGRAM_API_ID` | `31528324` |
| `TELEGRAM_API_HASH` | `bb4e3ae5103442b0a30534d838e902da` |
| `TELEGRAM_SESSION` | *(Copy from TELEGRAM_SESSION_ENCODED.txt file)* |
| `SUPABASE_URL` | `https://sspufleiikzsazouzkot.supabase.co` |
| `SUPABASE_KEY` | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNzcHVmbGVpaWt6c2F6b3V6a290Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU1MjkzNTEsImV4cCI6MjA4MTEwNTM1MX0.Uzh8O4Tn6buf2mhcA4w1JQeCZA-dcpzhm7AovwL4c4E` |

#### Optional Variables (Recommended):

| Variable Name | Variable Value |
|---------------|----------------|
| `OPENAI_API_KEY` | *(Your OpenAI API key for AI verification)* |

### 4. Save and Deploy

1. Click **"Save Changes"**
2. Render will automatically redeploy
3. Wait for deployment to complete (usually 2-5 minutes)

### 5. Verify Deployment

Check the **Logs** tab. You should see:

```
🔍 Initializing Supabase...
   URL: https://sspufleiikzsazouzkot.supabase.co
   KEY: eyJhbGciOiJIUzI1NiIsInR5...
✅ Connected to Supabase
✅ Loaded session from environment variable
✅ Successfully logged in as: [Your Name]
👂 Listening to X channels...
```

## 🎯 How It Works

1. **Session File**: You already authenticated locally and created a session file
2. **Base64 Encoding**: The session was encoded to base64 (see `TELEGRAM_SESSION_ENCODED.txt`)
3. **Environment Variable**: Render loads the session from `TELEGRAM_SESSION` variable
4. **Auto-Login**: Bot uses the session file and skips OTP authentication
5. **Background Worker**: Bot runs 24/7 listening to Telegram channels

## ⚠️ Important Notes

- **No OTP Required**: The session file handles authentication automatically
- **Session Validity**: The session is valid indefinitely (unless you logout or change password)
- **Security**: Never share your `TELEGRAM_SESSION` value publicly
- **Free Tier**: Render free tier may spin down after 15 minutes of inactivity
- **Upgrade**: For 24/7 operation without downtime, upgrade to paid plan ($7/month)

## 🔧 Troubleshooting

### Bot Not Starting
- Check logs for error messages
- Verify all environment variables are set correctly
- Ensure `TELEGRAM_SESSION` is complete (no truncation)

### "Session expired" Error
- Re-run `python create_session_for_render.py` locally
- Update `TELEGRAM_SESSION` variable with new value

### Database Connection Errors
- Verify SUPABASE_URL and SUPABASE_KEY are correct
- Check Supabase project is active

## 🔄 Updating the Bot

To update after making code changes:

```powershell
git add .
git commit -m "Update telegram bot"
git push
```

Render will automatically redeploy with the latest code!

## 📊 Monitor Your Bot

- **Logs**: View real-time logs in Render dashboard
- **Metrics**: Monitor CPU/memory usage
- **Alerts**: Set up email notifications for failures

---

## ✅ Summary

Your Telegram bot is now deployed and will:
- ✅ Listen to all configured Telegram channels
- ✅ Parse discount messages with NLP
- ✅ Verify deals by scraping official websites
- ✅ Store verified deals in Supabase database
- ✅ Handle images and extract text using OCR
- ✅ Run 24/7 (with free tier limitations)

**No manual OTP authentication needed!** 🎉
