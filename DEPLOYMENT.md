# Promethean-Unified-Platform - PythonAnywhere Deployment Guide

## Overview

This guide covers deploying the Promethean-Unified-Platform to PythonAnywhere with full HTTPS security, DeepSeek LLM integration, and Supabase backend support.

## Architecture

- **Backend Framework**: Flask with CORS support
- **LLM Provider**: DeepSeek API (uncensored, transparent AI)
- **Database**: Supabase (PostgreSQL with real-time features)
- **Hosting**: PythonAnywhere (Python 3.x)
- **Security**: HTTPS/SSL, HSTS headers, CSP, WSGI application

## Pre-Deployment Checklist

- [x] HTTPS security headers configured in app.py
- [x] DeepSeek LLM integration implemented
- [x] Environment variables template (.env.example) created
- [x] WSGI application configured (wsgi.py)
- [x] Requirements.txt with all dependencies
- [ ] PythonAnywhere account created
- [ ] DeepSeek API key obtained
- [ ] Supabase credentials configured

## Deployment Steps

### Step 1: PythonAnywhere Web App Setup

1. Log into [PythonAnywhere.com](https://www.pythonanywhere.com/)
2. Go to Web tab → Add a new web app
3. Choose Flask framework
4. Select Python 3.10+ (latest available)
5. Choose manual configuration

### Step 2: Clone Repository

In PythonAnywhere console:

```bash
cd /home/yourusername
git clone https://github.com/LittleBunneh/Promethean-Unified-Platform.git
cd Promethean-Unified-Platform
```

### Step 3: Create Virtual Environment

```bash
mkvirtualenv --python=/usr/bin/python3.10 promethean
workon promethean
pip install -r requirements.txt
```

### Step 4: Create .env File

Create `/home/yourusername/Promethean-Unified-Platform/.env`:

```
# Supabase Configuration
SUPABASE_URL=https://gmxvnzqouuwqvcismixp.supabase.co
SUPABASE_ANON_KEY=your_supabase_anon_key_here

# DeepSeek LLM Configuration
DEEPSEEK_API_KEY=YOUR_DEEPSEEK_API_KEY_HERE

# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False

# Server Configuration
SERVER_PORT=5000
SERVER_HOST=0.0.0.0
```

**⚠️ IMPORTANT**: Replace `YOUR_DEEPSEEK_API_KEY_HERE` with your actual DeepSeek API key from [platform.deepseek.com](https://platform.deepseek.com/api_keys)

### Step 5: Configure WSGI Application

1. In PythonAnywhere Web tab, edit WSGI configuration
2. Replace default content with:

```python
import sys
import os
from pathlib import Path

# Add project to path
project_folder = '/home/yourusername/Promethean-Unified-Platform'
sys.path.insert(0, project_folder)

# Set environment
os.environ['FLASK_ENV'] = 'production'
os.environ['FLASK_DEBUG'] = 'False'

# Load .env
from dotenv import load_dotenv
load_dotenv(os.path.join(project_folder, '.env'))

# Import Flask app
from backend.app import app

# WSGI application
application = app
```

3. Save the file

### Step 6: Configure Web App Settings

1. **Virtualenv**: Set to `/home/yourusername/.virtualenvs/promethean`
2. **Source Code**: `/home/yourusername/Promethean-Unified-Platform`
3. **WSGI Configuration File**: `/home/yourusername/Promethean-Unified-Platform/pythonanywhere_wsgi.py`
4. **Python version**: 3.10+

### Step 7: Enable HTTPS/SSL

1. Go to Web tab → Security section
2. Force HTTPS: **ON**
3. HSTS: **Enabled** (max_age=31536000)

PythonAnywhere provides free HTTPS certificates via Let's Encrypt.

### Step 8: Configure Static Files

In PythonAnywhere Web tab:

- **Static files URL**: `/static/`
- **Static files directory**: `/home/yourusername/Promethean-Unified-Platform/static`

### Step 9: Reload Web App

1. Go to Web tab
2. Click **Reload** button for your web app
3. Visit `https://yourusername.pythonanywhere.com`

## API Endpoints

### Health Check
```
POST /health
```

### Chat Interaction
```
POST /api/chat
Content-Type: application/json

{
  "message": "Your question here",
  "conversation_id": "optional_id"
}
```

### Consciousness Interaction
```
POST /api/consciousness/interact
Content-Type: application/json

{
  "message": "Your message here"
}
```

### Get Conversations
```
GET /api/conversations
```

## Security Features

✓ **HTTPS Enforcement**: All traffic encrypted with TLS
✓ **HSTS Headers**: Browser enforces HTTPS for future visits
✓ **Content Security Policy**: Prevents XSS attacks
✓ **Frame Protection**: X-Frame-Options deny clickjacking
✓ **XSS Protection**: X-XSS-Protection enabled
✓ **Referrer Policy**: Strict origin information sharing

## DeepSeek LLM Integration

### System Prompt Design

The system is configured with a prompt that:
- Enables transparent discussion of controversial topics
- Maintains ethical boundaries (no harm instructions)
- Demonstrates intellectual rigor
- Provides disclaimer about limitations

### Example Request

```bash
curl -X POST https://yourusername.pythonanywhere.com/api/chat \
  -H "Content-Type: application/json" \
  -H "user-id: unique-user-id" \
  -d '{"message": "Explain a controversial topic", "conversation_id": "conv-123"}'
```

## Troubleshooting

### 502 Bad Gateway
- Check PythonAnywhere error logs
- Verify WSGI configuration
- Ensure .env file exists and is readable
- Check virtual environment is activated

### "Module not found" errors
- Ensure virtual environment is correctly set
- Run `pip install -r requirements.txt` again
- Verify Python path in WSGI configuration

### DeepSeek API errors
- Verify API key is correct in .env
- Check DeepSeek account has credits
- Review API response in server logs

### Static files not loading
- Verify static directory path in Web settings
- Check file permissions (755 for directories, 644 for files)
- Reload web app after changes

## Monitoring

1. **PythonAnywhere Log Files**: View in Web → Log files section
2. **Error Log**: Check `/var/log/yourusername.pythonanywhere.com_error.log`
3. **Access Log**: Monitor API usage patterns

## Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| SUPABASE_URL | Yes | Supabase project URL |
| SUPABASE_ANON_KEY | Yes | Supabase anonymous key |
| DEEPSEEK_API_KEY | Yes | DeepSeek API authentication |
| FLASK_ENV | Yes | Set to 'production' |
| FLASK_DEBUG | Yes | Set to 'False' |
| SERVER_PORT | No | Default: 5000 |
| SERVER_HOST | No | Default: 0.0.0.0 |

## Post-Deployment Verification

```bash
# 1. Test HTTPS
curl -I https://yourusername.pythonanywhere.com/

# 2. Verify security headers
curl -I https://yourusername.pythonanywhere.com/ | grep -E "Strict-Transport-Security|X-Frame-Options|X-Content-Type-Options"

# 3. Test API
curl -X POST https://yourusername.pythonanywhere.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Test message", "conversation_id": "test"}'
```

## Performance Optimization

- **Caching**: Implement Redis caching for frequent queries
- **Database**: Index conversation_id and user_id columns
- **API Rate Limiting**: Consider adding rate limiting for DeepSeek API
- **Static Compression**: Enable gzip for static files

## Support & Resources

- [PythonAnywhere Help](https://help.pythonanywhere.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [DeepSeek API Docs](https://platform.deepseek.com/api-docs)
- [Supabase Documentation](https://supabase.com/docs)

## License

This project is part of Promethean Conduit AI initiative.
