# ❓ Frequently Asked Questions - Deployment

## 🔐 Authentication & OTP

### Q: Do I need to enter OTP on Render?
**A: NO!** OTP is only needed **once** when you run `create_session_for_render.py` on your local computer.

### Q: When do I need to enter the OTP?
**A:** When you run this command on your local computer:
```bash
python create_session_for_render.py
```

The process:
1. You run the script
2. Telegram sends OTP to your phone
3. You enter the OTP in your terminal
4. Script creates a session file
5. You copy the base64 string
6. You paste it into Render

**After this, OTP is NEVER needed again!**

### Q: What if I don't have access to my phone?
**A:** You need your phone to receive the OTP during the initial setup. Make sure you have your phone with you when running `create_session_for_render.py`.

### Q: Will the session expire?
**A:** No! Telegram sessions remain valid indefinitely unless you:
- Manually logout
- Revoke the session from another device
- Delete your Telegram account

### Q: What if I redeploy on Render?
**A:** The session persists! As long as the `TELEGRAM_SESSION` environment variable is set, you won't need to re-authenticate.

---

## 🚀 Deployment

### Q: Can I deploy without creating the session file?
**A:** No. If you try to deploy without the session, the bot will fail because it can't authenticate without a terminal.

### Q: Where do I paste the session string?
**A:** In Render Dashboard:
1. Go to your Worker Service (telegram-scraper-bot)
2. Click "Environment" tab
3. Add variable: `TELEGRAM_SESSION`
4. Paste the long base64 string
5. Save

### Q: Is my session secure?
**A:** Yes, as long as:
- Don't commit it to GitHub
- Only store it in Render's environment variables
- Keep it private (don't share the base64 string)

---

## 🌐 Website & Backend

### Q: Will the website work immediately?
**A:** Yes! Once deployed, the website is accessible at `https://dealfinder-website.onrender.com`

### Q: How long does the bot run?
**A:** 24/7! The worker service on Render runs continuously.

### Q: What if there are no deals on the website?
**A:** Wait a few minutes for the bot to start scraping. Check:
1. Worker logs (is the bot running?)
2. Database (are deals being saved?)
3. Website API (refresh the page)

### Q: Can I use a custom domain?
**A:** Yes! Render supports custom domains (see their docs).

---

## 💰 Cost

### Q: Is Render really free?
**A:** Yes! The free tier includes:
- 750 hours/month (enough for 24/7)
- Both web service and worker
- No credit card required

### Q: What are the limitations?
**A:** Free tier:
- Web service sleeps after 15 mins inactivity (wakes up automatically)
- Worker runs continuously
- 512 MB RAM per service

---

## 🐛 Troubleshooting

### Q: Bot is not working on Render
**Check these:**
1. Is `TELEGRAM_SESSION` environment variable set?
2. Are all other environment variables correct?
3. Check the logs in Render Dashboard
4. Verify your Supabase credentials

### Q: Session invalid error
**A:** If you see "session invalid":
1. Run `create_session_for_render.py` again
2. Get a new base64 string
3. Update the `TELEGRAM_SESSION` variable in Render
4. Redeploy

### Q: Website shows 500 error
**A:** Check:
1. Supabase credentials are correct
2. Database tables exist
3. API logs in Render Dashboard

---

## 📱 Telegram Specific

### Q: Can I use a bot token instead of phone auth?
**A:** Not recommended for this use case. User accounts have better channel access than bots.

### Q: What if I change my phone number?
**A:** You'll need to:
1. Update `TELEGRAM_PHONE` variable
2. Run `create_session_for_render.py` again
3. Get new session string
4. Update `TELEGRAM_SESSION` in Render

### Q: Can multiple people use the same session?
**A:** No. Each Telegram account needs its own session.

---

## 🎯 Best Practices

### ✅ DO:
- Keep your session string private
- Use environment variables for all credentials
- Monitor your Render logs regularly
- Keep your phone number updated

### ❌ DON'T:
- Commit session files to GitHub
- Share your base64 session string
- Use the same session on multiple servers
- Logout from Telegram while bot is running

---

## 🆘 Still Need Help?

1. Check the full guide: `DEPLOYMENT_GUIDE.md`
2. Review logs in Render Dashboard
3. Verify all environment variables
4. Test locally first before deploying

**Remember: The hardest part is the first-time setup. After that, it just works! 🚀**
