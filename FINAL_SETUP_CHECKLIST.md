# ✅ Final Setup Checklist

## Your Services

- **Frontend**: `https://ai-based-parking-availability-predictor-3.onrender.com` ✅
- **Backend**: `https://ai-based-parking-availability-predictor-2.onrender.com` ⚠️ (500 errors)

---

## Step 1: Fix Backend (MUST DO FIRST)

### 1.1 Add Environment Variables to Backend Service

Go to: **Render Dashboard → Backend Service → Environment**

Add these variables:

```bash
DATABASE_URL=mongodb+srv://parking_admin:jay123@cluster-parking-system.uyhmitw.mongodb.net/parking_db
USE_ML_MODEL=true
SECRET_KEY=change-this-to-a-random-secret-key-in-production
```

- [ ] `DATABASE_URL` is set
- [ ] `USE_ML_MODEL` is set
- [ ] Backend redeployed automatically

### 1.2 Verify MongoDB Atlas Network Access

Go to: **MongoDB Atlas → Network Access**

- [ ] IP `0.0.0.0/0` is allowed (or Render's IPs)
- [ ] Network access is active

### 1.3 Test Backend

Run this command:
```bash
curl https://ai-based-parking-availability-predictor-2.onrender.com/api/v1/zones
```

- [ ] Returns list of zones (not "Internal Server Error")

---

## Step 2: Configure Frontend (AFTER Backend Works)

### 2.1 Add Environment Variable to Frontend Service

Go to: **Render Dashboard → Frontend Service → Environment**

Add this variable:

```bash
VITE_API_URL=https://ai-based-parking-availability-predictor-2.onrender.com/api/v1
```

- [ ] `VITE_API_URL` is set
- [ ] Frontend redeployed automatically

### 2.2 Test Frontend

1. Open: `https://ai-based-parking-availability-predictor-3.onrender.com`
2. Click "Sign Up"
3. Fill in the form
4. Click "Create Account"

- [ ] No "Failed to fetch" error
- [ ] User is created successfully
- [ ] Redirected to dashboard

---

## Step 3: Verify Everything Works

### 3.1 Test Signup
- [ ] Can create new user
- [ ] Receives access token
- [ ] Redirected to dashboard

### 3.2 Test Login
- [ ] Can login with created user
- [ ] Receives access token
- [ ] Redirected to dashboard

### 3.3 Test Predictions
- [ ] Can select a zone
- [ ] Can select a time
- [ ] Can get parking predictions
- [ ] Predictions show availability

---

## Common Issues

### Backend still returns 500 error
**Cause**: Environment variables not set or MongoDB not accessible
**Fix**: Check backend logs in Render dashboard

### Frontend still shows "Failed to fetch"
**Cause**: `VITE_API_URL` not set or backend is down
**Fix**: Verify environment variable and backend status

### CORS errors in browser console
**Cause**: Frontend URL not in backend CORS list
**Fix**: Already fixed in code, just redeploy backend

---

## Quick Reference

### Backend Environment Variables
```bash
DATABASE_URL=mongodb+srv://parking_admin:jay123@cluster-parking-system.uyhmitw.mongodb.net/parking_db
USE_ML_MODEL=true
SECRET_KEY=your-secret-key
```

### Frontend Environment Variables
```bash
VITE_API_URL=https://ai-based-parking-availability-predictor-2.onrender.com/api/v1
```

### Test Commands
```bash
# Test backend root
curl https://ai-based-parking-availability-predictor-2.onrender.com/

# Test backend zones (requires DB)
curl https://ai-based-parking-availability-predictor-2.onrender.com/api/v1/zones

# Test backend signup (requires DB)
curl -X POST https://ai-based-parking-availability-predictor-2.onrender.com/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"full_name":"Test","email":"test@test.com","username":"test","password":"test123"}'
```

---

## Priority Order

1. **FIRST**: Fix backend (add DATABASE_URL)
2. **SECOND**: Test backend (should return data, not 500)
3. **THIRD**: Configure frontend (add VITE_API_URL)
4. **FOURTH**: Test signup (should work!)

---

## Need Help?

Share:
1. Backend logs from Render dashboard
2. Screenshot of backend environment variables
3. Result of: `curl https://ai-based-parking-availability-predictor-2.onrender.com/api/v1/zones`

---

**Start with Step 1: Fix Backend!** 🚀
