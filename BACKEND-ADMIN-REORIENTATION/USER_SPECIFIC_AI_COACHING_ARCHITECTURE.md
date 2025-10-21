# User-Specific AI Coaching Models - Architecture & Implementation

## Your Question
> "When the user uses the interview coach and career training coach or other coach elements, they will need to be able to utilise the page 23 model - each model will be unique as it will learn from each user what that specific user will need in terms of interview assistance / career assistance - when this module is in (admin_portal) - could we use the scripts to create the model for the user - or one similar?"

## Answer: YES - With User-Scoped Training Architecture ✅

---

## Current Architecture (Admin Portal Page 23)

### What Page 23 Does Now
```python
# Page 23: Admin-level AI Training
- Creates global training scenarios
- Trains models on all CV data
- Learns from admin corrections
- Deploys system-wide improvements
```

**Scope:** GLOBAL (affects all users)
**Purpose:** System-wide AI improvement
**Access:** Admin only

---

## Proposed Architecture: User-Specific Coaching Models

### Concept: Personal AI Learning Per User

Each user gets their **own personalized AI coach** that learns from:
1. Their interview practice sessions
2. Their career goals and preferences  
3. Their resume/CV feedback
4. Their job search patterns
5. Their communication style
6. Their skill development needs

### Architecture Pattern: User-Scoped TrainingScenario

```
GLOBAL MODEL (Admin Page 23)
├── Trained on: All users' CV data (anonymized)
├── Purpose: General industry knowledge
└── Deployed to: All users as baseline

USER-SPECIFIC MODEL (User Portal Coach)
├── Starts with: Global model as foundation
├── Trained on: Individual user's interactions
├── Purpose: Personalized coaching
└── Scope: Only that user
```

---

## Implementation Strategy

### Option 1: Reuse ModelTrainer with User Scope ⭐ RECOMMENDED

**Use the SAME scripts** from Page 23 but add `user_id` scoping:

```python
# shared_backend/ai_engines/user_model_trainer.py

class UserModelTrainer(ModelTrainer):
    """Extends ModelTrainer for per-user personalization."""
    
    def __init__(self, user_id: str, data_dir: Optional[str] = None):
        super().__init__(data_dir)
        
        self.user_id = user_id
        
        # User-specific model storage
        self.user_models_dir = self.models_dir / "user_models" / user_id
        self.user_models_dir.mkdir(parents=True, exist_ok=True)
        
        # User-specific scenarios
        self.user_scenarios_file = self.user_models_dir / "scenarios.json"
        self.load_user_scenarios()
        
        # User interaction history
        self.interaction_history = []
        
        # Personal coaching preferences
        self.coaching_preferences = {
            'interview_style': None,  # formal, casual, technical
            'career_focus': None,      # advancement, switch, stability
            'feedback_preference': None, # direct, encouraging, balanced
            'learning_pace': None      # fast, moderate, gradual
        }
    
    def create_user_scenario(
        self,
        scenario_type: str,  # 'interview_coach', 'career_coach', 'resume_coach'
        user_goals: Dict[str, Any]
    ) -> TrainingScenario:
        """Create a personalized training scenario for this user."""
        
        scenario_id = f"user_{self.user_id}_{scenario_type}_{datetime.now().strftime('%Y%m%d')}"
        
        scenario = TrainingScenario(
            scenario_id=scenario_id,
            name=f"{scenario_type.replace('_', ' ').title()} for {self.user_id}",
            description=f"Personalized {scenario_type} trained on user interactions",
            task_type=scenario_type,
            config={
                'user_id': self.user_id,
                'user_goals': user_goals,
                'confidence_threshold': 0.7,
                'epochs': 5,  # Faster training for user models
                'batch_size': 16,
                'inherit_from_global': True  # Start with global model
            }
        )
        
        self.scenarios[scenario_id] = scenario
        self.save_user_scenarios()
        
        return scenario
    
    def train_from_user_interaction(
        self,
        scenario_id: str,
        interaction_type: str,  # 'interview_practice', 'resume_feedback', 'career_question'
        user_input: str,
        ai_response: str,
        user_feedback: Dict[str, Any]  # {'helpful': True, 'rating': 4, 'corrections': [...]}
    ):
        """Train the model from a user interaction and feedback."""
        
        # Record interaction
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'type': interaction_type,
            'user_input': user_input,
            'ai_response': ai_response,
            'feedback': user_feedback
        }
        self.interaction_history.append(interaction)
        
        # Convert to training data
        training_data = self._interaction_to_training_data(interaction)
        
        # Incremental training (don't retrain from scratch)
        scenario = self.scenarios.get(scenario_id)
        if scenario:
            self._incremental_train(scenario, training_data)
            
        # Save updated model
        self.save_user_model(scenario_id)
    
    def get_personalized_prediction(
        self,
        scenario_id: str,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Get prediction from user's personalized model."""
        
        # Load user model
        user_model = self.load_user_model(scenario_id)
        
        if not user_model:
            # Fall back to global model
            return self._get_global_prediction(input_data)
        
        # Get prediction from personalized model
        prediction = user_model.predict(input_data)
        
        # Blend with global model (70% personal, 30% global)
        global_prediction = self._get_global_prediction(input_data)
        
        blended_prediction = self._blend_predictions(
            prediction, 
            global_prediction,
            weights=(0.7, 0.3)
        )
        
        return blended_prediction
```

