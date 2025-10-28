# IntelliCV Data Architecture - Clarification

**Date:** October 15, 2025  
**Purpose:** Clarify where all data is located and used in the IntelliCV system

---

## 🗂️ DATA DIRECTORY STRUCTURE

### Primary Data Locations

```
C:\IntelliCV-AI\IntelliCV\
│
├── BACKEND-ADMIN-REORIENTATION/              ← DEVELOPMENT WORKSPACE
│   └── admin_portal/
│       ├── backend/
│       │   ├── ai_services/                   ← Neural Network, Expert System, etc.
│       │   │   ├── model_trainer.py
│       │   │   ├── neural_network_engine.py
│       │   │   ├── expert_system_engine.py
│       │   │   ├── feedback_loop_engine.py
│       │   │   └── hybrid_integrator.py
│       │   ├── data/                          ← Backend AI data
│       │   │   ├── models/                    ← Trained models
│       │   │   ├── rules/                     ← Expert system rules
│       │   │   └── feedback/                  ← Feedback data
│       │   └── logs/                          ← Backend logs
│       └── ai_data_final/                     ← AI TRAINING DATA (primary)
│           ├── exported_cvs/
│           ├── candidate_profiles/
│           ├── enrichment_results/
│           └── training_data/
│
├── SANDBOX/                                   ← PRODUCTION/TESTING WORKSPACE
│   └── admin_portal/
│       ├── backend/                           ← SAME as REORIENTATION
│       │   ├── ai_services/                   ← Neural Network, Expert System, etc.
│       │   ├── data/                          ← Backend AI data
│       │   └── logs/                          ← Backend logs
│       ├── ai_data_final/                     ← AI TRAINING DATA (SANDBOX copy)
│       ├── services/
│       │   └── intellicv_data_manager.py      ← Updated to use SANDBOX paths
│       └── pages/
│           └── 23_AI_Model_Training_Review.py
│
└── IntelliCV-data/                            ← SHARED DATA (email, external)
    ├── email_integration/                     ← Email account data
    ├── email_extracted/                       ← CVs from email
    │   ├── gmail/
    │   ├── outlook/
    │   └── yahoo/
    └── candidate_data/                        ← Candidate information
```

---

## 🎯 CORRECT DATA PATHS FOR AI BACKEND

### For Neural Network & Expert System Development

**Location:** `C:\IntelliCV-AI\IntelliCV\BACKEND-ADMIN-REORIENTATION\admin_portal\`

**AI Services:**
- Neural Network: `backend/ai_services/neural_network_engine.py`
- Expert System: `backend/ai_services/expert_system_engine.py`
- Feedback Loop: `backend/ai_services/feedback_loop_engine.py`
- Model Trainer: `backend/ai_services/model_trainer.py`

**Data Paths:**
- Training Data: `ai_data_final/training_data/`
- Trained Models: `backend/data/models/`
- Expert Rules: `backend/data/rules/`
- Feedback Data: `backend/data/feedback/`
- Logs: `backend/logs/`

---

## 📊 DATA SOURCE PRIORITY

### For AI Training

**Primary Source:** `SANDBOX/admin_portal/ai_data_final/`
- This is where AI training data lives
- Contains CV data for model training
- Structured for AI processing

**Secondary Source:** `IntelliCV-data/email_extracted/`
- CVs extracted from email integration
- Can be imported into ai_data_final
- Organized by email provider

**Tertiary Source:** `IntelliCV-data/candidate_data/`
- Additional candidate information
- Supplementary data for enrichment

---

## 🔧 UPDATED intellicv_data_manager.py

The updated data manager now correctly handles:

### 1. **SANDBOX AI Data** (Primary for AI)
```python
self.ai_data_path = self.sandbox_root / "ai_data_final"
```
- Located at: `C:\IntelliCV-AI\IntelliCV\SANDBOX\admin_portal\ai_data_final\`
- **This is the primary source for AI training**

### 2. **Backend AI Services Data**
```python
self.backend_data_path = self.sandbox_root / "backend" / "data"
self.backend_models_path = self.backend_data_path / "models"
self.backend_rules_path = self.backend_data_path / "rules"
self.backend_feedback_path = self.backend_data_path / "feedback"
```
- Located at: `C:\IntelliCV-AI\IntelliCV\SANDBOX\admin_portal\backend\data\`
- **This is where neural network, expert system store their data**

### 3. **Email Integration Data** (Secondary)
```python
self.email_extracted_path = self.intellicv_data_path / "email_extracted"
```
- Located at: `C:\IntelliCV-AI\IntelliCV\IntelliCV-data\email_extracted\`
- **This is where email CVs are extracted**

---

## 🚀 HOW TO USE

### For Model Trainer

```python
from backend.ai_services.model_trainer import ModelTrainer

