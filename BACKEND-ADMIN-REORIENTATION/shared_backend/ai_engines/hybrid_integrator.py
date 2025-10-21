"""
Hybrid AI Integrator - Orchestrates ALL 7 AI Engines
Connects new backend engines with existing unified_ai_engine.py

Created: October 14, 2025
"""

import logging
from pathlib import Path
import sys
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from collections import defaultdict
import json

# Add paths
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))
services_path = backend_path.parent / "services"
sys.path.insert(0, str(services_path))

# Import new backend engines
from ai_engines.neural_network_engine import NeuralNetworkEngine
from ai_engines.expert_system_engine import ExpertSystemEngine
from ai_engines.feedback_loop_engine import FeedbackLoopEngine
from ai_engines.model_trainer import ModelTrainer
from ai_engines.inference_engine import InferenceEngine  # NEW: 7th AI Engine!
from ai_engines.intelligence_type_registry import IntelligenceTypeRegistry, get_global_registry  # Dynamic registry

# Import existing unified AI engine
try:
    from unified_ai_engine import UnifiedAIEngine
    UNIFIED_AI_AVAILABLE = True
except ImportError:
    UNIFIED_AI_AVAILABLE = False
    logging.warning("unified_ai_engine.py not available - running with new engines only")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class HybridAIIntegrator:
    """
    Orchestrates all 7 AI engines:
    
    LEVEL 1 - CORE INTELLIGENCE (4 engines):
    1. Neural Network Engine - Deep learning & embeddings
    2. Bayesian Inference - Pattern recognition (from unified_ai_engine)
    3. Expert System Engine - Rule-based validation
    4. Inference Engine - Career & job intelligence (NEW!)
    
    LEVEL 2 - ADVANCED PROCESSING (3 engines):
    5. NLP Engine - Semantic understanding (from unified_ai_engine)
    6. LLM Engine - Content generation (from unified_ai_engine)
    7. Statistical Analysis - Data science (from unified_ai_engine)
    
    The Feedback Loop Engine acts as the orchestrator, collecting votes from
    all engines and producing ensemble predictions.
    """
    
    def __init__(self):
        """Initialize all 7 AI engines"""
        logger.info("Initializing Hybrid AI Integrator with 7 engines...")
        
        # Initialize Level 1 engines (Core Intelligence)
        self.neural_network = NeuralNetworkEngine()
        self.expert_system = ExpertSystemEngine()
        self.inference_engine = InferenceEngine()  # NEW: 7th engine!
        self.feedback_loop = FeedbackLoopEngine()
        self.model_trainer = ModelTrainer()
        
        # Initialize existing unified AI engine
        self.unified_ai = None
        if UNIFIED_AI_AVAILABLE:
            try:
                self.unified_ai = UnifiedAIEngine()
                logger.info("Unified AI Engine initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Unified AI Engine: {e}")
        
        # NEW: Initialize Dynamic Intelligence Type Registry
        self.intelligence_registry = get_global_registry()
        self._discover_intelligence_types()
        self._register_intelligence_handlers()
        
        # Register all engines with feedback loop
        self._register_engines()
        
        # Track integration metrics
        self.integration_metrics = {
            'total_predictions': 0,
            'engine_votes': defaultdict(int),
            'ensemble_accuracy': 0.0,
            'last_updated': datetime.now()
        }
        
        logger.info("Hybrid AI Integrator initialized with 7 engines")
    
    def _register_engines(self):
        """Register all available engines with the feedback loop"""
        # Register Level 1 engines (Core Intelligence)
        self.feedback_loop.register_engine(
            "neural_network",
            self.neural_network,
            initial_weight=0.85
        )
        
        self.feedback_loop.register_engine(
            "expert_system",
            self.expert_system,
            initial_weight=0.80
        )
        
        # NEW: Register Inference Engine
        self.feedback_loop.register_engine(
            "inference_engine",
            self.inference_engine,
            initial_weight=0.80
        )
        
        # Create wrapper for unified AI engine components
        if self.unified_ai:
            # Bayesian wrapper
            self.feedback_loop.register_engine(
                "bayesian",
                self._create_bayesian_wrapper(),
                initial_weight=0.75
            )
            
            # NLP wrapper
            self.feedback_loop.register_engine(
                "nlp",
                self._create_nlp_wrapper(),
                initial_weight=0.70
            )
            
            # LLM wrapper
            self.feedback_loop.register_engine(
                "llm",
                self._create_llm_wrapper(),
                initial_weight=0.80
            )
            
            # Fuzzy Logic wrapper
            self.feedback_loop.register_engine(
                "fuzzy",
                self._create_fuzzy_wrapper(),
                initial_weight=0.65
            )
            
            # NEW: Statistical Analysis wrapper
            self.feedback_loop.register_engine(
                "statistical",
                self._create_statistical_wrapper(),
                initial_weight=0.75
            )
        
        logger.info(f"Registered {len(self.feedback_loop.engines)} engines with feedback loop")
    
    def _discover_intelligence_types(self):
        """Discover intelligence types from data directory"""
        try:
            # Look for ai_data_final directory
            data_dir = Path(__file__).parent.parent.parent.parent / 'ai_data_final'
            
            if data_dir.exists():
                logger.info(f"Discovering intelligence types from: {data_dir}")
                stats = self.intelligence_registry.discover_from_directory(data_dir)
                logger.info(f"Discovery complete: {stats['types_discovered']} types from {stats['files_scanned']} files")
            else:
                logger.warning(f"Data directory not found: {data_dir}")
                logger.info("Intelligence registry initialized without discovery")
        except Exception as e:
            logger.error(f"Error during intelligence type discovery: {e}")
    
    def _register_intelligence_handlers(self):
        """Register implemented intelligence type handlers"""
        logger.info("Registering intelligence type handlers...")
        
        # Register implemented handlers from inference_engine
        self.intelligence_registry.register_handler(
            'career_path',
            lambda data: self.inference_engine.infer_career_path(
                profile=data.get('profile', data),
                target_role=data.get('target_role'),
                timeframe_years=data.get('timeframe_years', 5)
            ).to_dict(),
            priority='HIGH',
            description='Career progression predictions using inference engine'
        )
        
        self.intelligence_registry.register_handler(
            'job_match',
            lambda data: self.inference_engine.match_job_to_candidate(
                profile=data.get('profile', {}),
                job=data.get('job', {}),
                include_reasoning=data.get('include_reasoning', True)
            ).to_dict(),
            priority='HIGH',
            description='Job-candidate matching with explainable reasoning'
        )
        
        self.intelligence_registry.register_handler(
            'skill_gap_analysis',
            lambda data: self.inference_engine.predict_skill_gaps(
                current_skills=data.get('current_skills', []),
                target_role=data.get('target_role', '')
            ).to_dict(),
            priority='HIGH',
            description='Identify skill gaps for target role with learning recommendations'
        )
        
        self.intelligence_registry.register_handler(
            'salary_analysis',
            lambda data: self.inference_engine.infer_salary_range(
                role=data.get('role', data.get('job_title', '')),
                location=data.get('location', ''),
                experience_years=data.get('experience_years', 0),
                skills=data.get('skills')
            ).to_dict(),
            priority='HIGH',
            description='Salary range estimation based on market data'
        )
        
        logger.info(f"Registered {len([t for t in self.intelligence_registry.types.values() if t.is_implemented])} handlers")
    
    def _create_bayesian_wrapper(self):
        """Create wrapper for Bayesian engine from unified AI"""
        class BayesianWrapper:
            def __init__(self, unified_ai):
                self.unified_ai = unified_ai
            
            def predict_with_confidence(self, input_data: Dict, task: str) -> Tuple[Any, float, Dict]:
                """Make Bayesian prediction"""
                try:
                    # Use unified AI's Bayesian capabilities
                    if hasattr(self.unified_ai, 'bayesian_engine'):
                        result = self.unified_ai.bayesian_engine.classify(
                            input_data.get('text', ''),
                            input_data.get('features', {})
                        )
                        return (
                            result.get('classification'),
                            result.get('confidence', 0.5),
                            {'method': 'bayesian', 'details': result}
                        )
                except Exception as e:
                    logger.error(f"Bayesian wrapper error: {e}")
                
                return (None, 0.0, {'error': 'Bayesian prediction failed'})
            
            def process_feedback(self, prediction_id: str, feedback: Dict):
                """Process feedback for Bayesian learning"""
                try:
                    if hasattr(self.unified_ai, 'learning_table'):
                        self.unified_ai.learning_table.add_entry(
                            term=feedback.get('term', ''),
                            category=feedback.get('category', ''),
                            context=feedback.get('context', '')
                        )
                except Exception as e:
                    logger.error(f"Bayesian feedback error: {e}")
        
        return BayesianWrapper(self.unified_ai)
    
    def _create_nlp_wrapper(self):
        """Create wrapper for NLP engine from unified AI"""
        class NLPWrapper:
            def __init__(self, unified_ai):
                self.unified_ai = unified_ai
            
            def predict_with_confidence(self, input_data: Dict, task: str) -> Tuple[Any, float, Dict]:
                """Make NLP prediction"""
                try:
                    if hasattr(self.unified_ai, 'nlp_engine'):
                        text = input_data.get('text', '')
                        result = self.unified_ai.nlp_engine.analyze(text)
                        
                        # Extract relevant prediction based on task
                        if task == 'skills_extraction':
                            prediction = result.get('skills', [])
                        elif task == 'job_title_classifier':
                            prediction = result.get('job_title', '')
                        else:
                            prediction = result.get('entities', [])
                        
                        confidence = result.get('confidence', 0.6)
                        
                        return (prediction, confidence, {'method': 'nlp', 'details': result})
                except Exception as e:
                    logger.error(f"NLP wrapper error: {e}")
                
                return (None, 0.0, {'error': 'NLP prediction failed'})
            
            def process_feedback(self, prediction_id: str, feedback: Dict):
                """Process feedback for NLP learning"""
                # NLP models typically don't have direct feedback mechanisms
                # Could update entity recognition patterns here
                pass
        
        return NLPWrapper(self.unified_ai)
    
    def _create_llm_wrapper(self):
        """Create wrapper for LLM engine from unified AI"""
        class LLMWrapper:
            def __init__(self, unified_ai):
                self.unified_ai = unified_ai
            
            def predict_with_confidence(self, input_data: Dict, task: str) -> Tuple[Any, float, Dict]:
                """Make LLM prediction"""
                try:
                    if hasattr(self.unified_ai, 'llm_engine'):
                        prompt = input_data.get('prompt', '')
                        result = self.unified_ai.llm_engine.generate(prompt, task)
                        
                        return (
                            result.get('text', ''),
                            result.get('confidence', 0.7),
                            {'method': 'llm', 'details': result}
                        )
                except Exception as e:
                    logger.error(f"LLM wrapper error: {e}")
                
                return (None, 0.0, {'error': 'LLM prediction failed'})
            
            def process_feedback(self, prediction_id: str, feedback: Dict):
                """Process feedback for LLM fine-tuning"""
                # Could log feedback for future fine-tuning
                pass
        
        return LLMWrapper(self.unified_ai)
    
    def _create_fuzzy_wrapper(self):
        """Create wrapper for Fuzzy Logic engine from unified AI"""
        class FuzzyWrapper:
            def __init__(self, unified_ai):
                self.unified_ai = unified_ai
            
            def predict_with_confidence(self, input_data: Dict, task: str) -> Tuple[Any, float, Dict]:
                """Make Fuzzy Logic prediction"""
                try:
                    if hasattr(self.unified_ai, 'fuzzy_engine'):
                        values = input_data.get('values', {})
                        result = self.unified_ai.fuzzy_engine.evaluate(values)
                        
                        return (
                            result.get('classification'),
                            result.get('membership', 0.5),
                            {'method': 'fuzzy', 'details': result}
                        )
                except Exception as e:
                    logger.error(f"Fuzzy wrapper error: {e}")
                
                return (None, 0.0, {'error': 'Fuzzy prediction failed'})
            
            def process_feedback(self, prediction_id: str, feedback: Dict):
                """Process feedback for Fuzzy rule updates"""
                # Could adjust membership functions based on feedback
                pass
        
        return FuzzyWrapper(self.unified_ai)
    
    def _create_statistical_wrapper(self):
        """Create wrapper for Statistical Analysis engine from unified AI"""
        class StatisticalWrapper:
            def __init__(self, unified_ai):
                self.unified_ai = unified_ai
            
            def predict_with_confidence(self, input_data: Dict, task: str) -> Tuple[Any, float, Dict]:
                """Make Statistical Analysis prediction"""
                try:
                    if hasattr(self.unified_ai, 'statistical_engine'):
                        result = self.unified_ai.statistical_engine.analyze(input_data)
                        
                        return (
                            result.get('prediction'),
                            result.get('confidence', 0.0),
                            {'method': 'statistical', 'details': result}
                        )
                except Exception as e:
                    logger.error(f"Statistical wrapper error: {e}")
                
                return (None, 0.0, {'error': 'Statistical prediction failed'})
            
            def process_feedback(self, prediction_id: str, feedback: Dict):
                """Process feedback for statistical model updates"""
                # Could retrain statistical models based on feedback
                pass
        
        return StatisticalWrapper(self.unified_ai)
    
    def predict(
        self,
        input_data: Dict[str, Any],
        task: str,
        engines_to_use: Optional[List[str]] = None,
        require_expert_validation: bool = True
    ) -> Dict[str, Any]:
        """
        Make a hybrid prediction using all selected engines.
        
        Args:
            input_data: Input data for prediction
            task: Type of task (job_title_classifier, skills_extractor, etc.)
            engines_to_use: List of engine names to use (None = all)
            require_expert_validation: Whether to validate with expert system
        
        Returns:
            Dictionary with prediction, confidence, votes, and validation results
        """
        try:
            logger.info(f"Making hybrid prediction for task: {task}")
            
            # Get ensemble prediction from all engines
            ensemble_result = self.feedback_loop.ensemble_predict(
                input_data=input_data,
                task=task,
                engines_to_use=engines_to_use
            )
            
            # Validate with expert system if required
            validation_result = None
            if require_expert_validation:
                is_valid, triggered_rules, explanation = self.expert_system.validate_prediction(
                    prediction=ensemble_result['prediction'],
                    context=input_data,
                    category=task
                )
                
                validation_result = {
                    'is_valid': is_valid,
                    'triggered_rules': triggered_rules,
                    'explanation': explanation
                }
                
                # If invalid, flag for review
                if not is_valid:
                    logger.warning(f"Prediction failed expert validation: {explanation}")
                    ensemble_result['requires_review'] = True
                    ensemble_result['review_reason'] = explanation
            
            # Update metrics
            self.integration_metrics['total_predictions'] += 1
            for vote in ensemble_result.get('votes', []):
                self.integration_metrics['engine_votes'][vote['engine']] += 1
            self.integration_metrics['last_updated'] = datetime.now()
            
            # Compile final result
            result = {
                'prediction': ensemble_result['prediction'],
                'confidence': ensemble_result['confidence'],
                'ensemble_method': ensemble_result.get('ensemble_method', 'weighted_vote'),
                'engine_votes': ensemble_result.get('votes', []),
                'validation': validation_result,
                'metadata': {
                    'task': task,
                    'timestamp': datetime.now().isoformat(),
                    'engines_used': len(ensemble_result.get('votes', [])),
                    'total_engines_available': len(self.feedback_loop.engines)
                }
            }
            
            logger.info(f"Hybrid prediction complete: {result['confidence']:.2f} confidence")
            return result
            
        except Exception as e:
            logger.error(f"Hybrid prediction error: {e}")
            return {
                'prediction': None,
                'confidence': 0.0,
                'error': str(e),
                'metadata': {'task': task, 'timestamp': datetime.now().isoformat()}
            }
    
    def submit_feedback(
        self,
        original_prediction: Any,
        user_correction: Any,
        context: Dict[str, Any]
    ) -> str:
        """
        Submit feedback that will be distributed to all engines for learning.
        
        Args:
            original_prediction: The original prediction made
            user_correction: The correct answer provided by user
            context: Context data including task, input, etc.
        
        Returns:
            Feedback ID for tracking
        """
        try:
            # Submit to feedback loop
            feedback_id = self.feedback_loop.submit_feedback(
                original_prediction=original_prediction,
                user_correction=user_correction,
                context=context
            )
            
            # Also update unified AI learning table if available
            if self.unified_ai and hasattr(self.unified_ai, 'learning_table'):
                self.unified_ai.learning_table.add_entry(
                    term=str(user_correction),
                    category=context.get('task', 'general'),
                    context=json.dumps(context)
                )
            
            logger.info(f"Feedback submitted: {feedback_id}")
            return feedback_id
            
        except Exception as e:
            logger.error(f"Feedback submission error: {e}")
            raise
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get comprehensive performance report from all engines"""
        try:
            # Get feedback loop performance
            feedback_performance = self.feedback_loop.get_performance_report()
            
            # Get expert system stats
            expert_performance = self.expert_system.get_performance_metrics()
            
            # Get neural network stats
            nn_performance = self.neural_network.get_performance_metrics()
            
            # NEW: Get inference engine stats
            inference_performance = {}
            if hasattr(self.inference_engine, 'get_performance_metrics'):
                inference_performance = self.inference_engine.get_performance_metrics()
            
            # Get unified AI stats if available
            unified_stats = {}
            if self.unified_ai and hasattr(self.unified_ai, 'learning_table'):
                unified_stats = {
                    'learning_table_entries': len(self.unified_ai.learning_table.entries),
                    'verified_entries': sum(1 for e in self.unified_ai.learning_table.entries.values() if e.verified)
                }
            
            # Compile comprehensive report
            report = {
                'integration_metrics': self.integration_metrics,
                'feedback_loop_performance': feedback_performance,
                'expert_system_performance': expert_performance,
                'neural_network_performance': nn_performance,
                'inference_engine_performance': inference_performance,  # NEW!
                'unified_ai_stats': unified_stats,
                'total_engines': len(self.feedback_loop.engines),
                'timestamp': datetime.now().isoformat()
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Performance report error: {e}")
            return {'error': str(e)}
    
    def train_models(
        self,
        scenario_id: Optional[str] = None,
        include_unified_ai_data: bool = True
    ) -> Dict[str, Any]:
        """
        Train models using data from both new and existing systems.
        
        Args:
            scenario_id: Specific scenario to train (None = all)
            include_unified_ai_data: Whether to include data from unified AI learning table
        
        Returns:
            Training results
        """
        try:
            logger.info("Starting hybrid model training...")
            
            results = {}
            
            # Train new backend models
            if scenario_id:
                result = self.model_trainer.train_scenario(scenario_id)
                results[scenario_id] = result
            else:
                # Train all scenarios
                for sid in self.model_trainer.scenarios:
                    result = self.model_trainer.train_scenario(sid)
                    results[sid] = result
            
            # Optionally incorporate unified AI learning data
            if include_unified_ai_data and self.unified_ai:
                if hasattr(self.unified_ai, 'learning_table'):
                    # Export learning table data for training
                    learning_data = self.unified_ai.learning_table.export_verified_entries()
                    results['unified_ai_data_exported'] = len(learning_data)
                    logger.info(f"Exported {len(learning_data)} verified entries from unified AI")
            
            logger.info("Hybrid model training complete")
            return results
            
        except Exception as e:
            logger.error(f"Training error: {e}")
            return {'error': str(e)}
    
    # ========================================================================
    # NEW: Comprehensive Intelligence Methods - ALL Data Types
    # ========================================================================
    
    def run_inference(
        self,
        data: Dict[str, Any],
        inference_type: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Run intelligence operations using dynamic discovery system.
        
        This method routes intelligence requests through the dynamic registry,
        which auto-discovers types from data files and provides:
        - Registered handlers for implemented types
        - Helpful stubs with schemas for unimplemented types
        - Automatic type discovery as new data is added
        
        The system currently discovers 70+ intelligence types from evidence files,
        with 4 fully implemented handlers:
        - career_path: Career progression predictions (HIGH priority)
        - job_match: Job-candidate matching (HIGH priority)  
        - skill_gap_analysis: Skill gaps and learning paths (HIGH priority)
        - salary_analysis: Salary range estimation (HIGH priority)
        
        For comprehensive documentation of all discovered types, see:
        - ALL_70_INTELLIGENCE_TYPES.md
        - EVIDENCE_MAPPING_INTELLIGENCE_TYPES.md
        
        Args:
            data: Input data for inference
            inference_type: Type of intelligence operation (e.g., 'career_path', 'job_match')
            **kwargs: Additional parameters specific to intelligence type
        
        Returns:
            Intelligence results as dictionary. For unimplemented types, returns
            a helpful stub with schema information extracted from evidence files.
        """
        try:
            # Route through dynamic registry
            handler = self.intelligence_registry.get_handler(inference_type)
            
            if handler:
                # Call registered handler
                return handler(data)
            else:
                # Return helpful stub with schema info from registry
                type_info = self.intelligence_registry.get_type_info(inference_type)
                
                if type_info:
                    return {
                        'status': 'not_implemented',
                        'intelligence_type': inference_type,
                        'message': f"Intelligence type '{inference_type}' discovered but not yet implemented",
                        'schema': type_info.schema,
                        'example_usage': type_info.examples[0] if type_info.examples else None,
                        'priority': type_info.priority,
                        'category': type_info.category,
                        'source_files': type_info.source_files,
                        'hint': 'This type was auto-discovered from data files. Implementation coming soon!'
                    }
                else:
                    # Unknown type - not in registry
                    available_types = self.intelligence_registry.list_types()
                    return {
                        'status': 'unknown',
                        'error': f"Unknown intelligence type: {inference_type}",
                        'available_types': available_types[:20],  # Show first 20
                        'total_types': len(available_types),
                        'hint': 'Use one of the available types, or add data files to auto-discover new types'
                    }
        
        except Exception as e:
            logger.error(f"Inference error ({inference_type}): {e}")
            return {
                'status': 'error',
                'error': str(e), 
                'intelligence_type': inference_type
            }


