"""
User-Specific Model Training System for IntelliCV

This extends the admin ModelTrainer to provide personalized AI coaching
for individual users. Each user gets their own AI models that learn from
their specific interactions, preferences, and feedback.

Use Cases:
- Interview Coach: Personalized interview practice and feedback
- Career Coach: Tailored career path recommendations
- Resume Coach: Custom resume improvement suggestions
- Skill Coach: Adaptive learning based on user progress

Key Features:
- Inherits from global admin models (Page 23)
- Trains incrementally from user interactions
- Isolated per-user storage for privacy
- Blends personal and global predictions
- Adaptive difficulty and pacing

Created: October 15, 2025
Part of: User Portal Personalization System
"""

import os
import sys
import json
import logging
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path
import hashlib
import pickle

# Import base ModelTrainer from admin system
from model_trainer import ModelTrainer, TrainingScenario


class UserCoachingPreferences:
    """Stores user's personalized coaching preferences."""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        
        # Interview coaching preferences
        self.interview_style = 'balanced'  # formal, casual, technical, balanced
        self.feedback_detail = 'moderate'  # brief, moderate, detailed
        self.difficulty_level = 'adaptive' # easy, moderate, hard, adaptive
        
        # Career coaching preferences
        self.career_focus = []  # advancement, switch, stability, learning
        self.industry_interests = []
        self.timeline_preference = 'flexible'  # urgent, planned, flexible
        
        # Learning preferences
        self.learning_pace = 'moderate'  # fast, moderate, gradual
        self.content_style = 'example_driven'  # theoretical, example_driven, mixed
        self.feedback_tone = 'encouraging'  # direct, encouraging, balanced
        
        # Communication preferences
        self.response_length = 'moderate'  # concise, moderate, comprehensive
        self.technical_depth = 'moderate'  # surface, moderate, deep
        
        # Personal tracking
        self.strong_areas = []
        self.improvement_areas = []
        self.completed_goals = []
        self.current_goals = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            'user_id': self.user_id,
            'interview_style': self.interview_style,
            'feedback_detail': self.feedback_detail,
            'difficulty_level': self.difficulty_level,
            'career_focus': self.career_focus,
            'industry_interests': self.industry_interests,
            'timeline_preference': self.timeline_preference,
            'learning_pace': self.learning_pace,
            'content_style': self.content_style,
            'feedback_tone': self.feedback_tone,
            'response_length': self.response_length,
            'technical_depth': self.technical_depth,
            'strong_areas': self.strong_areas,
            'improvement_areas': self.improvement_areas,
            'completed_goals': self.completed_goals,
            'current_goals': self.current_goals
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserCoachingPreferences':
        """Create from dictionary."""
        prefs = cls(data['user_id'])
        for key, value in data.items():
            if hasattr(prefs, key):
                setattr(prefs, key, value)
        return prefs


class UserInteraction:
    """Represents a single user interaction with the AI coach."""
    
    def __init__(
        self,
        user_id: str,
        coach_type: str,  # interview, career, resume, skill
        interaction_type: str,  # practice, question, feedback, review
        user_input: Dict[str, Any],
        ai_response: Dict[str, Any],
        user_feedback: Optional[Dict[str, Any]] = None
    ):
        self.user_id = user_id
        self.coach_type = coach_type
        self.interaction_type = interaction_type
        self.user_input = user_input
        self.ai_response = ai_response
        self.user_feedback = user_feedback or {}
        self.timestamp = datetime.now().isoformat()
        
        # Performance metrics
        self.response_quality_score = None
        self.user_satisfaction = None
        self.learning_impact = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            'user_id': self.user_id,
            'coach_type': self.coach_type,
            'interaction_type': self.interaction_type,
            'user_input': self.user_input,
            'ai_response': self.ai_response,
            'user_feedback': self.user_feedback,
            'timestamp': self.timestamp,
            'response_quality_score': self.response_quality_score,
            'user_satisfaction': self.user_satisfaction,
            'learning_impact': self.learning_impact
        }


