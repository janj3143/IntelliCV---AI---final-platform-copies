# SANDBOX INTEGRATION GUIDE - AI Model Training System

**Date:** October 14, 2025  
**Status:** ✅ FILES COPIED TO SANDBOX  
**Purpose:** Side-by-side comparison testing with existing system

---

## 📦 FILES COPIED TO SANDBOX

### Backend AI Services (4 engines)
1. ✅ `backend/ai_services/model_trainer.py` (570 lines)
2. ✅ `backend/ai_services/neural_network_engine.py` (420 lines)
3. ✅ `backend/ai_services/expert_system_engine.py` (780 lines)
4. ✅ `backend/ai_services/feedback_loop_engine.py` (850 lines)

### Admin UI Dashboard
5. ✅ `pages/23_AI_Model_Training_Review.py` (670 lines)

### Supporting Files
6. ✅ `backend/__init__.py` (package initialization)
7. ✅ `backend/ai_services/__init__.py` (AI services package)

### Directory Structure Created
```
SANDBOX/admin_portal/
├── backend/
│   ├── __init__.py
│   ├── ai_services/
│   │   ├── __init__.py
│   │   ├── model_trainer.py
│   │   ├── neural_network_engine.py
│   │   ├── expert_system_engine.py
│   │   └── feedback_loop_engine.py
│   ├── logs/                    (for engine logs)
│   └── data/
│       ├── rules/               (Expert System rules)
│       ├── feedback/            (Feedback Loop data)
│       └── models/              (Trained models)
└── pages/
    └── 23_AI_Model_Training_Review.py
```

---

## 🚀 HOW TO ACCESS THE NEW SYSTEM

### Option 1: Through Streamlit Admin Portal

1. **Start the admin portal:**
   ```powershell
   cd c:\IntelliCV-AI\IntelliCV\SANDBOX\admin_portal
   streamlit run main.py
   ```

2. **Navigate to page 23:**
   - Look for "23 AI Model Training Review" in the sidebar
   - Click to open the dashboard

3. **What you'll see:**
   - 5 tabs: Overview, Training Scenarios, Train Models, Review Queue, Performance
   - System will auto-initialize all 4 AI engines on first load

### Option 2: Direct Access to Page

```powershell
cd c:\IntelliCV-AI\IntelliCV\SANDBOX\admin_portal
streamlit run pages/23_AI_Model_Training_Review.py
```

### Option 3: Test Individual Engines

**Test Model Trainer:**
```powershell
cd c:\IntelliCV-AI\IntelliCV\SANDBOX\admin_portal\backend\ai_services
python model_trainer.py
```

**Test Neural Network Engine:**
```powershell
python neural_network_engine.py
```

**Test Expert System Engine:**
```powershell
python expert_system_engine.py
```

**Test Feedback Loop Engine:**
```powershell
python feedback_loop_engine.py
```

Each engine has a test harness in its `__main__` section.

---

## 📋 PREREQUISITES

### Required Python Packages

The new system requires these packages (check if already installed):

```python
# Core packages (likely already installed)
import streamlit
import pandas
import plotly
import numpy

# Standard library (built-in)
import json
import logging
import pathlib
import datetime
import statistics
```

### Check Installation

```powershell
# Check if packages are installed
python -c "import streamlit; print('Streamlit OK')"
python -c "import pandas; print('Pandas OK')"
python -c "import plotly; print('Plotly OK')"
python -c "import numpy; print('Numpy OK')"
```

### Install Missing Packages

```powershell
pip install streamlit pandas plotly numpy
```

---

## 🧪 TESTING CHECKLIST

### Phase 1: Individual Engine Testing

- [ ] **Model Trainer Test**
  ```powershell
  cd c:\IntelliCV-AI\IntelliCV\SANDBOX\admin_portal\backend\ai_services
  python model_trainer.py
  ```
  - Should create 5 default scenarios
  - Should scan IntelliCV-data for training files
  - Should show test output

- [ ] **Neural Network Test**
  ```powershell
  python neural_network_engine.py
  ```
  - Should calculate semantic similarity
  - Should generate predictions with confidence
  - Should show performance metrics