# ============================================================================
# Convenience wrapper for backward compatibility
# ============================================================================

class EnhancedUnifiedAI:
    """
    Enhanced wrapper that provides backward compatibility with existing code
    while leveraging the new hybrid AI integrator.
    
    Use this to replace UnifiedAIEngine in existing code with minimal changes.
    """
    
    def __init__(self):
        """Initialize the enhanced AI system"""
        self.hybrid_integrator = HybridAIIntegrator()
        
        # Expose individual engines for direct access if needed
        self.neural_network = self.hybrid_integrator.neural_network
        self.expert_system = self.hybrid_integrator.expert_system
        self.feedback_loop = self.hybrid_integrator.feedback_loop
        self.unified_ai = self.hybrid_integrator.unified_ai
    
    def predict(self, input_data: Dict, task: str) -> Dict:
        """Make prediction - backward compatible interface"""
        return self.hybrid_integrator.predict(input_data, task)
    
    def submit_feedback(self, prediction: Any, correction: Any, context: Dict) -> str:
        """Submit feedback - backward compatible interface"""
        return self.hybrid_integrator.submit_feedback(prediction, correction, context)
    
    def get_performance(self) -> Dict:
        """Get performance metrics - backward compatible interface"""
        return self.hybrid_integrator.get_performance_report()