class UserModelTrainer(ModelTrainer):
    """
    Extends ModelTrainer for user-specific personalization.
    
    Each user gets their own AI models that:
    - Start with global admin models as baseline
    - Train incrementally from user interactions
    - Learn user preferences and patterns
    - Adapt difficulty and content to user
    - Provide personalized coaching
    
    Privacy: All user data isolated per user_id
    """
    
    def __init__(
        self,
        user_id: str,
        data_dir: Optional[str] = None,
        inherit_global_models: bool = True
    ):
        """
        Initialize User Model Trainer.
        
        Args:
            user_id: Unique identifier for the user
            data_dir: Optional custom data directory
            inherit_global_models: Whether to start with global admin models
        """
        # Initialize base ModelTrainer
        super().__init__(data_dir=data_dir)
        
        self.user_id = user_id
        self.inherit_global_models = inherit_global_models
        
        # User-specific directories
        self.user_base_dir = self.models_dir / "user_models" / user_id
        self.user_base_dir.mkdir(parents=True, exist_ok=True)
        
        self.user_models_dir = self.user_base_dir / "models"
        self.user_models_dir.mkdir(exist_ok=True)
        
        self.user_data_dir = self.user_base_dir / "data"
        self.user_data_dir.mkdir(exist_ok=True)
        
        # User-specific files
        self.user_scenarios_file = self.user_base_dir / "scenarios.json"
        self.user_preferences_file = self.user_base_dir / "preferences.json"
        self.user_interactions_file = self.user_base_dir / "interactions.json"
        self.user_progress_file = self.user_base_dir / "progress.json"
        
        # Load user data
        self.preferences = self.load_preferences()
        self.interaction_history = self.load_interactions()
        self.progress_tracker = self.load_progress()
        
        # Load user scenarios (separate from global)
        self.load_user_scenarios()
        
        # Model blending weights (personal vs global)
        self.blending_weights = {
            'initial': (0.3, 0.7),      # 30% personal, 70% global (new user)
            'learning': (0.5, 0.5),     # 50/50 after some interactions
            'established': (0.7, 0.3),  # 70% personal, 30% global (experienced user)
            'expert': (0.9, 0.1)        # 90% personal, 10% global (lots of data)
        }
        
        self.logger.info(f"User Model Trainer initialized for user: {user_id}")
    
    def load_preferences(self) -> UserCoachingPreferences:
        """Load user's coaching preferences."""
        if self.user_preferences_file.exists():
            with open(self.user_preferences_file, 'r') as f:
                data = json.load(f)
                return UserCoachingPreferences.from_dict(data)
        else:
            # Create default preferences
            return UserCoachingPreferences(self.user_id)
    
    def save_preferences(self):
        """Save user's coaching preferences."""
        with open(self.user_preferences_file, 'w') as f:
            json.dump(self.preferences.to_dict(), f, indent=2)
    
    def load_interactions(self) -> List[UserInteraction]:
        """Load user's interaction history."""
        if self.user_interactions_file.exists():
            with open(self.user_interactions_file, 'r') as f:
                data = json.load(f)
                return [UserInteraction(**item) for item in data]
        return []
    
    def save_interactions(self):
        """Save user's interaction history."""
        with open(self.user_interactions_file, 'w') as f:
            json.dump([i.to_dict() for i in self.interaction_history], f, indent=2)
    
    def load_progress(self) -> Dict[str, Any]:
        """Load user's progress tracking data."""
        if self.user_progress_file.exists():
            with open(self.user_progress_file, 'r') as f:
                return json.load(f)
        return {
            'total_interactions': 0,
            'practice_sessions': 0,
            'skills_improved': [],
            'achievements': [],
            'performance_history': []
        }
    
    def save_progress(self):
        """Save user's progress tracking data."""
        with open(self.user_progress_file, 'w') as f:
            json.dump(self.progress_tracker, f, indent=2)
    
    def load_user_scenarios(self):
        """Load user-specific training scenarios."""
        if self.user_scenarios_file.exists():
            with open(self.user_scenarios_file, 'r') as f:
                data = json.load(f)
                for scenario_id, scenario_data in data.items():
                    self.scenarios[scenario_id] = TrainingScenario(
                        scenario_id=scenario_data['scenario_id'],
                        name=scenario_data['name'],
                        description=scenario_data['description'],
                        task_type=scenario_data['task_type'],
                        config=scenario_data['config']
                    )
                    # Restore state
                    scenario = self.scenarios[scenario_id]
                    scenario.trained_at = scenario_data.get('trained_at')
                    scenario.model_version = scenario_data.get('model_version')
                    scenario.performance_metrics = scenario_data.get('performance_metrics', {})
                    scenario.status = scenario_data.get('status', 'created')
    
    def save_user_scenarios(self):
        """Save user-specific training scenarios."""
        data = {sid: s.to_dict() for sid, s in self.scenarios.items()}
        with open(self.user_scenarios_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def create_coaching_scenario(
        self,
        coach_type: str,  # 'interview_coach', 'career_coach', 'resume_coach'
        user_goals: Dict[str, Any],
        inherit_from_global: Optional[str] = None
    ) -> TrainingScenario:
        """
        Create a personalized coaching scenario for this user.
        
        Args:
            coach_type: Type of coaching (interview, career, resume, skill)
            user_goals: User's specific goals for this coaching type
            inherit_from_global: Global scenario ID to inherit from (optional)
        
        Returns:
            TrainingScenario configured for user's needs
        """
        scenario_id = f"user_{self.user_id}_{coach_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        scenario = TrainingScenario(
            scenario_id=scenario_id,
            name=f"{coach_type.replace('_', ' ').title()} for User {self.user_id}",
            description=f"Personalized {coach_type} trained on user's interactions and preferences",
            task_type=coach_type,
            config={
                'user_id': self.user_id,
                'user_goals': user_goals,
                'inherit_from_global': inherit_from_global,
                'confidence_threshold': 0.7,
                'epochs': 5,  # Faster incremental training
                'batch_size': 16,
                'learning_rate': 0.001,
                'personalization_enabled': True,
                'adaptive_difficulty': True,
                'user_preferences': self.preferences.to_dict()
            }
        )
        
        self.scenarios[scenario_id] = scenario
        self.save_user_scenarios()
        
        # If inheriting from global, copy global model as starting point
        if inherit_from_global and self.inherit_global_models:
            self._inherit_global_model(scenario, inherit_from_global)
        
        self.logger.info(f"Created coaching scenario {scenario_id} for user {self.user_id}")
        
        return scenario
    
    def _inherit_global_model(self, user_scenario: TrainingScenario, global_scenario_id: str):
        """Copy global admin model as starting point for user model."""
        # Path to global model
        global_model_path = self.models_dir / "global" / f"{global_scenario_id}.pkl"
        
        if global_model_path.exists():
            # Copy to user's model directory
            user_model_path = self.user_models_dir / f"{user_scenario.scenario_id}.pkl"
            
            import shutil
            shutil.copy(global_model_path, user_model_path)
            
            user_scenario.model_version = "inherited_from_global_v1"
            user_scenario.status = "initialized"
            
            self.logger.info(f"Inherited global model {global_scenario_id} for user {self.user_id}")
        else:
            self.logger.warning(f"Global model {global_scenario_id} not found, starting fresh")
    
    def record_interaction(
        self,
        coach_type: str,
        interaction_type: str,
        user_input: Dict[str, Any],
        ai_response: Dict[str, Any],
        user_feedback: Optional[Dict[str, Any]] = None
    ) -> UserInteraction:
        """
        Record a user interaction with the AI coach.
        
        Args:
            coach_type: Type of coaching session
            interaction_type: Type of interaction
            user_input: What the user provided
            ai_response: What the AI responded with
            user_feedback: User's feedback on the AI response (optional)
        
        Returns:
            UserInteraction object
        """
        interaction = UserInteraction(
            user_id=self.user_id,
            coach_type=coach_type,
            interaction_type=interaction_type,
            user_input=user_input,
            ai_response=ai_response,
            user_feedback=user_feedback
        )
        
        self.interaction_history.append(interaction)
        self.save_interactions()
        
        # Update progress
        self.progress_tracker['total_interactions'] += 1
        if interaction_type == 'practice':
            self.progress_tracker['practice_sessions'] += 1
        
        self.save_progress()
        
        return interaction
    
    def train_from_interaction(
        self,
        scenario_id: str,
        interaction: UserInteraction,
        incremental: bool = True
    ):
        """
        Train the user's model from a recorded interaction.
        
        Args:
            scenario_id: The coaching scenario to train
            interaction: The user interaction containing training data
            incremental: Whether to do incremental training (True) or full retrain (False)
        """
        scenario = self.scenarios.get(scenario_id)
        
        if not scenario:
            self.logger.error(f"Scenario {scenario_id} not found for user {self.user_id}")
            return
        
        # Convert interaction to training data format
        training_data = self._interaction_to_training_data(interaction)
        
        if not training_data:
            self.logger.warning(f"No training data extracted from interaction")
            return
        
        # Perform incremental training (don't retrain from scratch)
        if incremental:
            self._incremental_train(scenario, training_data)
        else:
            # Full retrain with all historical data
            all_training_data = [
                self._interaction_to_training_data(i)
                for i in self.interaction_history
                if i.coach_type == scenario.task_type
            ]
            self._full_retrain(scenario, all_training_data)
        
        # Save updated model
        self._save_user_model(scenario)
        
        self.logger.info(f"Trained user model {scenario_id} from interaction")
    
    def _interaction_to_training_data(self, interaction: UserInteraction) -> Optional[Dict[str, Any]]:
        """
        Convert a user interaction into training data format.
        
        This extracts the relevant information from the interaction
        and formats it for model training.
        """
        if not interaction.user_feedback:
            return None  # Can't train without feedback
        
        return {
            'input': interaction.user_input,
            'expected_output': interaction.ai_response,
            'correction': interaction.user_feedback.get('corrections', []),
            'quality_score': interaction.user_feedback.get('rating', 3),
            'helpful': interaction.user_feedback.get('helpful', True),
            'timestamp': interaction.timestamp
        }
    
    def _incremental_train(self, scenario: TrainingScenario, new_data: Dict[str, Any]):
        """
        Perform incremental training on user's model.
        
        This updates the model with new data without full retraining,
        which is faster and better for continuous learning.
        """
        # Load existing user model
        model = self._load_user_model(scenario.scenario_id)
        
        if model is None:
            self.logger.warning(f"No existing model found, creating new one")
            model = self._initialize_new_model(scenario)
        
        # Update model with new training data
        # (Implementation depends on model type - neural, bayesian, etc.)
        if scenario.task_type in ['interview_coach', 'career_coach']:
            model = self._update_coaching_model(model, new_data, scenario.task_type)
        
        # Update scenario metadata
        scenario.trained_at = datetime.now().isoformat()
        scenario.status = 'trained'
        
        self.save_user_scenarios()
    
    def _full_retrain(self, scenario: TrainingScenario, all_data: List[Dict[str, Any]]):
        """Full model retraining with all historical data."""
        # Create fresh model
        model = self._initialize_new_model(scenario)
        
        # Train on all data
        for data_point in all_data:
            if data_point:
                model = self._update_coaching_model(model, data_point, scenario.task_type)
        
        # Update scenario
        scenario.trained_at = datetime.now().isoformat()
        scenario.model_version = f"v{len(all_data)}"
        scenario.status = 'trained'
        
        self.save_user_scenarios()
    
    def _initialize_new_model(self, scenario: TrainingScenario):
        """Initialize a new model for the scenario."""
        # Placeholder - actual implementation depends on model type
        return {
            'type': scenario.task_type,
            'created_at': datetime.now().isoformat(),
            'weights': {},
            'patterns': [],
            'user_preferences': self.preferences.to_dict()
        }
    
    def _update_coaching_model(self, model, training_data: Dict[str, Any], coach_type: str):
        """Update the coaching model with new training data."""
        # Placeholder - actual implementation depends on model architecture
        # This would integrate with the 6 AI engines (Neural, Bayesian, NLP, etc.)
        
        if 'patterns' not in model:
            model['patterns'] = []
        
        model['patterns'].append({
            'input_pattern': training_data['input'],
            'output_pattern': training_data['expected_output'],
            'quality': training_data['quality_score'],
            'timestamp': training_data['timestamp']
        })
        
        return model
    
    def _load_user_model(self, scenario_id: str):
        """Load user's trained model from disk."""
        model_path = self.user_models_dir / f"{scenario_id}.pkl"
        
        if model_path.exists():
            with open(model_path, 'rb') as f:
                return pickle.load(f)
        return None
    
    def _save_user_model(self, scenario: TrainingScenario):
        """Save user's trained model to disk."""
        model_path = self.user_models_dir / f"{scenario.scenario_id}.pkl"
        
        # Get model from scenario (placeholder - actual model would be stored differently)
        model = self._load_user_model(scenario.scenario_id)
        
        if model:
            with open(model_path, 'wb') as f:
                pickle.dump(model, f)
    
    def get_personalized_prediction(
        self,
        scenario_id: str,
        input_data: Dict[str, Any],
        blend_with_global: bool = True
    ) -> Dict[str, Any]:
        """
        Get prediction from user's personalized model.
        
        Args:
            scenario_id: User's coaching scenario ID
            input_data: Input data for prediction
            blend_with_global: Whether to blend with global model predictions
        
        Returns:
            Prediction tailored to user's learning patterns and preferences
        """
        # Load user's model
        user_model = self._load_user_model(scenario_id)
        
        if not user_model:
            # Fall back to global model if user model doesn't exist
            return self._get_global_prediction(input_data)
        
        # Get prediction from user's personalized model
        user_prediction = self._predict_from_model(user_model, input_data)
        
        # Optionally blend with global model for robustness
        if blend_with_global:
            global_prediction = self._get_global_prediction(input_data)
            
            # Determine blending weights based on user experience
            weights = self._get_blending_weights()
            
            blended_prediction = self._blend_predictions(
                user_prediction,
                global_prediction,
                weights
            )
            
            return blended_prediction
        
        return user_prediction
    
    def _get_blending_weights(self) -> Tuple[float, float]:
        """
        Determine how much to weight personal vs global model.
        
        Returns:
            (personal_weight, global_weight) tuple
        """
        interaction_count = len(self.interaction_history)
        
        if interaction_count < 10:
            return self.blending_weights['initial']  # New user, trust global more
        elif interaction_count < 50:
            return self.blending_weights['learning']  # Learning user, 50/50
        elif interaction_count < 200:
            return self.blending_weights['established']  # Established user, trust personal more
        else:
            return self.blending_weights['expert']  # Expert user, mostly personal
    
    def _predict_from_model(self, model, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Make prediction using the model."""
        # Placeholder - actual implementation would use the 6 AI engines
        return {
            'prediction': 'Sample personalized response',
            'confidence': 0.85,
            'explanation': 'Based on your previous interactions...',
            'personalized': True
        }
    
    def _get_global_prediction(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get prediction from global admin model."""
        # Placeholder - would call global ModelTrainer
        return {
            'prediction': 'Sample global response',
            'confidence': 0.75,
            'explanation': 'Based on general patterns...',
            'personalized': False
        }
    
    def _blend_predictions(
        self,
        user_pred: Dict[str, Any],
        global_pred: Dict[str, Any],
        weights: Tuple[float, float]
    ) -> Dict[str, Any]:
        """Blend user and global predictions with given weights."""
        user_weight, global_weight = weights
        
        blended_confidence = (
            user_pred['confidence'] * user_weight +
            global_pred['confidence'] * global_weight
        )
        
        return {
            'prediction': user_pred['prediction'],  # Prefer user's prediction
            'confidence': blended_confidence,
            'explanation': f"{user_pred['explanation']} (Personalized: {user_weight*100:.0f}%)",
            'personalized': True,
            'blend_ratio': f"{user_weight:.1f}/{global_weight:.1f}"
        }
    
    def get_user_statistics(self) -> Dict[str, Any]:
        """Get statistics about user's learning progress."""
        return {
            'user_id': self.user_id,
            'total_interactions': len(self.interaction_history),
            'coaching_scenarios': len(self.scenarios),
            'practice_sessions': self.progress_tracker['practice_sessions'],
            'skills_improved': self.progress_tracker['skills_improved'],
            'achievements': self.progress_tracker['achievements'],
            'preferences': self.preferences.to_dict(),
            'model_maturity': self._get_model_maturity_level()
        }
    
    def _get_model_maturity_level(self) -> str:
        """Determine how mature/trained the user's models are."""
        interaction_count = len(self.interaction_history)
        
        if interaction_count < 10:
            return "beginner"
        elif interaction_count < 50:
            return "learning"
        elif interaction_count < 200:
            return "established"
        else:
            return "expert"
    
    def export_user_data(self, export_path: Optional[str] = None) -> str:
        """
        Export all user data for portability or backup.
        
        Args:
            export_path: Optional custom export path
        
        Returns:
            Path to exported data file
        """
        if not export_path:
            export_path = self.user_base_dir / f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        export_data = {
            'user_id': self.user_id,
            'exported_at': datetime.now().isoformat(),
            'preferences': self.preferences.to_dict(),
            'interactions': [i.to_dict() for i in self.interaction_history],
            'progress': self.progress_tracker,
            'scenarios': {sid: s.to_dict() for sid, s in self.scenarios.items()}
        }
        
        with open(export_path, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        self.logger.info(f"Exported user data to {export_path}")
        return str(export_path)
    
    def delete_user_data(self, confirm: bool = False):
        """
        Delete all user data (models, interactions, preferences).
        
        Args:
            confirm: Must be True to actually delete (safety check)
        """
        if not confirm:
            raise ValueError("Must confirm deletion by setting confirm=True")
        
        import shutil
        
        if self.user_base_dir.exists():
            shutil.rmtree(self.user_base_dir)
            self.logger.info(f"Deleted all data for user {self.user_id}")
        else:
            self.logger.warning(f"No data found for user {self.user_id}")
