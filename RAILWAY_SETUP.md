# Railway Deployment - Quick Setup

## Step 1: Add these Environment Variables in Railway

Go to your Railway project → Variables tab → Add these:

```bash
# Required
SECRET_KEY=<generate-a-random-string-here>
DJANGO_SETTINGS_MODULE=proshop.settings.production

# Railway automatically provides DATABASE_URL from PostgreSQL service
# No need to set DATABASE_URL manually if you added PostgreSQL service

# Optionally customize these:
ALLOWED_HOSTS=${{ RAILWAY_PUBLIC_DOMAIN }},*.railway.app,vibevault-production.up.railway.app
```

## Step 2: Generate SECRET_KEY

Run this locally to generate a secure SECRET_KEY:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Or use this online: `openssl rand -base64 50`

Copy the output and set it as `SECRET_KEY` in Railway.

## Step 3: Add PostgreSQL Database

In Railway:
1. Click "New" → "Database" → "PostgreSQL"
2. Railway will automatically create a `DATABASE_URL` variable
3. Your app will use this automatically!

## Step 4: Deploy

1. Connect your GitHub repository
2. Railway will auto-detect the Dockerfile
3. Deploy will start automatically

## Verification

After deployment, check:
- Logs for any errors
- Visit: `https://your-app.railway.app/admin`
- API docs: `https://your-app.railway.app/api/schema/swagger-ui/`

## Default Superuser

After first deployment, a default superuser is created:
- **Username:** admin
- **Password:** admin123
- ⚠️ **Change this immediately in production!**

---

**Need help?** See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed instructions.
