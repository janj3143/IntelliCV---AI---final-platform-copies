# IntelliCV User Portal Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         INTELLICV COMPLETE SYSTEM                            │
└─────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────┐         ┌────────────────────────────────┐
│       ADMIN PORTAL             │         │       USER PORTAL              │
│    (Port 8501)                 │         │    (Port 8502)                 │
├────────────────────────────────┤         ├────────────────────────────────┤
│                                │         │                                │
│  Pages:                        │         │  Pages:                        │
│  ├─ 23_AI_Model_Training       │         │  ├─ 00_Home                   │
│  │   Review.py                 │         │  ├─ 01_Interview_Coach        │
│  │   • Train GLOBAL models     │         │  └─ 02_Career_Coach           │
│  │   • All 6 AI engines        │         │                                │
│  │   • Admin scenarios         │         │  Features:                     │
│  │   • System-wide training    │         │  • Personalized coaching       │
│  └─ Other admin pages...       │         │  • User-specific models        │
│                                │         │  • Progress tracking           │
└────────────┬───────────────────┘         └─────────────┬──────────────────┘
             │                                           │
             │ Creates/trains                            │ Uses/extends
             │ GLOBAL MODELS                             │ GLOBAL + USER MODELS
             │                                           │
             ▼                                           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          SHARED BACKEND                                      │