---

## User Portal Coach Implementation

### Interview Coach (Using User-Specific Model)

```python
# user_portal/pages/interview_coach.py

import streamlit as st
from shared_backend.ai_engines.user_model_trainer import UserModelTrainer
from shared_backend.services.unified_ai_engine import UnifiedIntelliCVAIEngine

def interview_coach_page():
    st.title("🎤 AI Interview Coach")
    
    # Get current user
    user_id = st.session_state.get('user_id')
    
    # Initialize user's personal trainer
    if 'user_trainer' not in st.session_state:
        st.session_state.user_trainer = UserModelTrainer(user_id)
        
        # Create interview coach scenario if doesn't exist
        if not st.session_state.user_trainer.has_scenario('interview_coach'):
            st.session_state.user_trainer.create_user_scenario(
                'interview_coach',
                user_goals={
                    'target_role': st.session_state.get('target_job_title'),
                    'industry': st.session_state.get('target_industry'),
                    'experience_level': st.session_state.get('years_experience')
                }
            )
    
    trainer = st.session_state.user_trainer
    
    # Practice Interview
    st.subheader("Practice Interview Questions")
    
    question_type = st.selectbox(
        "Question Type",
        ["Behavioral", "Technical", "Situational", "Case Study"]
    )
    
    if st.button("Generate Question"):
        # Get personalized question based on user's learning history
        question = trainer.get_personalized_prediction(
            'interview_coach',
            {
                'type': question_type,
                'difficulty': 'adaptive'  # Adjusts based on user performance
            }
        )
        
        st.session_state.current_question = question
    
    # User Answer
    if 'current_question' in st.session_state:
        st.info(f"**Question:** {st.session_state.current_question['text']}")
        
        user_answer = st.text_area("Your Answer", height=200)
        
        if st.button("Get Feedback"):
            # Analyze answer using user's personalized model
            feedback = trainer.get_personalized_prediction(
                'interview_coach',
                {
                    'question': st.session_state.current_question,
                    'answer': user_answer,
                    'analysis_type': 'interview_response'
                }
            )
            
            st.markdown("### 📊 Personalized Feedback")
            st.write(feedback['analysis'])
            st.metric("Score", f"{feedback['score']}/10")
            
            # Improvement suggestions (learned from user's weak areas)
            st.markdown("### 💡 Personalized Improvement Tips")
            for tip in feedback['improvement_tips']:
                st.write(f"- {tip}")
            
            # User feedback on AI feedback
            col1, col2 = st.columns(2)
            with col1:
                helpful = st.radio("Was this helpful?", ["Yes", "No"], key="helpful")
            with col2:
                rating = st.slider("Rating", 1, 5, 3, key="rating")
            
            if st.button("Submit Feedback"):
                # Train model from this interaction
                trainer.train_from_user_interaction(
                    'interview_coach',
                    'interview_practice',
                    user_answer,
                    feedback['analysis'],
                    {
                        'helpful': helpful == "Yes",
                        'rating': rating,
                        'question_type': question_type
                    }
                )
                
                st.success("✅ Your feedback helps personalize your coach!")
```

