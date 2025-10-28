"""
🤖 Chatbot Service - Admin-Backend Bridge
==========================================
Connects user portal chatbots to admin AI services for:
- Interview Coach Chatbot
- Career Coach Chatbot  
- Mentorship Coach Chatbot
- Resume Builder Chatbot

This service acts as a bridge between Streamlit user pages and
the admin backend AI systems (OpenAI, Claude, Portal Bridge).
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
import json
import sys
from datetime import datetime

# Setup paths
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

# Try to import Portal Bridge from admin backend
try:
    sys.path.insert(0, str(current_dir.parent / "BACKEND-ADMIN-REORIENTATION"))
    from shared_backend.services.portal_bridge import PortalBridge
    PORTAL_BRIDGE_AVAILABLE = True
except ImportError:
    PORTAL_BRIDGE_AVAILABLE = False
    print("⚠️ Portal Bridge not available - using fallback responses")


class ChatbotService:
    """
    Service for managing AI chatbot interactions across coaching specialties.
    Routes user messages to appropriate AI backend and formats responses.
    """
    
    def __init__(self):
        self.portal_bridge = self._init_portal_bridge()
        self.conversation_history = {}  # {user_id: {coach_type: [messages]}}
        
    def _init_portal_bridge(self) -> Optional[Any]:
        """Initialize Portal Bridge connection to admin AI"""
        if PORTAL_BRIDGE_AVAILABLE:
            try:
                bridge = PortalBridge()
                print("✅ Portal Bridge initialized")
                return bridge
            except Exception as e:
                print(f"❌ Portal Bridge initialization failed: {e}")
        return None
    
    def get_response(
        self, 
        coach_type: str, 
        user_message: str, 
        user_id: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Get AI response from appropriate coaching chatbot.
        
        Args:
            coach_type: 'interview', 'career', 'mentorship', or 'resume'
            user_message: User's input message
            user_id: Unique user identifier
            context: Additional context (e.g., resume data, job info, goals)
            
        Returns:
            AI-generated response string
        """
        
        # Initialize conversation history for user if needed
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = {
                'interview': [],
                'career': [],
                'mentorship': [],
                'resume': []
            }
        
        # Add user message to history
        self.conversation_history[user_id][coach_type].append({
            'role': 'user',
            'content': user_message,
            'timestamp': datetime.now().isoformat()
        })
        
        # Route to appropriate coach
        if self.portal_bridge:
            response = self._get_ai_response(coach_type, user_message, user_id, context)
        else:
            response = self._get_fallback_response(coach_type, user_message)
        
        # Add AI response to history
        self.conversation_history[user_id][coach_type].append({
            'role': 'assistant',
            'content': response,
            'timestamp': datetime.now().isoformat()
        })
        
        return response
    
    def _get_ai_response(
        self, 
        coach_type: str, 
        user_message: str, 
        user_id: str,
        context: Optional[Dict[str, Any]]
    ) -> str:
        """
        Get AI response from admin backend via Portal Bridge.
        
        TODO: Implement actual Portal Bridge AI call when admin integration is ready.
        For now, returns intelligent fallback responses.
        """
        
        # System prompts for each coach type
        system_prompts = {
            'interview': """You are an expert Interview Coach AI. Help users prepare for job interviews 
            by providing tailored advice, practice questions, feedback on responses, and confidence-building strategies.
            Use the STAR method for behavioral questions. Be encouraging but realistic.""",
            
            'career': """You are an expert Career Coach AI. Help users plan their career path, identify skill gaps,
            set SMART goals, and navigate career transitions. Provide data-driven insights and actionable recommendations.
            Consider market trends and individual strengths.""",
            
            'mentorship': """You are an expert Mentorship Coach AI. Help users find suitable mentors, prepare for
            mentorship sessions, set mentorship goals, and track growth. Facilitate meaningful mentor-mentee connections.
            Focus on maximizing mentorship value.""",
            
            'resume': """You are an expert Resume Builder AI. Help users create compelling resumes by suggesting
            improvements, optimizing keywords, tailoring content to job descriptions, and ensuring ATS compatibility.
            Focus on quantifiable achievements and impact."""
        }
        
        # TODO: Replace with actual Portal Bridge API call
        # Example: response = self.portal_bridge.chat_completion(
        #     messages=[
        #         {'role': 'system', 'content': system_prompts[coach_type]},
        #         {'role': 'user', 'content': user_message}
        #     ],
        #     user_id=user_id,
        #     context=context
        # )
        
        # For now, return intelligent fallback
        return self._get_fallback_response(coach_type, user_message)
    
    def _get_fallback_response(self, coach_type: str, user_message: str) -> str:
        """Intelligent fallback responses when AI backend is unavailable"""
        
        user_message_lower = user_message.lower()
        
        # Interview Coach responses
        if coach_type == 'interview':
            if any(word in user_message_lower for word in ['prepare', 'ready', 'practice']):
                return """Great! Let's prepare for your interview. Here's my recommended approach:

**1. Research Phase** (2-3 days before):
   - Company background, recent news, products
   - Team structure and culture
   - Interviewer profiles (LinkedIn)

**2. Technical Prep** (1 week before):
   - Review core concepts in your domain
   - Practice coding problems (if technical role)
   - Prepare system design examples

**3. Behavioral Prep** (3-4 days before):
   - Use STAR method for 8-10 stories
   - Practice out loud (record yourself!)
   - Prepare questions to ask them

**4. Day-of Checklist**:
   - T-24h: Review notes, light practice
   - T-2h: Mindset prep, avoid cramming
   - T-15m: Breathing exercises, positive self-talk

Would you like me to drill deeper into any of these areas?"""
            
            elif any(word in user_message_lower for word in ['nervous', 'anxious', 'scared', 'worried']):
                return """It's completely normal to feel nervous before an interview! Here are proven techniques to manage anxiety:

**🧘 Mindset Strategies:**
- Reframe nerves as excitement (same physiological response!)
- Remember: They WANT you to succeed
- You're evaluating them too (it's a two-way street)

**💪 Practical Techniques:**
- Power posing for 2 minutes before (Amy Cuddy research)
- Box breathing: 4 counts in, 4 hold, 4 out, 4 hold
- Prepare 3 "confidence anchors" (past wins to recall)

**📝 Preparation = Confidence:**
- Mock interviews reduce anxiety by 40%
- Having 5-6 STAR stories ready gives you flexibility
- Practicing out loud builds muscle memory

Ready to do a quick mock interview to build confidence?"""
            
            elif any(word in user_message_lower for word in ['star', 'behavioral', 'situation']):
                return """Perfect! The STAR method is your secret weapon for behavioral questions:

**S - Situation** (20% of answer):
Set the context briefly. When? Where? What was happening?

**T - Task** (20% of answer):
What was your responsibility? What challenge/goal did you face?

**A - Action** (40% of answer):  ← THIS IS THE MOST IMPORTANT
What specifically did YOU do? Focus on YOUR actions, not the team's.

**R - Result** (20% of answer):
What happened? Quantify if possible! What did you learn?

**Example Template:**
"In my role as [position] at [company] (S), I was tasked with [challenge] (T). 
I approached this by [specific actions 1, 2, 3] (A). As a result, we achieved 
[quantified outcome] and I learned [key takeaway] (R)."

Want to practice with a specific question?"""
            
            else:
                return """I'm here to help you ace your interview! I can assist with:

- 📚 **Common interview questions** and how to answer them
- 🎯 **STAR method** for behavioral questions  
- 💡 **Company research** strategies
- 🗣️ **Mock interviews** and practice sessions
- 😰 **Anxiety management** and confidence building
- 📝 **Questions to ask them** (super important!)

What would be most helpful for your upcoming interview?"""
        
        # Career Coach responses
        elif coach_type == 'career':
            if any(word in user_message_lower for word in ['path', 'direction', 'next', 'goal']):
                return """Excellent question about your career direction! Let's map out your path systematically.

**🎯 Career Path Framework:**

**1. Current State Assessment:**
   - What are your top 3 strengths?
   - What energizes you at work?
   - What drains you?

**2. Future Vision (3-5 years):**
   - What role do you aspire to?
   - What impact do you want to have?
   - What lifestyle do you want?

**3. Gap Analysis:**
   - Technical skills needed
   - Leadership/soft skills needed
   - Experience/credentials needed

**4. Action Plan:**
   - Short-term wins (3-6 months)
   - Medium-term goals (6-18 months)
   - Long-term objectives (2-5 years)

Based on your current role, I typically see 3 main paths:
1. **Technical Leadership** (IC track: Senior → Staff → Principal)
2. **People Management** (EM track: Manager → Director → VP)
3. **Specialist/Consultant** (Deep expertise in niche domain)

Which resonates most with you?"""
            
            elif any(word in user_message_lower for word in ['skill', 'learn', 'develop', 'improve']):
                return """Great focus on skill development! This is how top performers accelerate growth:

**📊 Skills Development Framework:**

**1. Prioritize Skills by ROI:**
   - **High Impact + Quick to Learn**: Do these first
   - **High Impact + Slow to Learn**: Plan long-term
   - **Low Impact**: Delegate or skip

**2. Learning Approaches:**
   - **Projects** (70%): Learn by doing real work
   - **Mentorship** (20%): Learn from others
   - **Courses** (10%): Structured learning

**3. Validation:**
   - Build something real (portfolio project)
   - Get certified (if relevant to your field)
   - Teach others (best way to solidify)

**4. Time Investment:**
   - Dedicate 5-10 hours/week
   - Track progress weekly
   - Review quarterly

For your current career stage, I recommend focusing on:
1. **Technical depth** in your core domain (become the go-to expert)
2. **Adjacent skills** that multiply your impact (e.g., ML + MLOps)
3. **Soft skills** that scale (communication, leadership, strategy)

What's the #1 skill you want to develop first?"""
            
            else:
                return """I'm your AI Career Coach! I specialize in:

- 🗺️ **Career path planning** and trajectory optimization
- 📊 **Skill gap analysis** and development roadmaps
- 🎯 **Goal setting** (SMART goals framework)
- 💼 **Career transitions** and pivots
- 📈 **Promotions** and advancement strategies
- ⚖️ **Work-life balance** and fulfillment

What career challenge are you facing right now?"""
        
        # Mentorship Coach responses
        elif coach_type == 'mentorship':
            if any(word in user_message_lower for word in ['find', 'looking', 'search', 'need']):
                return """Great! Finding the right mentor is crucial. Here's my proven framework:

**🔍 Finding the Right Mentor:**

**1. Define What You Need:**
   - **Career guidance** (where to go next?)
   - **Skill development** (how to improve?)
   - **Industry navigation** (who to know?)
   - **Emotional support** (how to cope?)

**2. Where to Look:**
   - **Internal**: Within your company (easiest to access)
   - **Alumni networks**: Former colleagues, school connections
   - **Professional groups**: LinkedIn, industry associations
   - **IntelliCV Marketplace**: Sector-specific offers (page 42) 💎

**3. Good Mentor Traits:**
   - Relevant experience (5-10 years ahead of you)
   - Communication style fit (coaching vs. directing)
   - Available and committed (1-2 hours/month minimum)
   - Genuinely wants to help (not just networking)

**4. Making the Ask:**
   - Be specific about what you need
   - Respect their time (propose structure)
   - Show you've done your homework
   - Make it easy to say yes

For sector-specific mentorship offers, check out our **Mentorship Marketplace** (page 42).
It's organized by sectors, not people, and requires Annual Pro subscription.

What specific area do you need mentorship in?"""
            
            elif any(word in user_message_lower for word in ['session', 'meeting', 'prepare', 'ready']):
                return """Excellent! Preparation is key to maximizing mentorship value. Here's your session prep checklist:

**📋 Before the Session (24-48h prior):**

1. **Set Clear Objectives:**
   - What's your #1 question/challenge?
   - What decision do you need help with?
   - What specific advice are you seeking?

2. **Share Context in Advance:**
   - Send brief background (2-3 paragraphs)
   - Include any relevant documents
   - Highlight key points you want to discuss

3. **Prepare Specific Questions:**
   - Have 3-5 questions ready (prioritized)
   - Make them open-ended, not yes/no
   - Frame around your goals

**💬 During the Session:**

1. **Start with Context** (5 min):
   - Quick recap of where you are
   - What's happened since last session

2. **Core Discussion** (40-45 min):
   - Lead with your priority question
   - Take notes actively
   - Ask clarifying questions

3. **Action Items** (5-10 min):
   - Summarize key takeaways
   - Commit to specific actions
   - Schedule next session

**✅ After the Session:**

1. Send thank you within 24h
2. Share your action items
3. Update on progress before next session

Want me to create a template for your next session?"""
            
            else:
                return """I'm your Mentorship Coach! I help you:

- 🔍 **Find the right mentor** for your goals
- 📅 **Prepare for sessions** and maximize value
- 📊 **Track your growth** through mentorship
- 🎯 **Set mentorship goals** and measure progress
- 🏪 **Navigate the Mentorship Marketplace** (sector-specific offers on page 42)

The Mentorship Marketplace (page 42) is organized by **sector-specific offers**, not individual people.
It requires Annual Pro (£299/year) subscription for full access.

How can I help you with mentorship today?"""
        
        # Resume Builder responses
        elif coach_type == 'resume':
            return """I'm your Resume Builder AI! I can help you:

- ✍️ **Optimize content** for impact and ATS compatibility
- 🎯 **Tailor resumes** to specific job descriptions
- 📊 **Quantify achievements** with metrics
- 🔑 **Extract keywords** and match requirements
- 📝 **Format properly** for readability and parsing

Upload your resume or paste a job description to get started!"""
        
        return f"I'm here to help with {coach_type} coaching. How can I assist you today?"
    
    def get_conversation_history(self, user_id: str, coach_type: str) -> List[Dict[str, Any]]:
        """Retrieve conversation history for a specific user and coach type"""
        if user_id in self.conversation_history:
            return self.conversation_history[user_id].get(coach_type, [])
        return []
    
    def clear_conversation_history(self, user_id: str, coach_type: Optional[str] = None):
        """Clear conversation history for user (optionally for specific coach)"""
        if user_id in self.conversation_history:
            if coach_type:
                self.conversation_history[user_id][coach_type] = []
            else:
                self.conversation_history[user_id] = {
                    'interview': [],
                    'career': [],
                    'mentorship': [],
                    'resume': []
                }


# Singleton instance
_chatbot_service_instance = None

def get_chatbot_service() -> ChatbotService:
    """Get singleton ChatbotService instance"""
    global _chatbot_service_instance
    if _chatbot_service_instance is None:
        _chatbot_service_instance = ChatbotService()
    return _chatbot_service_instance