# ============================================================================
# Standalone Test
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("HYBRID AI INTEGRATOR - TEST HARNESS")
    print("=" * 80)
    
    # Initialize
    print("\n1. Initializing Hybrid AI Integrator...")
    integrator = HybridAIIntegrator()
    
    print(f"\n   ✓ Registered {len(integrator.feedback_loop.engines)} engines:")
    for engine_name in integrator.feedback_loop.engines:
        weight = integrator.feedback_loop.engine_weights[engine_name]
        print(f"     - {engine_name}: weight={weight:.2f}")
    
    # Test prediction
    print("\n2. Testing Hybrid Prediction...")
    test_input = {
        'text': 'Senior Software Engineer with 8 years of Python and FastAPI experience',
        'job_title': 'Senior Software Engineer',
        'experience_years': 8,
        'skills': ['Python', 'FastAPI', 'Docker']
    }
    
    result = integrator.predict(
        input_data=test_input,
        task='job_title_classifier',
        require_expert_validation=True
    )
    
    print(f"\n   Prediction: {result['prediction']}")
    print(f"   Confidence: {result['confidence']:.2%}")
    print(f"   Engines voted: {result['metadata']['engines_used']}")
    
    if result.get('validation'):
        val = result['validation']
        print(f"   Expert validation: {'✓ PASSED' if val['is_valid'] else '✗ FAILED'}")
        if val['explanation']:
            print(f"   Explanation: {val['explanation']}")
    
    # Test feedback
    print("\n3. Testing Feedback Submission...")
    feedback_id = integrator.submit_feedback(
        original_prediction="Senior Developer",
        user_correction="Senior Software Engineer",
        context={'task': 'job_title_classifier', 'source': 'test'}
    )
    print(f"   ✓ Feedback submitted: {feedback_id}")
    
    # Performance report
    print("\n4. Performance Report...")
    report = integrator.get_performance_report()
    
    print(f"\n   Total predictions: {report['integration_metrics']['total_predictions']}")
    print(f"   Total engines: {report['total_engines']}")
    
    if 'feedback_loop_performance' in report:
        for engine, metrics in report['feedback_loop_performance'].items():
            acc = metrics.get('accuracy', 0)
            conf = metrics.get('avg_confidence', 0)
            print(f"   {engine}: {acc:.1%} accuracy, {conf:.2f} avg confidence")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE - Hybrid AI Integrator is operational!")
    print("=" * 80)