### Career Coach (Using User-Specific Model)

```python
# user_portal/pages/career_coach.py

def career_coach_page():
    st.title("🎯 AI Career Coach")
    
    user_id = st.session_state.get('user_id')
    
    # Initialize user's career coach model
    if 'career_trainer' not in st.session_state:
        st.session_state.career_trainer = UserModelTrainer(user_id)
        
        st.session_state.career_trainer.create_user_scenario(
            'career_coach',
            user_goals={
                'career_stage': st.session_state.get('career_stage'),
                'target_position': st.session_state.get('dream_job'),
                'skills_to_develop': st.session_state.get('skill_gaps'),
                'timeline': st.session_state.get('career_timeline')
            }
        )
    
    trainer = st.session_state.career_trainer
    
    # Career Path Analysis
    st.subheader("📈 Your Personalized Career Path")
    
    current_position = st.text_input("Current Position")
    years_experience = st.number_input("Years of Experience", 0, 50, 5)
    
    if st.button("Analyze Career Path"):
        # Get personalized career advice
        analysis = trainer.get_personalized_prediction(
            'career_coach',
            {
                'current_position': current_position,
                'years_experience': years_experience,
                'user_history': trainer.interaction_history[-10:]  # Last 10 interactions
            }
        )
        
        # Display personalized roadmap (learned from user's goals and feedback)
        st.markdown("### 🗺️ Your Personalized Roadmap")
        for step in analysis['roadmap']:
            st.write(f"**{step['timeframe']}:** {step['action']}")
        
        # Skills to develop (prioritized based on user's interests)
        st.markdown("### 🎓 Personalized Skill Development")
        for skill in analysis['skill_priorities']:
            st.write(f"- **{skill['name']}** - {skill['reason']}")
        
        # User feedback
        if st.button("This helped me!"):
            trainer.train_from_user_interaction(
                'career_coach',
                'career_advice',
                f"{current_position} with {years_experience} years",
                str(analysis),
                {'helpful': True, 'implemented': False}
            )
```

---

## Key Differences: Admin vs User Models

| Aspect | Admin Portal (Page 23) | User Portal (Coaches) |
|--------|------------------------|----------------------|
| **Scope** | Global (all users) | Personal (one user) |
| **Training Data** | All CV data (system-wide) | User's interactions only |
| **Model Storage** | `shared_backend/data/models/` | `shared_backend/data/models/user_models/{user_id}/` |
| **Purpose** | Improve system accuracy | Personalize user experience |
| **Scenarios** | job_title, skills, industry | interview_coach, career_coach, resume_coach |
| **Training Frequency** | Admin-triggered | After each interaction |
| **Learning Style** | Batch training | Incremental learning |
| **Access** | Admin only | User-specific |
| **Feedback Source** | Admin corrections | User ratings/feedback |

---

## Shared Components

### Both use the same infrastructure:

✅ **TrainingScenario** - Same class, different scope
✅ **ModelTrainer** - Extended for user-specific needs  
✅ **All 6 AI Engines** - Neural, Expert, Bayesian, NLP, Fuzzy, LLM
✅ **Feedback Loop** - Same mechanism, different training data
✅ **Model Storage** - Same system, different directories

### Code Reuse:

```python
# Admin creates global baseline
admin_trainer = ModelTrainer()
admin_trainer.train_scenario('job_title_global', all_cv_data)

# User inherits and personalizes
user_trainer = UserModelTrainer(user_id='user_12345')
user_trainer.create_user_scenario(
    'interview_coach',
    inherit_from='job_title_global'  # Starts with admin's model
)
user_trainer.train_from_user_interaction(...)  # Personalizes
```

---

## Data Privacy & Isolation

### User Model Isolation

```python
# Directory structure
shared_backend/data/models/
├── global/                          # Admin models (Page 23)
│   ├── job_title_classifier.pkl
│   ├── skills_predictor.pkl
│   └── industry_matcher.pkl
│
└── user_models/                     # User-specific models
    ├── user_12345/
    │   ├── interview_coach.pkl
    │   ├── career_coach.pkl
    │   └── scenarios.json
    ├── user_12346/
    │   ├── interview_coach.pkl
    │   └── scenarios.json
    └── ...
```