│                     (Root level directory)                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ai_engines/                                                                 │
│  ├─ model_trainer.py ◄────────────────┐                                     │
│  │   • TrainingScenario class         │                                     │
│  │   • ModelTrainer base class        │                                     │
│  │   • Used by ADMIN                  │                                     │
│  │                                    │                                     │
│  └─ user_model_trainer.py ◄───────────┼─────┐ NEW!                          │
│      • UserCoachingPreferences         │     │                              │
│      • UserInteraction                 │     │ Extends                      │
│      • UserModelTrainer ───────────────┘     │ ModelTrainer                 │
│        (extends ModelTrainer)                │                              │
│        • User ID scoping                     │                              │
│        • Incremental training                │                              │
│        • Model blending                      │                              │
│        • Privacy controls                    │                              │
│                                              │                              │
│  services/                                   │                              │
│  └─ unified_ai_engine.py                     │                              │
│      • 6 AI Engines:                         │                              │
│        ├─ Neural Network Engine              │                              │
│        ├─ Expert System Engine               │                              │
│        ├─ Bayesian Inference Engine ◄────────┤ Both portals                 │
│        ├─ Advanced NLP Engine                │ use all                      │
│        ├─ Fuzzy Logic Engine                 │ 6 engines                    │
│        └─ LLM Integration Engine             │                              │
│      • UnifiedIntelliCVAIEngine              │                              │
│      • Feedback Loop                         │                              │
│                                              │                              │
│  data/models/                                │                              │
│  ├─ global/                                  │                              │
│  │   ├─ global_interview_coach_v1.pkl ◄──────┤ Admin trains                 │
│  │   ├─ global_career_coach_v1.pkl           │ these models                 │
│  │   └─ ... (other global models)            │                              │
│  │                                           │                              │
│  └─ user_models/                             │                              │
│      ├─ demo_user_001/                       │                              │
│      │   ├─ models/                          │                              │
│      │   │   ├─ user_..._interview_coach.pkl │ User-specific                │
│      │   │   └─ user_..._career_coach.pkl    │ trained models               │
│      │   ├─ data/                            │                              │
│      │   ├─ scenarios.json                   │                              │
│      │   ├─ preferences.json ◄────────────────┤ User's settings              │
│      │   ├─ interactions.json                │ Interaction history          │
│      │   └─ progress.json                    │ Progress metrics             │
│      │                                       │                              │
│      ├─ user_002/                            │                              │
│      │   └─ ... (separate isolation)         │ Privacy: Each user           │
│      │                                       │ completely isolated          │
│      └─ user_003/                            │                              │
│          └─ ...                              │                              │
│                                              │                              │
└──────────────────────────────────────────────┴──────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                        MODEL BLENDING STRATEGY                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  User Maturity Levels:                                                       │
│                                                                              │
│  Beginner (< 10 interactions)                                                │
│  ├─ Personal Model: 30%  ┐                                                   │
│  └─ Global Model:   70%  ├──► Blended Prediction                             │
│                          │                                                   │
│  Learning (10-50 interactions)                                               │
│  ├─ Personal Model: 50%  │                                                   │
│  └─ Global Model:   50%  │                                                   │
│                          │                                                   │
│  Established (50-200 interactions)                                           │
│  ├─ Personal Model: 70%  │                                                   │
│  └─ Global Model:   30%  │                                                   │
│                          │                                                   │
│  Expert (200+ interactions)                                                  │
│  ├─ Personal Model: 90%  │                                                   │
│  └─ Global Model:   10%  ┘                                                   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                          USER JOURNEY FLOW                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. USER LOGS IN                                                             │
│     └─► user_id = "demo_user_001"                                            │
│                                                                              │
│  2. USER PORTAL LOADS                                                        │
│     └─► UserModelTrainer(user_id, inherit_global_models=True)               │
│         └─► Checks for existing user models                                 │
│             ├─ Found: Load user's trained models                             │
│             └─ Not found: Copy global models as baseline                     │
│                                                                              │
│  3. USER PRACTICES INTERVIEW                                                 │
│     ├─► Generate question (based on user's level)                            │
│     ├─► User writes answer                                                   │
│     ├─► AI analyzes answer:                                                  │
│     │   └─► Blend(user_model, global_model, adaptive_weights)                │
│     └─► Provide personalized feedback                                        │
│                                                                              │
│  4. USER RATES FEEDBACK                                                      │
│     └─► record_interaction(coach_type, input, response, feedback)            │
│         └─► Saved to user_models/{user_id}/interactions.json                 │
│                                                                              │
│  5. MODEL TRAINS INCREMENTALLY                                               │
│     └─► train_from_interaction(scenario_id, interaction)                     │
│         ├─► Load user's existing model                                       │
│         ├─► Update with new training data                                    │
│         ├─► Save updated model                                               │
│         └─► Update progress metrics                                          │
│                                                                              │
│  6. NEXT INTERACTION                                                         │
│     └─► More personalized (maturity level increases)                         │
│         └─► Cycle repeats, AI gets smarter                                   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                      DATA ISOLATION & PRIVACY                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐                     │
│  │   User A     │   │   User B     │   │   User C     │                     │
│  │              │   │              │   │              │                     │
│  │  Models ─────┼───│─► Isolated   │   │              │                     │
│  │  Data        │   │   No sharing │◄──┼─ Isolated    │                     │
│  │  Preferences │   │              │   │   No sharing │                     │
│  └──────────────┘   └──────────────┘   └──────────────┘                     │
│                                                                              │
│  Each user's directory:                                                      │
│  user_models/{user_id}/                                                      │
│  ├─ Separate models                                                          │
│  ├─ Separate training data                                                   │
│  ├─ Separate preferences                                                     │
│  ├─ Encrypted interactions                                                   │
│  └─ Export/delete controls                                                   │
│                                                                              │
│  Global models:                                                              │
│  models/global/                                                              │
│  ├─ Shared baseline for all users                                            │
│  └─ Trained by admin on aggregated patterns                                  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                        CODE REUSE ARCHITECTURE                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Admin Page 23 (23_AI_Model_Training_Review.py)                              │
│  ├─ TrainingScenario class ──────────────┐                                   │
│  ├─ ModelTrainer class ──────────────────┤                                   │
│  ├─ 6 AI engines integration ────────────┤                                   │
│  ├─ Feedback loop system ────────────────┤                                   │
│  └─ Model versioning ────────────────────┤                                   │
│                                          │                                   │
│                                          │ 90% Code Reuse                    │
│                                          ▼                                   │
│  User Portal (UserModelTrainer)                                              │
│  ├─ INHERITS: TrainingScenario ◄─────────┤                                   │
│  ├─ EXTENDS: ModelTrainer ◄──────────────┤                                   │
│  ├─ USES: 6 AI engines ◄─────────────────┤                                   │
│  ├─ USES: Feedback loop ◄────────────────┤                                   │
│  ├─ USES: Model versioning ◄─────────────┘                                   │
│  │                                                                           │
│  └─ ADDS 10%:                                                                │
│      ├─ User ID scoping                                                      │
│      ├─ Preference management                                                │
│      ├─ Incremental training                                                 │
│      ├─ Model blending logic                                                 │
│      └─ Privacy controls                                                     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                          FILE SUMMARY                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Created/Modified Files:                                                     │
│                                                                              │
│  1. shared_backend/ai_engines/user_model_trainer.py         [680 lines] NEW │
│     └─ Core personalization engine                                           │
│                                                                              │
│  2. user_portal/main.py                                     [60 lines]  NEW │
│     └─ Portal entry point                                                    │
│                                                                              │
│  3. user_portal/00_Home.py                                  [230 lines] NEW │
│     └─ Welcome dashboard                                                     │
│                                                                              │
│  4. user_portal/pages/01_Interview_Coach.py                 [565 lines] NEW │
│     └─ Personalized interview practice                                       │
│                                                                              │
│  5. user_portal/pages/02_Career_Coach.py                    [530 lines] NEW │
│     └─ Personalized career guidance                                          │
│                                                                              │
│  6. user_portal/launch_user_portal.ps1                      [85 lines]  NEW │
│     └─ Easy launcher script                                                  │
│                                                                              │
│  7. user_portal/README.md                                   [360 lines] NEW │
│     └─ Comprehensive documentation                                           │
│                                                                              │
│  8. USER_PORTAL_IMPLEMENTATION_COMPLETE.md                  [400 lines] NEW │
│     └─ Implementation summary                                                │
│                                                                              │
│  TOTAL: 8 files, ~2,910 lines of code + documentation                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                          LAUNCH COMMANDS                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Admin Portal (Port 8501):                                                   │
│  ─────────────────────────                                                   │
│  cd c:\IntelliCV-AI\IntelliCV\SANDBOX\admin_portal                           │
│  .\launch_admin_portal.ps1                                                   │
│                                                                              │
│  OR                                                                          │
│                                                                              │
│  streamlit run main.py --server.port 8501                                    │
│                                                                              │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                              │
│  User Portal (Port 8502):                                                    │
│  ────────────────────────                                                    │
│  cd c:\IntelliCV-AI\IntelliCV\SANDBOX\admin_portal\user_portal               │
│  .\launch_user_portal.ps1                                                    │
│                                                                              │
│  OR                                                                          │
│                                                                              │
│  streamlit run main.py --server.port 8502                                    │
│                                                                              │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                              │
│  Access URLs:                                                                │
│  ────────────                                                                │
│  Admin Portal:  http://localhost:8501                                        │
│  User Portal:   http://localhost:8502                                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

**Architecture Key Points:**

✅ **Separation of Concerns** - Admin trains global, users train personal  
✅ **Code Reuse** - 90% shared from admin Page 23  
✅ **Data Isolation** - Complete privacy per user  
✅ **Model Blending** - Adaptive personal + global  
✅ **Scalability** - Supports unlimited users  
✅ **Privacy** - Export, delete, encryption  

---

Created: October 15, 2025  
Status: ✅ Complete and Ready for Testing
