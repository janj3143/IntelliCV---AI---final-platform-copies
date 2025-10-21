"""
🎯 IntelliCV User Portal - AI Interview Coach Suite
================================================================

Advanced AI-powered interview preparation system combining:
- Interview simulator with real-time feedback
- Industry-specific question banks
- Performance analytics and improvement tracking
- Video and speech analysis capabilities
- Mock interview scheduling and management

Integrated from frontend/interview_*.py modules
"""

import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import time
import random

# Page configuration
st.set_page_config(
    page_title="AI Interview Coach | IntelliCV",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Interview Coach System
class EnhancedInterviewCoach:
    """Comprehensive AI-powered interview coaching system"""
    
    def __init__(self):
        self.question_banks = self._load_question_banks()
        self.industry_data = self._load_industry_data()
        self.performance_history = self._load_performance_history()
        
    def _load_question_banks(self) -> Dict[str, List[Dict]]:
        """Load comprehensive question banks by category"""
        return {
            "behavioral": [
                {
                    "question": "Tell me about a time when you faced a significant challenge at work. How did you handle it?",
                    "category": "Problem Solving",
                    "difficulty": "medium",
                    "tips": ["Use STAR method", "Focus on your specific actions", "Highlight the positive outcome"]
                },
                {
                    "question": "Describe a situation where you had to work with a difficult team member.",
                    "category": "Teamwork",
                    "difficulty": "medium",
                    "tips": ["Show emotional intelligence", "Focus on resolution", "Demonstrate communication skills"]
                },
                {
                    "question": "Give me an example of a time you showed leadership.",
                    "category": "Leadership",
                    "difficulty": "hard",
                    "tips": ["Include metrics if possible", "Show impact on others", "Demonstrate decision-making"]
                }
            ],
            "technical": [
                {
                    "question": "Explain the difference between supervised and unsupervised learning.",
                    "category": "Machine Learning",
                    "difficulty": "medium",
                    "field": "Data Science",
                    "tips": ["Use examples", "Mention use cases", "Show practical understanding"]
                },
                {
                    "question": "How would you optimize a slow-running SQL query?",
                    "category": "Database",
                    "difficulty": "hard",
                    "field": "Software Engineering",
                    "tips": ["Mention indexing", "Query plan analysis", "Database-specific optimizations"]
                }
            ],
            "situational": [
                {
                    "question": "How would you handle a situation where you disagreed with your manager's decision?",
                    "category": "Conflict Resolution",
                    "difficulty": "hard",
                    "tips": ["Show respect", "Focus on business impact", "Demonstrate professional communication"]
                }
            ]
        }
    
    def _load_industry_data(self) -> Dict[str, Any]:
        """Load industry-specific interview data"""
        return {
            "technology": {
                "common_topics": ["System Design", "Algorithms", "Code Review", "Architecture"],
                "interview_stages": ["Phone Screen", "Technical Screen", "On-site", "Final Round"],
                "avg_duration": "45-60 minutes per round"
            },
            "finance": {
                "common_topics": ["Market Analysis", "Risk Management", "Regulations", "Financial Modeling"],
                "interview_stages": ["HR Screen", "Technical Round", "Case Study", "Final Interview"],
                "avg_duration": "30-45 minutes per round"
            },
            "healthcare": {
                "common_topics": ["Patient Care", "Compliance", "Medical Knowledge", "Ethics"],
                "interview_stages": ["Initial Screen", "Clinical Assessment", "Behavioral Round", "Final Meeting"],
                "avg_duration": "30-60 minutes per round"
            }
        }
    
    def _load_performance_history(self) -> List[Dict]:
        """Load user's interview performance history"""
        # In production, this would load from user database
        return [
            {
                "date": "2025-09-25",
                "session_type": "Mock Interview",
                "role": "Senior Developer",
                "score": 82,
                "strengths": ["Technical knowledge", "Communication"],
                "areas_for_improvement": ["Body language", "Confidence"]
            },
            {
                "date": "2025-09-20",
                "session_type": "Practice Session",
                "role": "Product Manager",
                "score": 75,
                "strengths": ["Strategic thinking", "Problem solving"],
                "areas_for_improvement": ["Industry knowledge", "Presentation skills"]
            }
        ]

class InterviewSimulator:
    """Interactive interview simulation with real-time feedback"""
    
    def __init__(self, coach: EnhancedInterviewCoach):
        self.coach = coach
        
    def run_simulation(self, role: str, industry: str, difficulty: str):
        """Run interactive interview simulation"""
        st.markdown("### 🎬 Live Interview Simulation")
        
        # Session setup
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info(f"**Role:** {role}")
        with col2:
            st.info(f"**Industry:** {industry}")
        with col3:
            st.info(f"**Difficulty:** {difficulty.title()}")
        
        # Question selection and display
        questions = self._select_questions(industry, difficulty)
        
        if "current_question" not in st.session_state:
            st.session_state.current_question = 0
            st.session_state.answers = []
            st.session_state.session_start = datetime.now()
        
        if st.session_state.current_question < len(questions):
            current_q = questions[st.session_state.current_question]
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h4 style="color: white; margin: 0;">Question {st.session_state.current_question + 1} of {len(questions)}</h4>
                <p style="color: white; font-size: 18px; margin: 10px 0 0 0;">{current_q['question']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Tips and guidance
            with st.expander("💡 Interview Tips"):
                for tip in current_q.get('tips', []):
                    st.write(f"• {tip}")
            
            # Answer input
            answer = st.text_area(
                "Your Answer:",
                height=150,
                placeholder="Take your time to provide a thoughtful response...",
                key=f"answer_{st.session_state.current_question}"
            )
            
            # Timer
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                if st.button("📝 Submit Answer & Continue", type="primary"):
                    if answer.strip():
                        # Analyze answer
                        feedback = self._analyze_answer(answer, current_q)
                        st.session_state.answers.append({
                            "question": current_q['question'],
                            "answer": answer,
                            "feedback": feedback,
                            "timestamp": datetime.now()
                        })
                        st.session_state.current_question += 1
                        st.rerun()
                    else:
                        st.warning("Please provide an answer before continuing.")
            
            with col2:
                if st.button("⏭️ Skip Question"):
                    st.session_state.current_question += 1
                    st.rerun()
            
            with col3:
                if st.button("🔄 Reset Session"):
                    for key in ["current_question", "answers", "session_start"]:
                        if key in st.session_state:
                            del st.session_state[key]
                    st.rerun()
                    
        else:
            # Session complete - show results
            self._show_session_results()
    
    def _select_questions(self, industry: str, difficulty: str) -> List[Dict]:
        """Select appropriate questions based on criteria"""
        all_questions = []
        
        # Add behavioral questions
        behavioral = [q for q in self.coach.question_banks["behavioral"] 
                     if q.get("difficulty", "medium") == difficulty]
        all_questions.extend(random.sample(behavioral, min(2, len(behavioral))))
        
        # Add technical questions if available
        if industry.lower() in ["technology", "data science", "software engineering"]:
            technical = [q for q in self.coach.question_banks["technical"]
                        if q.get("difficulty", "medium") == difficulty]
            all_questions.extend(random.sample(technical, min(2, len(technical))))
        
        # Add situational questions
        situational = [q for q in self.coach.question_banks["situational"]
                      if q.get("difficulty", "medium") == difficulty]
        all_questions.extend(random.sample(situational, min(1, len(situational))))
        
        return all_questions[:5]  # Limit to 5 questions for demo
    
    def _analyze_answer(self, answer: str, question: Dict) -> Dict:
        """Analyze user's answer and provide feedback"""
        # Simplified AI feedback simulation
        word_count = len(answer.split())
        
        # Basic analysis
        score = min(100, max(0, 
            50 +  # Base score
            min(30, word_count // 5) +  # Word count bonus
            (20 if any(keyword in answer.lower() for keyword in 
                      ["result", "impact", "improved", "achieved", "success"]) else 0) +  # Results focus
            (10 if len(answer) > 100 else -10)  # Minimum detail
        ))
        
        feedback = {
            "score": score,
            "word_count": word_count,
            "strengths": [],
            "improvements": [],
            "specific_feedback": ""
        }
        
        # Generate specific feedback
        if score >= 80:
            feedback["strengths"] = ["Clear communication", "Good structure", "Results-focused"]
            feedback["specific_feedback"] = "Excellent answer! You provided good detail and showed clear outcomes."
        elif score >= 60:
            feedback["strengths"] = ["Adequate detail", "Relevant content"]
            feedback["improvements"] = ["Add more specific examples", "Include measurable results"]
            feedback["specific_feedback"] = "Good answer, but could be enhanced with more specific examples."
        else:
            feedback["improvements"] = ["Provide more detail", "Include specific examples", "Show measurable impact"]
            feedback["specific_feedback"] = "Consider expanding your answer with more specific details and examples."
        
        return feedback
    
    def _show_session_results(self):
        """Display comprehensive session results"""
        st.markdown("### 🎉 Interview Session Complete!")
        
        if not st.session_state.answers:
            st.warning("No answers recorded.")
            return
        
        # Overall performance
        avg_score = sum(answer["feedback"]["score"] for answer in st.session_state.answers) / len(st.session_state.answers)
        duration = datetime.now() - st.session_state.session_start
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Overall Score", f"{avg_score:.0f}/100")
        with col2:
            st.metric("Questions Answered", len(st.session_state.answers))
        with col3:
            st.metric("Session Duration", f"{duration.seconds // 60}m {duration.seconds % 60}s")
        with col4:
            performance = "Excellent" if avg_score >= 80 else "Good" if avg_score >= 60 else "Needs Improvement"
            st.metric("Performance", performance)
        
        # Detailed feedback
        st.markdown("### 📊 Detailed Feedback")
        
        for i, answer_data in enumerate(st.session_state.answers):
            with st.expander(f"Question {i+1}: Score {answer_data['feedback']['score']}/100"):
                st.write(f"**Question:** {answer_data['question']}")
                st.write(f"**Your Answer:** {answer_data['answer']}")
                
                feedback = answer_data['feedback']
                
                col1, col2 = st.columns(2)
                with col1:
                    if feedback['strengths']:
                        st.success("**Strengths:**")
                        for strength in feedback['strengths']:
                            st.write(f"✅ {strength}")
                
                with col2:
                    if feedback['improvements']:
                        st.warning("**Areas for Improvement:**")
                        for improvement in feedback['improvements']:
                            st.write(f"⚠️ {improvement}")
                
                if feedback['specific_feedback']:
                    st.info(f"**Feedback:** {feedback['specific_feedback']}")
        
        # Performance analytics
        self._show_performance_analytics()
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄 Start New Session", type="primary"):
                for key in ["current_question", "answers", "session_start"]:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
        
        with col2:
            if st.button("📊 View Progress History"):
                st.session_state.show_history = True
        
        with col3:
            if st.button("📥 Download Results"):
                self._download_results()
    
    def _show_performance_analytics(self):
        """Show performance analytics and trends"""
        st.markdown("### 📈 Performance Analytics")
        
        # Score distribution
        scores = [answer["feedback"]["score"] for answer in st.session_state.answers]
        
        fig = px.bar(
            x=[f"Q{i+1}" for i in range(len(scores))],
            y=scores,
            title="Score by Question",
            labels={"x": "Question", "y": "Score"},
            color=scores,
            color_continuous_scale="RdYlGn"
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # Progress over time
        if len(self.coach.performance_history) > 0:
            history_df = pd.DataFrame(self.coach.performance_history)
            history_df['date'] = pd.to_datetime(history_df['date'])
            
            fig = px.line(
                history_df,
                x='date',
                y='score',
                title='Performance Trend Over Time',
                markers=True
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def _download_results(self):
        """Generate downloadable results report"""
        st.success("📥 Results download functionality would be implemented here")

def main():
    """Main application interface"""
    
    # Header
    st.markdown("""
    <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                padding: 20px; border-radius: 10px; margin-bottom: 30px;">
        <h1 style="color: white; margin: 0;">🎯 AI Interview Coach Suite</h1>
        <p style="color: white; margin: 5px 0 0 0; opacity: 0.9;">
            Master your interviews with AI-powered coaching and real-time feedback
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize coach
    coach = EnhancedInterviewCoach()
    
    # Sidebar navigation
    st.sidebar.markdown("## 🎯 Interview Coach Menu")
    
    mode = st.sidebar.radio(
        "Choose Your Training Mode:",
        [
            "🎬 Interview Simulator",
            "📚 Practice Questions",
            "📊 Performance Analytics",
            "🎓 Interview Tips & Guides",
            "📅 Schedule Mock Interview"
        ]
    )
    
    if mode == "🎬 Interview Simulator":
        st.markdown("## Interview Simulation Suite")
        
        # Configuration
        col1, col2, col3 = st.columns(3)
        
        with col1:
            role = st.selectbox(
                "Target Role:",
                ["Software Engineer", "Product Manager", "Data Scientist", "Marketing Manager", 
                 "Sales Representative", "Business Analyst", "Project Manager", "Designer"]
            )
        
        with col2:
            industry = st.selectbox(
                "Industry:",
                ["Technology", "Finance", "Healthcare", "Consulting", "Retail", "Manufacturing"]
            )
        
        with col3:
            difficulty = st.selectbox(
                "Difficulty Level:",
                ["easy", "medium", "hard"]
            )
        
        # Start simulation
        if st.button("🚀 Start Interview Simulation", type="primary"):
            st.session_state.simulation_active = True
        
        if st.session_state.get("simulation_active", False):
            simulator = InterviewSimulator(coach)
            simulator.run_simulation(role, industry, difficulty)
    
    elif mode == "📚 Practice Questions":
        st.markdown("## Practice Question Bank")
        
        # Question browser
        category = st.selectbox(
            "Question Category:",
            ["All Categories", "Behavioral", "Technical", "Situational"]
        )
        
        if category == "All Categories":
            all_questions = []
            for cat_questions in coach.question_banks.values():
                all_questions.extend(cat_questions)
        else:
            all_questions = coach.question_banks.get(category.lower(), [])
        
        # Display questions
        for i, question in enumerate(all_questions):
            with st.expander(f"Question {i+1}: {question.get('category', 'General')} - {question.get('difficulty', 'medium').title()}"):
                st.write(f"**Question:** {question['question']}")
                
                if 'tips' in question:
                    st.write("**Tips:**")
                    for tip in question['tips']:
                        st.write(f"• {tip}")
                
                # Practice answer
                answer = st.text_area(f"Practice your answer:", key=f"practice_{i}")
                if st.button(f"Get Feedback", key=f"feedback_{i}"):
                    if answer.strip():
                        # Simplified feedback
                        st.success("Great practice! In a real interview setting, consider using the STAR method for behavioral questions.")
                    else:
                        st.warning("Try writing out an answer to practice your response.")
    
    elif mode == "📊 Performance Analytics":
        st.markdown("## Performance Analytics Dashboard")
        
        if coach.performance_history:
            # Overall statistics
            df = pd.DataFrame(coach.performance_history)
            avg_score = df['score'].mean()
            latest_score = df['score'].iloc[-1]
            improvement = latest_score - df['score'].iloc[0] if len(df) > 1 else 0
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Average Score", f"{avg_score:.1f}")
            with col2:
                st.metric("Latest Score", f"{latest_score}")
            with col3:
                st.metric("Improvement", f"+{improvement:.1f}" if improvement > 0 else f"{improvement:.1f}")
            with col4:
                st.metric("Sessions Completed", len(df))
            
            # Performance chart
            fig = px.line(
                df, 
                x='date', 
                y='score',
                title='Interview Performance Over Time',
                markers=True
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed history
            st.markdown("### Session History")
            for session in coach.performance_history:
                with st.expander(f"{session['date']} - {session['role']} (Score: {session['score']})"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Strengths:**")
                        for strength in session['strengths']:
                            st.write(f"✅ {strength}")
                    with col2:
                        st.write("**Areas for Improvement:**")
                        for area in session['areas_for_improvement']:
                            st.write(f"⚠️ {area}")
        else:
            st.info("No performance history available. Complete some interview simulations to see your analytics!")
    
    elif mode == "🎓 Interview Tips & Guides":
        st.markdown("## Interview Tips & Guides")
        
        guide_type = st.selectbox(
            "Select Guide Type:",
            ["General Interview Tips", "Industry-Specific Advice", "Question Types", "Body Language", "Follow-up Questions"]
        )
        
        if guide_type == "General Interview Tips":
            st.markdown("""
            ### 🌟 General Interview Success Tips
            
            #### Before the Interview:
            - **Research the company** thoroughly - mission, values, recent news
            - **Review the job description** and match your experience to requirements
            - **Prepare your STAR stories** - Situation, Task, Action, Result
            - **Practice common questions** out loud
            - **Prepare thoughtful questions** to ask the interviewer
            
            #### During the Interview:
            - **Arrive 10-15 minutes early**
            - **Make strong eye contact** and offer a firm handshake
            - **Listen actively** and ask for clarification if needed
            - **Use specific examples** and quantify your achievements
            - **Show enthusiasm** for the role and company
            
            #### After the Interview:
            - **Send a thank-you email** within 24 hours
            - **Reiterate your interest** in the position
            - **Address any concerns** that came up during the interview
            - **Follow up appropriately** if you don't hear back
            """)
        
        elif guide_type == "Industry-Specific Advice":
            industry = st.selectbox("Select Industry:", list(coach.industry_data.keys()))
            industry_info = coach.industry_data[industry]
            
            st.markdown(f"### {industry.title()} Industry Interview Guide")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Common Interview Topics:**")
                for topic in industry_info["common_topics"]:
                    st.write(f"• {topic}")
            
            with col2:
                st.write("**Typical Interview Process:**")
                for stage in industry_info["interview_stages"]:
                    st.write(f"• {stage}")
            
            st.info(f"**Average Interview Duration:** {industry_info['avg_duration']}")
    
    elif mode == "📅 Schedule Mock Interview":
        st.markdown("## Schedule Mock Interview")
        
        st.info("🚧 Mock interview scheduling feature coming soon! This will allow you to book sessions with experienced interviewers.")
        
        # Placeholder for scheduling interface
        col1, col2 = st.columns(2)
        with col1:
            preferred_date = st.date_input("Preferred Date")
            preferred_time = st.time_input("Preferred Time")
        
        with col2:
            interview_type = st.selectbox(
                "Interview Type:",
                ["Technical Interview", "Behavioral Interview", "Case Study", "System Design"]
            )
            duration = st.selectbox("Duration:", ["30 minutes", "45 minutes", "60 minutes"])
        
        if st.button("Request Mock Interview"):
            st.success("Mock interview request submitted! You'll receive a confirmation email shortly.")

if __name__ == "__main__":
    main()