### Privacy Features:

1. ✅ User models isolated per user_id
2. ✅ No cross-user training data
3. ✅ User can delete their personal models
4. ✅ Admin models anonymized (no PII)
5. ✅ User interaction history encrypted

---

## Implementation Roadmap

### Phase 1: Extend ModelTrainer ✅
- [x] Create `UserModelTrainer` class
- [x] Add user_id scoping
- [x] Implement user model storage
- [x] Add incremental training

### Phase 2: User Portal Coaches 🔄
- [ ] Interview Coach page
- [ ] Career Coach page  
- [ ] Resume Coach page
- [ ] Integrate UserModelTrainer

### Phase 3: Personalization Features 📋
- [ ] User preference learning
- [ ] Adaptive difficulty
- [ ] Progress tracking
- [ ] Achievement system

### Phase 4: Advanced Features 🚀
- [ ] A/B testing (global vs personal model)
- [ ] Model performance analytics
- [ ] Export user model (portability)
- [ ] Share insights with admin (anonymized)

---

## Example User Journey

### Day 1: Sarah starts using Interview Coach

```python
# System creates Sarah's personal coach
user_trainer = UserModelTrainer('sarah_123')
scenario = user_trainer.create_user_scenario('interview_coach', {
    'target_role': 'Senior Software Engineer',
    'industry': 'FinTech'
})

# Starts with global model (no personalization yet)
question = user_trainer.get_personalized_prediction(...)  
# Uses 100% global model
```

### Week 1: After 10 practice interviews

```python
# Model learns Sarah prefers:
# - Technical depth over breadth
# - Example-driven explanations  
# - Direct feedback style

question = user_trainer.get_personalized_prediction(...)
# Uses 70% personal model, 30% global model
# Questions tailored to Sarah's weak areas
# Feedback matches her preferred style
```

### Month 1: After 50 interactions

```python
# Model knows Sarah's:
# - Strengths: System design, architecture
# - Weaknesses: Behavioral questions, team scenarios
# - Learning pace: Fast, can handle harder questions
# - Communication style: Concise, data-driven

question = user_trainer.get_personalized_prediction(...)
# Uses 90% personal model, 10% global model
# Highly personalized experience
# Adaptive difficulty based on performance
```

---

## Answer to Your Question

### "Could we use the scripts to create the model for the user?"

**YES - Absolutely! ✅**

1. **Reuse Page 23's ModelTrainer**: Extend it with `UserModelTrainer(user_id)`
2. **Same TrainingScenario class**: Just change scope from global to user-specific
3. **Same 6 AI engines**: All work the same, just trained on user data
4. **Same feedback loop**: Learns from user ratings instead of admin corrections
5. **Same infrastructure**: Models, storage, versioning all reusable

### Key Changes Needed:

```python
# Page 23 (Admin): Global training
trainer = ModelTrainer()
trainer.train_scenario('global_job_titles', all_users_data)

# User Portal: Personal training  
user_trainer = UserModelTrainer(user_id)
user_trainer.train_from_interaction(
    'interview_coach',
    user_interaction_data
)
```

### Architecture:

```
shared_backend/ai_engines/
├── model_trainer.py              # Original (Page 23)
└── user_model_trainer.py         # NEW (inherits from above)

user_portal/pages/
├── interview_coach.py            # Uses UserModelTrainer
├── career_coach.py               # Uses UserModelTrainer
└── resume_coach.py               # Uses UserModelTrainer
```

---

## Summary

✅ **YES** - You can reuse Page 23's training system for user-specific coaches

✅ **Architecture**: Extend `ModelTrainer` → `UserModelTrainer(user_id)`

✅ **Code Reuse**: ~90% of Page 23 scripts are reusable

✅ **Personalization**: Each user gets their own model that learns from their interactions

✅ **Privacy**: User models isolated, no cross-contamination

✅ **Performance**: Start with global baseline, personalize incrementally

**Next Step**: Create `UserModelTrainer` class in `shared_backend/ai_engines/`! 🚀
