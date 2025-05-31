# GigFusion - Render.com Deployment

This directory contains all the files needed to deploy GigFusion frontend to Render.com.

## 🚀 Quick Deploy to Render

### 1. Push to GitHub
```bash
# Navigate to this render directory
cd render

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "GigFusion Render deployment"

# Add your GitHub repository
git remote add origin https://github.com/YOUR_USERNAME/gigfusion-render.git
git branch -M main
git push -u origin main
```

### 2. Deploy on Render.com
1. Go to https://render.com
2. Create new Web Service
3. Connect your GitHub repository
4. Use these settings:
   - **Build Command**: `pip install -r requirements_render.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT render_app:app`
   - **Environment**: Python 3

### 3. Environment Variables
Set these in Render dashboard:
- `FLASK_ENV` = `production`
- `SECRET_KEY` = [Generate in Render]
- `EC2_API_URL` = `http://ec2-54-221-34-34.compute-1.amazonaws.com:5000`

## 📁 Files Included
- `render_app.py` - Main Flask application
- `render.yaml` - Render service configuration
- `requirements_render.txt` - Production dependencies
- `ec2_api_client.py` - API client for EC2 backend
- `config.py` - Flask configuration
- `models.py` - Database models
- `forms.py` - Flask forms
- `templates/` - HTML templates
- `static/` - CSS, JS, images

## 🔗 Architecture
```
Internet → Render.com (Frontend) → EC2 (Backend API) → AWS RDS (Database)
```

## 🧪 Test Your Deployment
After deployment, test these features:
- Homepage loading
- User registration/login
- Dashboard access
- Post browsing
- Backend connectivity

Your live app will be available at: `https://your-app-name.onrender.com`