trainer = ModelTrainer()

# Automatically loads training data from:
# C:\IntelliCV-AI\IntelliCV\SANDBOX\admin_portal\ai_data_final\training_data\

# Saves models to:
# C:\IntelliCV-AI\IntelliCV\SANDBOX\admin_portal\backend\data\models\
```

### For Neural Network

```python
from backend.ai_services.neural_network_engine import NeuralNetworkEngine

nn = NeuralNetworkEngine()

# Stores embeddings cache in memory
# Processes feedback from:
# C:\IntelliCV-AI\IntelliCV\SANDBOX\admin_portal\backend\data\feedback\
```

### For Expert System

```python
from backend.ai_services.expert_system_engine import ExpertSystemEngine

expert = ExpertSystemEngine()

# Loads/saves rules to:
# C:\IntelliCV-AI\IntelliCV\SANDBOX\admin_portal\backend\data\rules\expert_rules.json
```

### For Data Manager

```python
from services.intellicv_data_manager import IntelliCVDataDirectoryManager

manager = IntelliCVDataDirectoryManager()

# Get CVs from ALL sources (ai_data_final + email_extracted)
all_cvs = manager.get_extracted_cv_list(source='all')

# Get CVs from SANDBOX ai_data_final only
ai_cvs = manager.get_extracted_cv_list(source='ai_data')

# Get CVs from email only
email_cvs = manager.get_extracted_cv_list(source='email')
```

---

## ✅ KEY CHANGES MADE

1. **Updated Primary AI Data Path**
   - Changed from: `IntelliCV-data/ai_data_final`
   - Changed to: `SANDBOX/admin_portal/ai_data_final`

2. **Added Backend Data Paths**
   - `backend/data/models/` - For trained models
   - `backend/data/rules/` - For expert system rules
   - `backend/data/feedback/` - For feedback loop data
   - `backend/logs/` - For backend logs

3. **Multi-Source CV Collection**
   - Can now pull CVs from multiple sources
   - `source='all'` - Both ai_data_final and email_extracted
   - `source='ai_data'` - Only SANDBOX ai_data_final
   - `source='email'` - Only email_extracted

4. **Enhanced Status Reporting**
   - Now tracks both email and AI data separately
   - Shows backend directory status
   - Combined statistics across all sources

---

## 🔍 VERIFICATION

### Check All Paths Are Correct

```powershell
cd C:\IntelliCV-AI\IntelliCV\SANDBOX\admin_portal
python -c "from services.intellicv_data_manager import IntelliCVDataDirectoryManager; mgr = IntelliCVDataDirectoryManager(); import json; print(json.dumps(mgr.get_real_data_stats(), indent=2))"
```

This will show:
- ✅ SANDBOX ai_data_final path
- ✅ Backend data paths
- ✅ Email extraction paths
- ✅ File counts from each source

---

## 📋 SUMMARY

**AI Backend Development:**
- ✅ Development in: `BACKEND-ADMIN-REORIENTATION/admin_portal/backend/`
- ✅ Production copy in: `SANDBOX/admin_portal/backend/`

**Training Data:**
- ✅ Primary source: `SANDBOX/admin_portal/ai_data_final/`
- ✅ Secondary source: `IntelliCV-data/email_extracted/`

**Backend AI Data:**
- ✅ Models: `SANDBOX/admin_portal/backend/data/models/`
- ✅ Rules: `SANDBOX/admin_portal/backend/data/rules/`
- ✅ Feedback: `SANDBOX/admin_portal/backend/data/feedback/`

**Data Manager:**
- ✅ Updated to use correct SANDBOX paths
- ✅ Supports multiple data sources
- ✅ Tracks all directories properly

---

**Status:** ✅ Data paths corrected and verified  
**Updated:** October 15, 2025