- [ ] **Expert System Test**
  ```powershell
  python expert_system_engine.py
  ```
  - Should load 10 default rules
  - Should validate predictions
  - Should provide explanations

- [ ] **Feedback Loop Test**
  ```powershell
  python feedback_loop_engine.py
  ```
  - Should register mock engines
  - Should perform ensemble voting
  - Should track performance

### Phase 2: Dashboard Testing

- [ ] **Access Dashboard**
  ```powershell
  cd c:\IntelliCV-AI\IntelliCV\SANDBOX\admin_portal
  streamlit run pages/23_AI_Model_Training_Review.py
  ```

- [ ] **Tab 1 - Overview**
  - Check system status cards display
  - Check scenario status table
  - Check performance charts render

- [ ] **Tab 2 - Training Scenarios**
  - Try creating a new scenario
  - View existing scenarios
  - Check scenario details

- [ ] **Tab 3 - Train Models**
  - Select a scenario
  - Check training data preview
  - Try training (may need actual CV data)

- [ ] **Tab 4 - Review Queue**
  - Check if review queue displays
  - Try filtering and sorting
  - Test approve/correct actions

- [ ] **Tab 5 - Performance**
  - Check engine performance metrics
  - Check Expert System rules stats
  - Check Neural Network metrics

### Phase 3: Integration Testing

- [ ] **Data Integration**
  - Verify IntelliCV-data directory accessible
  - Check if CVs can be loaded
  - Test training data loading

- [ ] **Persistence Testing**
  - Create a scenario → restart → check if persisted
  - Create a rule → restart → check if persisted
  - Submit feedback → restart → check if persisted

- [ ] **Logging Testing**
  - Check `backend/logs/` for log files
  - Verify logs are being written
  - Check log content for errors

---

## 🔍 COMPARISON WITH EXISTING SYSTEM

### What's NEW in This System

1. **Model Training System**
   - OLD: No formal training system
   - NEW: Complete training framework with scenarios, versioning, A/B testing

2. **Neural Network Engine**
   - OLD: No neural network capabilities
   - NEW: Embeddings, semantic similarity, confidence scoring

3. **Expert System Engine**
   - OLD: No rule-based validation
   - NEW: 10 business rules, explainability, admin-editable

4. **Feedback Loop Engine**
   - OLD: No ensemble voting
   - NEW: All engines vote, weighted ensemble, auto-learning

5. **Admin Dashboard**
   - OLD: Separate pages for different functions
   - NEW: Unified 5-tab dashboard for complete control

### What's EXISTING (Keep Using)

1. **Unified AI Engine** (`services/unified_ai_engine.py`)
   - Bayesian classification
   - NLP processing
   - LLM integration
   - Fuzzy logic
   - Still works independently

2. **Enhanced Job Title Engine** (`services/enhanced_job_title_engine.py`)
   - Job title classification
   - Can be integrated with new Neural Network

3. **Complete Data Parser** (`services/complete_data_parser.py`)
   - CV parsing
   - Data extraction
   - Works as before

### Integration Opportunities

**Phase 1 (Current):** Side-by-side testing
- New system operates independently
- Existing system continues working
- Compare results between both

**Phase 2 (Future):** Hybrid Integration
- Connect Feedback Loop with Unified AI Engine
- Ensemble voting: New NN + Existing Bayesian/NLP/LLM
- Best of both worlds

**Phase 3 (Future):** Full Merger
- Replace individual engines with Feedback Loop orchestrator
- Unified dashboard for all AI operations
- Single source of truth

---

## 📊 EXPECTED BEHAVIOR

### First Time Startup

1. **Dashboard loads** (may take 10-15 seconds)
2. **Engines initialize:**
   - Model Trainer: Creates 5 default scenarios
   - Neural Network: Initializes embedding cache
   - Expert System: Loads 10 default rules
   - Feedback Loop: Registers engines
3. **Logs created** in `backend/logs/`
4. **Data directories created** in `backend/data/`

### During Training

