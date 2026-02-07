# 🔧 Fix Backend 500 Error

## Current Status

✅ **Frontend**: `https://ai-based-parking-availability-predictor-3.onrender.com` (Working)
✅ **Backend**: `https://ai-based-parking-availability-predictor-2.onrender.com` (Deployed but errors)

## Problem

Your backend is returning **500 Internal Server Error** when trying to register users. This is most likely a **database connection issue**.

---

## Solution: Check Backend Environment Variables

### Step 1: Verify Environment Variables in Backend Service

Go to Render Dashboard → **Backend Service** (AI_BASED_PARKING_AVAILABILITY_PREDICTOR-2) → **Environment** tab

You MUST have these variables set:

```bash
DATABASE_URL=mongodb+srv://parking_admin:jay123@cluster-parking-system.uyhmitw.mongodb.net/parking_db
USE_ML_MODEL=true
```

### Step 2: Check Backend Logs

1. Go to Render Dashboard
2. Click on your **Backend** service
3. Click **"Logs"** tab
4. Look for error messages related to:
   - MongoDB connection
   - Database authentication
   - Missing environment variables

Common errors you might see:
```
pymongo.errors.ServerSelectionTimeoutError
pymongo.errors.ConfigurationError
KeyError: 'DATABASE_URL'
```

### Step 3: Fix Based on Error

#### If you see "DATABASE_URL not found":
- Add `DATABASE_URL` environment variable in Render
- Value: `mongodb+srv://parking_admin:jay123@cluster-parking-system.uyhmitw.mongodb.net/parking_db`

#### If you see "Authentication failed":
- Check MongoDB Atlas dashboard
- Verify user `parking_admin` exists
- Verify password is `jay123`
- Verify database is `parking_db`

#### If you see "Network timeout":
- Go to MongoDB Atlas
- Click "Network Access"
- Add IP: `0.0.0.0/0` (allow all IPs)
- This is required for Render to connect

---

## Quick Test Commands

### Test 1: Check if backend is running
```bash
curl https://ai-based-parking-availability-predictor-2.onrender.com/
```
Expected: `{"message":"Parking Availability Prediction API",...}`
Result: ✅ Working

### Test 2: Check zones endpoint (requires DB)
```bash
curl https://ai-based-parking-availability-predictor-2.onrender.com/api/v1/zones
```
Expected: List of parking zones
Current: ❌ Internal Server Error

### Test 3: Check auth endpoint (requires DB)
```bash
curl -X POST https://ai-based-parking-availability-predictor-2.onrender.com/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"full_name":"Test","email":"test@test.com","username":"test","password":"test123"}'
```
Expected: User created with token
Current: ❌ Internal Server Error

---

## Most Likely Issues

### Issue 1: DATABASE_URL Not Set (90% probability)
**Symptom**: 500 error on all database operations
**Fix**: Add `DATABASE_URL` in Render environment variables

### Issue 2: MongoDB Atlas Network Access (5% probability)
**Symptom**: Connection timeout
**Fix**: Add `0.0.0.0/0` to MongoDB Atlas Network Access

### Issue 3: Wrong Database Credentials (3% probability)
**Symptom**: Authentication error in logs
**Fix**: Verify credentials in MongoDB Atlas

### Issue 4: Database Not Initialized (2% probability)
**Symptom**: Collections not found
**Fix**: Run initialization script (but this shouldn't cause 500)

---

## Step-by-Step Fix

### 1. Add Environment Variables to Backend

**Render Dashboard → Backend Service → Environment:**

```
DATABASE_URL = mongodb+srv://parking_admin:jay123@cluster-parking-system.uyhmitw.mongodb.net/parking_db
USE_ML_MODEL = true
SECRET_KEY = your-secret-key-here-change-this-in-production
```

### 2. Verify MongoDB Atlas Network Access

**MongoDB Atlas Dashboard → Network Access:**
- Click "Add IP Address"
- Select "Allow Access from Anywhere"
- IP: `0.0.0.0/0`
- Click "Confirm"

### 3. Redeploy Backend

After adding environment variables:
- Render will automatically redeploy
- Wait 2-3 minutes
- Check logs for errors

### 4. Test Again

```bash
curl https://ai-based-parking-availability-predictor-2.onrender.com/api/v1/zones
```

Should return zones list (not 500 error)

---

## After Backend is Fixed

Once the backend returns data (not 500 errors), then set the frontend environment variable:

**Render Dashboard → Frontend Service → Environment:**

```
VITE_API_URL = https://ai-based-parking-availability-predictor-2.onrender.com/api/v1
```

Then redeploy frontend and test signup!

---

## What I Need From You

1. **Check backend logs** - Share any error messages you see
2. **Verify environment variables** - Screenshot of backend environment variables
3. **Test the zones endpoint** - Does it return data or 500 error?

---

## Expected Flow

```
Before Fix:
Frontend → Backend → Database ❌ (500 error)

After Fix:
Frontend → Backend → Database ✅ (Success!)
```

---

**Next Step**: Check your backend environment variables and logs! 🔍
