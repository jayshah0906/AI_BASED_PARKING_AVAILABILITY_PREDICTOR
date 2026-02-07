# 🔧 Frontend Environment Variable Fix

## Problem
Frontend can't connect to backend because `VITE_API_URL` is not set correctly in Render.

---

## Quick Fix (3 minutes)

### Step 1: Get Your Backend URL

1. Go to Render dashboard: https://dashboard.render.com
2. Click on your **BACKEND** service
3. Copy the URL at the top (e.g., `https://parking-backend-xyz.onrender.com`)

### Step 2: Set Frontend Environment Variable

1. In Render dashboard, click on your **FRONTEND** service
2. Click **"Environment"** tab (left sidebar)
3. Click **"Add Environment Variable"**
4. Add:
   ```
   Key: VITE_API_URL
   Value: https://YOUR-BACKEND-URL.onrender.com/api/v1
   ```
   
   **⚠️ IMPORTANT:** 
   - Replace `YOUR-BACKEND-URL` with your actual backend URL
   - Don't forget `/api/v1` at the end!

5. Click **"Save Changes"**

### Step 3: Wait for Redeploy

- Render will automatically redeploy your frontend (2-3 minutes)
- Watch for "Your site is live 🎉"

### Step 4: Test

1. Clear browser cache: `Ctrl+Shift+R` (or `Cmd+Shift+R` on Mac)
2. Go to your frontend URL
3. Try signup again
4. Should work! ✅

---

## Example

If your backend URL is:
```
https://parking-backend-abc123.onrender.com
```

Then your `VITE_API_URL` should be:
```
https://parking-backend-abc123.onrender.com/api/v1
```

---

## Verify It's Working

### Check in Browser Console (F12)

1. Open your frontend in browser
2. Press F12 to open Developer Tools
3. Go to "Console" tab
4. Type:
   ```javascript
   console.log(import.meta.env.VITE_API_URL)
   ```
5. Should show your backend URL

### Check Network Tab

1. In Developer Tools, go to "Network" tab
2. Try to signup
3. Look for request to `/api/v1/auth/register`
4. Check the URL - should point to your backend

---

## Common Mistakes

### ❌ Wrong: Missing /api/v1
```
VITE_API_URL = https://parking-backend-xyz.onrender.com
```

### ✅ Correct: With /api/v1
```
VITE_API_URL = https://parking-backend-xyz.onrender.com/api/v1
```

### ❌ Wrong: Using frontend URL
```
VITE_API_URL = https://parking-frontend-xyz.onrender.com/api/v1
```

### ✅ Correct: Using backend URL
```
VITE_API_URL = https://parking-backend-xyz.onrender.com/api/v1
```

---

## Still Not Working?

### Check These:

1. **Backend is running**
   ```bash
   curl https://YOUR-BACKEND.onrender.com/api/v1/health
   ```
   Should return: `{"status":"healthy",...}`

2. **CORS is configured**
   - Backend should have your frontend URL in CORS_ORIGINS
   - Already fixed in previous step ✅

3. **Environment variable is set**
   - Go to Render → Frontend → Environment
   - Verify `VITE_API_URL` is there
   - Check the value is correct

4. **Frontend redeployed**
   - After adding env variable, frontend must redeploy
   - Check deployment status in Render

5. **Browser cache cleared**
   - Old cached version might not have new env variable
   - Hard refresh: `Ctrl+Shift+R`

---

## Debug Steps

### 1. Test Backend Directly

```bash
# Health check
curl https://YOUR-BACKEND.onrender.com/api/v1/health

# Test registration
curl -X POST https://YOUR-BACKEND.onrender.com/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "password123",
    "full_name": "Test User"
  }'
```

### 2. Check Browser Console

Open F12 and look for:
- CORS errors → Backend CORS not configured
- 404 errors → Wrong URL
- Network errors → Backend not running
- Timeout → Backend sleeping (wait 60 seconds)

### 3. Check Render Logs

1. Go to Render dashboard
2. Click on backend service
3. Click "Logs" tab
4. Look for errors when you try to signup

---

## Complete Checklist

- [ ] Backend URL copied from Render dashboard
- [ ] VITE_API_URL set in frontend environment variables
- [ ] Value includes `/api/v1` at the end
- [ ] Frontend redeployed after adding variable
- [ ] Backend is live and responding
- [ ] CORS includes frontend URL
- [ ] Browser cache cleared
- [ ] Tested signup again

---

## What Should Happen

1. **Frontend loads** → Shows landing page
2. **Click signup** → Opens signup form
3. **Fill form** → Enter details
4. **Submit** → Sends request to backend
5. **Backend processes** → Creates user in MongoDB
6. **Returns token** → Frontend receives response
7. **Redirects** → Goes to dashboard
8. **Success!** ✅

---

## Need More Help?

Share these details:
1. **Frontend URL:** `https://_____.onrender.com`
2. **Backend URL:** `https://_____.onrender.com`
3. **VITE_API_URL value:** (from Render environment)
4. **Browser console error:** (screenshot or copy)
5. **Backend logs:** (from Render dashboard)

And I'll help you debug!
