# 🚀 HealthSense AI - Quick Start Guide

## 📋 Current Project Status

✅ **Completed:**
- Project structure created
- Core dependencies installed and tested
- Security setup with `.env` configuration
- HospitalComparisonAgent implemented
- FastAPI app created with proper endpoints
- Static homepage created
- Dockerfile created
- Compatibility testing completed

⚠️ **Needs Attention:**
- Revoke exposed API key
- Create `.env` file with new API key
- Create remaining agent files (Doctor, Emergency, Diagnostic)
- Create `main.py` for CrewAI routing

---

## 🏗️ Project Structure

```
healthsense_main/
├── data/                           # Datasets
│   ├── Hospital_General_Information.csv
│   ├── Hospital_Information_with_Lab_Tests.csv
│   └── hospitals_emergency_data.csv
│
├── src/                            # Source code
│   ├── __init__.py                 ✅ Created
│   ├── HospitalComparisonAgent.py  ✅ Created
│   ├── DoctorInfoAgent.py          ✅ Created
│   ├── EmergencyServicesAgent.py   ✅ Created
│   ├── DiagnosticInfoAgent.py      ✅ Created
│   ├── app.py                      ✅ Created (FastAPI)
│   ├── constants.py                ✅ Created (with dotenv)
│   ├── main.py                     ✅ Created (CrewAI)
│   ├── appointments.db             (auto-generated)
│   └── emergency.db                (auto-generated)
│
├── static/                         # Frontend
│   └── index.html                  ✅ Created
│
├── .env.example                    ✅ Created
├── .env                            ✅ Created
├── .gitignore                      ✅ Created
├── Dockerfile                      ✅ Created
├── requirements.txt                ✅ Updated
├── test_compatibility.py           ✅ Created
├── SECURITY_SETUP.md               ✅ Created
├── WEEK7_CODE_REVIEW.md            ✅ Created
└── README.md                       ✅ Created
```

---

## 🔧 Setup Steps

### Step 1: Security Setup (CRITICAL)

```bash
# 1. Revoke the exposed API key
# Go to: https://platform.openai.com/api-keys
# Find and revoke the exposed key

# 2. Create new API key at the same link

# 3. Create .env file
copy .env.example .env

# 4. Edit .env and add your NEW API key
notepad .env
```

Your `.env` should look like:
```env
OPENAI_API_KEY=sk-proj-YOUR_NEW_KEY_HERE
MODEL_NAME=gpt-3.5-turbo
```

### Step 2: Verify Setup

```bash
# Test that API key loads
python -c "from src.constants import OPENAI_API_KEY; print('✓ API Key loaded successfully')"

# Run compatibility test
python test_compatibility.py
```

### Step 3: Run the Application

```bash
# Option A: Run with uvicorn (development)
python -m uvicorn src.app:app --reload --port 7860

# Option B: Run directly
python -m src.app

# Access at: http://localhost:7860
```

### Step 4: Test the API

```bash
# Test homepage
curl http://localhost:7860/

# Test health check
curl http://localhost:7860/health

# Test hospital comparison
curl -X POST http://localhost:7860/compare-hospitals \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"Find hospitals in Boston\"}"
```

---

## 🐳 Docker Deployment

### Build and Run Locally

```bash
# Build Docker image
docker build -t healthsense-ai .

# Run container
docker run -p 7860:7860 --env-file .env healthsense-ai

# Access at: http://localhost:7860
```

### Deploy to Hugging Face Spaces

1. **Create Space:**
   - Go to https://huggingface.co/spaces
   - Click "Create new Space"
   - Name: `healthsense-ai`
   - SDK: **Docker**

2. **Upload Files:**
   ```
   - Dockerfile
   - requirements.txt
   - src/ (entire folder)
   - data/ (entire folder)
   - static/ (entire folder)
   ```

3. **Add Secret:**
   - Go to Settings → Repository secrets
   - Add: `OPENAI_API_KEY` = your_api_key

4. **Deploy:**
   - Space will auto-build and deploy
   - Access at: `https://huggingface.co/spaces/YOUR_USERNAME/healthsense-ai`

---

## 📝 Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message and API info |
| GET | `/health` | Health check endpoint |
| POST | `/compare-hospitals` | Compare hospitals based on query |
| POST | `/query` | General query (auto-routes to agent) |

### Example Requests:

```bash
# Hospital Comparison
curl -X POST http://localhost:7860/compare-hospitals \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Compare hospitals with cardiology department in San Francisco"
  }'

# General Query
curl -X POST http://localhost:7860/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Find top-rated hospitals near Boston"
  }'
```

---

## 🔍 Troubleshooting

### Issue: ModuleNotFoundError: No module named 'src'

**Solution 1 - Run from project root:**
```bash
# Make sure you're in healthsense_main/ directory
cd C:\capstone_ic_ik\healthsense_main
python -m uvicorn src.app:app --reload
```

**Solution 2 - Add to Python path (in notebook):**
```python
import sys
import os
sys.path.insert(0, os.path.dirname(os.getcwd()))
```

### Issue: OPENAI_API_KEY not found

**Solution:**
```bash
# Check if .env file exists
dir .env

# If not, create it from template
copy .env.example .env

# Edit and add your API key
notepad .env
```

### Issue: API returns errors

**Solution:**
```bash
# Check logs
python -m uvicorn src.app:app --reload --log-level debug

# Verify data files exist
dir data\*.csv
```

---

## 📚 Next Steps

### 1. Create Remaining Agents (Week 4-5)

Create these files in `src/` directory:

- `DoctorInfoAgent.py` - Doctor appointment booking
- `EmergencyServicesAgent.py` - Emergency services locator
- `DiagnosticInfoAgent.py` - Lab test information

### 2. Implement CrewAI Routing (Week 6)

Create `src/main.py` with:
- Routing agent
- Task definitions
- Multi-agent coordination

### 3. Frontend Enhancement (Optional)

- Add interactive chat interface
- Implement WebSocket for real-time updates
- Add user authentication

### 4. Testing & Documentation (Week 8)

- Write unit tests
- Create API documentation
- Performance testing
- User guide

---

## 🎯 Week 7 Checklist

- [x] Project structure created
- [x] Virtual environment setup
- [x] Dependencies installed
- [x] Security configuration (.env)
- [x] HospitalComparisonAgent created
- [x] FastAPI app created
- [x] Static homepage created
- [x] Dockerfile created
- [ ] **Revoke exposed API key** ⚠️ URGENT
- [ ] Create .env with new key
- [ ] Test API endpoints locally
- [ ] Create remaining 3 agents
- [ ] Implement CrewAI routing
- [ ] Deploy to Hugging Face Spaces

---

## 📖 Documentation Reference

- `SECURITY_SETUP.md` - Complete security guide
- `WEEK7_CODE_REVIEW.md` - Detailed code analysis
- `test_compatibility.py` - Run to verify all dependencies
- `.env.example` - Environment variable template

---

## 🆘 Getting Help

1. **Check the code review:**
   - Read `WEEK7_CODE_REVIEW.md` for issues and fixes

2. **Run compatibility test:**
   ```bash
   python test_compatibility.py
   ```

3. **Check logs:**
   ```bash
   python -m uvicorn src.app:app --reload --log-level debug
   ```

4. **Verify setup:**
   ```bash
   python -c "from src.constants import OPENAI_API_KEY; print('OK')"
   ```

---

**Remember:** Always keep your API keys secret! Never commit `.env` to git.

**Good luck with your HealthSense AI deployment! 🚀**
