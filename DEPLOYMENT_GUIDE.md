# 🚀 Complete Deployment Guide - Render

This guide will walk you through deploying your **TaskFlow Project Management System** on Render (both frontend and backend).

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Backend Deployment (FastAPI)](#backend-deployment-fastapi)
3. [Frontend Deployment (React)](#frontend-deployment-react)
4. [Post-Deployment Configuration](#post-deployment-configuration)
5. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before you begin, ensure you have:

- ✅ A [Render account](https://render.com) (free tier is sufficient)
- ✅ Your code pushed to a GitHub/GitLab repository
- ✅ Gmail account for email notifications (or another SMTP service)
- ✅ Basic understanding of environment variables

---

## Backend Deployment (FastAPI)

### Step 1: Create PostgreSQL Database

1. **Go to Render Dashboard**
   - Visit https://dashboard.render.com
   - Click **"New +"** → **"PostgreSQL"**

2. **Configure Database**
   - **Name**: `taskflow-db`
   - **Database**: `taskflow_db`
   - **User**: `taskflow_user`
   - **Region**: Choose closest to you
   - **Plan**: Free
   - Click **"Create Database"**

3. **Save Database URL**
   - Once created, go to the database details page
   - Copy the **"Internal Database URL"** (starts with `postgresql://`)
   - You'll need this in the next step

### Step 2: Deploy FastAPI Backend

1. **Create New Web Service**
   - Click **"New +"** → **"Web Service"**
   - Connect your GitHub/GitLab repository
   - Select your repository

2. **Configure Service**
   ```
   Name:           taskflow-backend
   Region:         Same as your database
   Branch:         main (or master)
   Root Directory: Server
   Runtime:        Python 3
   Build Command:  ./build.sh
   Start Command:  uvicorn app.main:app --host 0.0.0.0 --port $PORT
   Plan:           Free
   ```

3. **Set Environment Variables**
   
   Click **"Advanced"** → **"Add Environment Variable"** and add:

   | Key | Value | Notes |
   |-----|-------|-------|
   | `DATABASE_URL` | `postgresql://...` | Paste the Internal Database URL from Step 1 |
   | `SECRET_KEY` | Generate random string | Use: `openssl rand -hex 32` |
   | `ALGORITHM` | `HS256` | |
   | `ACCESS_TOKEN_EXPIRE_MINUTES` | `600` | |
   | `CLIENT_URL` | `https://taskflow-frontend.onrender.com` | Update after frontend deployment |
   | `MAIL_USERNAME` | `your-email@gmail.com` | Your Gmail address |
   | `MAIL_PASSWORD` | `your-app-password` | Gmail App Password (see below) |
   | `MAIL_FROM` | `your-email@gmail.com` | Same as MAIL_USERNAME |
   | `MAIL_SERVER` | `smtp.gmail.com` | |
   | `MAIL_PORT` | `587` | |

   **🔐 Getting Gmail App Password:**
   1. Go to https://myaccount.google.com/security
   2. Enable 2-Step Verification if not already enabled
   3. Go to **"App passwords"**
   4. Select **"Mail"** and **"Other (Custom name)"**
   5. Enter "TaskFlow" and click **"Generate"**
   6. Copy the 16-character password

4. **Make build.sh Executable**
   
   Before deploying, ensure `Server/build.sh` is executable:
   ```bash
   cd Server
   chmod +x build.sh
   git add build.sh
   git commit -m "Make build.sh executable"
   git push
   ```

5. **Deploy**
   - Click **"Create Web Service"**
   - Wait 5-10 minutes for deployment
   - Check logs for any errors

6. **Verify Backend**
   - Once deployed, visit: `https://taskflow-backend.onrender.com/docs`
   - You should see the FastAPI Swagger documentation
   - Test the health endpoint: `https://taskflow-backend.onrender.com/health`

---

## Frontend Deployment (React)

### Step 1: Update Backend URL

1. **Get Backend URL**
   - Copy your backend URL: `https://taskflow-backend.onrender.com`

### Step 2: Deploy React Frontend

1. **Create New Static Site**
   - Click **"New +"** → **"Static Site"**
   - Connect your repository
   - Select your repository

2. **Configure Service**
   ```
   Name:           taskflow-frontend
   Branch:         main (or master)
   Root Directory: client
   Build Command:  npm install && npm run build
   Publish Dir:    dist
   ```

3. **Set Environment Variables**
   
   Click **"Advanced"** → **"Add Environment Variable"**:

   | Key | Value |
   |-----|-------|
   | `VITE_API_BASE_URL` | `https://taskflow-backend.onrender.com` |

4. **Configure Redirects for SPA**
   
   Render auto-detects this for React apps, but verify in settings:
   - **Redirect/Rewrite Rules**: `/* → /index.html (rewrite)`

5. **Deploy**
   - Click **"Create Static Site"**
   - Wait 3-5 minutes for deployment

6. **Verify Frontend**
   - Visit: `https://taskflow-frontend.onrender.com`
   - You should see the login page

---

## Post-Deployment Configuration

### Step 1: Update Backend CORS

1. Go to your **backend service** on Render
2. Click **"Environment"**
3. Update `CLIENT_URL` to your frontend URL:
   ```
   CLIENT_URL = https://taskflow-frontend.onrender.com
   ```
4. Click **"Save Changes"**
5. Backend will automatically redeploy

### Step 2: Test the Application

1. **Register a New User**
   - Go to `https://taskflow-frontend.onrender.com/register`
   - Create an account with:
     - Valid email
     - Password with at least 8 characters, uppercase, lowercase, number, and special character

2. **Check Email**
   - You should receive a welcome email
   - If not, check spam folder

3. **Login**
   - Use your credentials to login
   - You should be redirected to the dashboard

4. **Test Features**
   - Create a project
   - Create tasks
   - Drag and drop tasks on Kanban board
   - Assign tasks to users

### Step 3: Create First Admin User (Manual)

Since the first user is created as 'user' role by default, you need to manually promote them to 'admin':

1. **Access Database Shell**
   - Go to your database in Render Dashboard
   - Click **"Connect"** → **"External Connection"**
   - Use a PostgreSQL client (like pgAdmin or DBeaver)

2. **Update User Role**
   ```sql
   UPDATE users 
   SET role = 'admin' 
   WHERE email = 'your-email@gmail.com';
   ```

3. **Alternative: Use Render Shell**
   - In your backend service, click **"Shell"**
   - Run:
   ```bash
   python
   >>> from app.core.database import SessionLocal
   >>> from app.models.user import User
   >>> db = SessionLocal()
   >>> user = db.query(User).filter(User.email == "your-email@gmail.com").first()
   >>> user.role = "admin"
   >>> db.commit()
   >>> exit()
   ```

---

## 🔄 Continuous Deployment

Both services are now set up for automatic deployments:

- **Push to GitHub** → Render automatically rebuilds and deploys
- **Environment changes** → Manual redeploy needed

---

## ⚙️ Environment Variables Reference

### Backend Required Variables

```bash
# Database
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Security
SECRET_KEY=your-super-secret-key-min-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=600

# Email (Optional but recommended)
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
MAIL_FROM=your-email@gmail.com
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587

# CORS
CLIENT_URL=https://your-frontend.onrender.com
```

### Frontend Required Variables

```bash
VITE_API_BASE_URL=https://your-backend.onrender.com
```

---

## 🐛 Troubleshooting

### Backend Issues

#### 1. **Build Failed: Permission Denied on build.sh**

**Solution:**
```bash
cd Server
chmod +x build.sh
git add build.sh
git commit -m "Make build.sh executable"
git push
```

#### 2. **Database Connection Error**

**Symptoms:** `connection refused` or `could not connect to server`

**Solution:**
- Verify `DATABASE_URL` is set correctly
- Use the **Internal Database URL** (not external)
- Ensure database and backend are in the same region

#### 3. **Migration Errors**

**Symptoms:** Alembic errors during build

**Solution:**
```bash
# In Render Shell
alembic downgrade -1
alembic upgrade head
```

#### 4. **CORS Errors**

**Symptoms:** Frontend can't connect to backend

**Solution:**
- Verify `CLIENT_URL` in backend env vars matches your frontend URL
- Check browser console for exact error
- Ensure no trailing slashes in URLs

#### 5. **Email Not Sending**

**Symptoms:** No welcome emails

**Solution:**
- Verify Gmail App Password (not regular password)
- Check Gmail "Less secure app access" is NOT enabled (use App Password instead)
- Check backend logs for email errors
- Test with a different email provider

### Frontend Issues

#### 1. **Blank Page After Deployment**

**Solution:**
- Check browser console for errors
- Verify `VITE_API_BASE_URL` is set correctly
- Check Network tab - are API calls reaching backend?

#### 2. **404 on Page Refresh**

**Solution:**
- Ensure redirect rule is set: `/* → /index.html (rewrite)`
- In Render dashboard → Static Site → Redirects/Rewrites

#### 3. **Build Fails**

**Solution:**
```bash
# Test build locally first
cd client
yarn install
yarn build
```

### Database Issues

#### 1. **Free Tier Database Expires**

**Note:** Render free databases expire after 90 days

**Solution:**
- Backup your data regularly
- Upgrade to paid plan for persistence
- Or recreate database and run migrations

#### 2. **Connection Limit Reached**

**Symptoms:** `too many connections`

**Solution:**
- Free tier has 97 connection limit
- Add to `database.py`:
```python
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=5,
    max_overflow=10
)
```

---

## 📊 Free Tier Limitations

### Render Free Tier

| Service | Limitation |
|---------|------------|
| **Web Service** | 750 hours/month, sleeps after 15 min inactivity |
| **Static Site** | 100 GB bandwidth/month |
| **Database** | 1 GB storage, expires after 90 days |
| **Build Minutes** | Unlimited |

**⚠️ Important Notes:**
- Free services spin down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds (cold start)
- Database expires after 90 days (backup regularly!)

---

## 🎉 Success!

Your TaskFlow application is now deployed! 

**URLs:**
- Frontend: `https://taskflow-frontend.onrender.com`
- Backend: `https://taskflow-backend.onrender.com`
- API Docs: `https://taskflow-backend.onrender.com/docs`

---

## 🔒 Security Best Practices

1. **Never commit `.env` files** - Use Render's environment variables
2. **Use strong SECRET_KEY** - Minimum 32 characters, random
3. **Enable HTTPS** - Render provides this automatically
4. **Regular backups** - Export database regularly
5. **Monitor logs** - Check for suspicious activity

---

## 📚 Additional Resources

- [Render Documentation](https://render.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Vite Production Build](https://vitejs.dev/guide/build.html)
- [PostgreSQL on Render](https://render.com/docs/databases)

---

## 🆘 Need Help?

If you encounter issues:

1. **Check Render Logs**
   - Go to your service → "Logs" tab
   - Look for error messages

2. **Check Browser Console**
   - Press F12 → Console tab
   - Look for network errors

3. **Database Shell**
   - Access database directly to debug data issues

4. **Render Community**
   - Visit Render community forum
   - Search for similar issues

---

## 🔄 Updates and Maintenance

### Updating the Application

1. **Make changes locally**
2. **Test thoroughly**
3. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Your update message"
   git push origin main
   ```
4. **Render auto-deploys** (or click "Manual Deploy")

### Database Migrations

When you add new models or change existing ones:

1. **Create migration locally**
   ```bash
   cd Server
   alembic revision --autogenerate -m "Description"
   ```

2. **Test migration**
   ```bash
   alembic upgrade head
   ```

3. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Add database migration"
   git push
   ```

4. **Render will run migrations automatically** via `build.sh`

---

**Happy Deploying! 🚀**