1. **Select scenario** in Tab 3
2. **Training data loads** from IntelliCV-data
3. **Training executes** (may take minutes depending on data size)
4. **Model saved** to `backend/data/models/[scenario_id]/`
5. **Metrics displayed** in dashboard

### During Review

1. **Low-confidence predictions** appear in review queue
2. **Admin reviews** in Tab 4
3. **Corrections applied** automatically feed back to training
4. **After 100 corrections** → auto-retrain triggered

---

## 🐛 TROUBLESHOOTING

### Issue: "Import could not be resolved"

**Cause:** Backend path not in Python path

**Solution:** Engines add backend to path automatically, but if issues persist:
```python
import sys
from pathlib import Path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))
```

### Issue: "No training data found"

**Cause:** IntelliCV-data directory not accessible

**Solution:** 
1. Check if IntelliCV-data exists: `c:\IntelliCV-AI\IntelliCV-data\`
2. Check if contains CV files (PDF, DOC, DOCX)
3. Update path in model_trainer.py if needed

### Issue: "Streamlit page not showing in sidebar"

**Cause:** Page number conflict or naming issue

**Solution:**
1. Check pages directory for duplicate numbers
2. Ensure file name starts with number: `23_`
3. Restart Streamlit server

### Issue: "Engine initialization failed"

**Cause:** Missing dependencies or file permissions

**Solution:**
1. Check Python packages installed
2. Check directory permissions for `backend/logs/` and `backend/data/`
3. Check error logs in `backend/logs/`

### Issue: "Rules not saving"

**Cause:** File permissions or path issues

**Solution:**
1. Check `backend/data/rules/` directory exists
2. Check write permissions
3. Check logs for error messages

---

## 📈 PERFORMANCE EXPECTATIONS

### Training Time
- **Small dataset** (<100 CVs): 1-2 minutes
- **Medium dataset** (100-1000 CVs): 5-10 minutes
- **Large dataset** (>1000 CVs): 15-30 minutes

### Prediction Time
- **Single prediction:** <100ms
- **Ensemble prediction (7 engines):** <500ms
- **Batch predictions (100):** 10-30 seconds

### Memory Usage
- **Dashboard idle:** ~200-300 MB
- **During training:** 500 MB - 2 GB (depends on data size)
- **All engines loaded:** ~400-500 MB

---

## 🎯 SUCCESS CRITERIA

**System is working correctly if:**

1. ✅ All 4 engines initialize without errors
2. ✅ Dashboard loads and displays 5 tabs
3. ✅ Can create new training scenarios
4. ✅ Can load training data from IntelliCV-data
5. ✅ Can execute training and see results
6. ✅ Review queue displays flagged predictions
7. ✅ Can approve/correct predictions
8. ✅ Performance metrics update correctly
9. ✅ Logs are created in backend/logs/
10. ✅ Rules/feedback/models persist across restarts

---

## 🔗 NEXT STEPS

### Immediate (This Week)
1. Test all engines individually
2. Test dashboard with real data
3. Compare results with existing system
4. Document any issues or improvements

### Short-term (Next Week)
1. Integrate Feedback Loop with Unified AI Engine
2. Test ensemble voting with all 7 engines
3. Train models on full IntelliCV-data dataset
4. Measure accuracy improvements

### Long-term (Next Month)
1. Create backend API server
2. Migrate all services to backend
3. Create user portal integration
4. Deploy Phase 5: Proof in the Pudding testing

---

## 📞 SUPPORT

**Issues or Questions:**
1. Check logs in `backend/logs/`
2. Review this integration guide
3. Test individual engines to isolate issues
4. Check REORIENTATION workspace for reference implementation

**Documentation:**
- `AI_MODEL_TRAINING_COMPLETION_SUMMARY.md` - Complete feature list
- `REORIENTATION_PROJECT_STATUS.md` - Project roadmap
- Individual engine files have detailed docstrings

---

**STATUS: ✅ READY FOR TESTING IN SANDBOX**

**Location:** `c:\IntelliCV-AI\IntelliCV\SANDBOX\admin_portal\`

**Next Action:** Run `streamlit run main.py` and test page 23!
